"""`pera_wallet` package."""

import os
from typing import Literal, TypeAlias, TypedDict

import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        'pera_wallet',
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url='http://localhost:3001',
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, 'frontend/build')
    _component_func = components.declare_component('pera_wallet', path=build_dir)


class WalletConnected(TypedDict):
    """Wallet connected state."""

    status: Literal['connected']
    address: str


class WalletDisconnected(TypedDict):
    """Wallet not connected state."""

    status: Literal['unavailable', 'disconnected']
    address: None


WalletState: TypeAlias = WalletConnected | WalletDisconnected


class PendingTransaction(TypedDict):
    """Pending transaction state."""

    status: Literal['proposed', 'signed', 'submitted']
    transaction_id: None


class ConfirmedTransaction(TypedDict):
    """Confirmed transaction state."""

    status: Literal['confirmed']
    transaction_id: str


class FailedTransaction(TypedDict):
    """Failed transaction state."""

    status: Literal['failed']
    msg: str


TransactionState: TypeAlias = PendingTransaction | ConfirmedTransaction | FailedTransaction

AppState: TypeAlias = tuple[WalletState, TransactionState | None]


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def pera_wallet(
    *,
    network: Literal['mainnet', 'testnet'] = 'mainnet',
    transactions_to_sign: list[str] | None = None,
    frame_height: int = 800,
    key: str | None = None,
) -> AppState:
    """Create a new instance of "pera_wallet".

    Args:
        network (Literal['mainnet', 'testnet'], optional): Name of the Algorand network to connect to. Defaults to 'mainnet'.
        transactions_to_sign (list[str] | None, optional): Optional list of msgpack-encoded transactions to sign. Defaults to None.
        frame_height (int, optional): Frame height for the Pera Wallet auth modal. Defaults to 800.
        key (str | None, optional):
            An optional key that uniquely identifies this component. If this is
                None, and the component's arguments are changed, the component will
                be re-mounted in the Streamlit frontend and lose its current state.
                Defaults to None.

    Returns:
        AppState: The wallet state and transaction state.
    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    component_value = _component_func(
        network=network,
        transactionsToSign=transactions_to_sign or [],
        frameHeight=frame_height,
        key=key,
        default=None,
    )
    if component_value is None:
        return WalletDisconnected(status='disconnected', address=None), None
    return component_value
