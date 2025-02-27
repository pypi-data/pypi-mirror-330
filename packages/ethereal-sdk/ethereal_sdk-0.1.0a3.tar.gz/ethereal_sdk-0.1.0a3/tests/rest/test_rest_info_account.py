"""Test simple REST API informational calls that require an account"""

from typing import List
from ethereal.models.rest import (
    OrderDto,
    OrderFillDto,
    TradeDto,
    TransferDto,
    WithdrawDto,
    SubaccountBalanceDto,
    SignerDto,
)


def test_rest_info_subaccount_balances(rc, sid):
    """Test retrieving balances for a specific subaccount."""
    subaccount_balances = rc.get_subaccount_balances(subaccountId=sid)
    assert isinstance(subaccount_balances, List)
    assert all(isinstance(sb, SubaccountBalanceDto) for sb in subaccount_balances)


def test_rest_info_orders(rc, sid):
    """Test retrieving list of orders for a specific subaccount."""
    orders = rc.list_orders(subaccountId=sid)
    assert isinstance(orders, List)
    assert all(isinstance(o, OrderDto) for o in orders)


def test_rest_info_fills(rc, sid):
    """Test retrieving list of fills for a specific subaccount."""
    fills = rc.list_fills(subaccountId=sid)
    assert isinstance(fills, List)
    assert all(isinstance(f, OrderFillDto) for f in fills)


def test_rest_info_trades(rc, sid):
    """Test retrieving list of trades."""
    params = {
        "productId": rc.products[0].id,
        "order": "desc",
        "limit": 100,
    }
    trades = rc.list_trades(**params)
    assert isinstance(trades, List)
    assert all(isinstance(t, TradeDto) for t in trades)


def test_rest_info_transfers(rc, sid):
    """Test retrieving list of transfers for a specific subaccount."""
    transfers = rc.list_token_transfers(sid)
    assert isinstance(transfers, List)
    assert all(isinstance(t, TransferDto) for t in transfers)


def test_rest_info_withdraws(rc, sid):
    """Test retrieving list of withdraws for a specific subaccount."""
    withdraws = rc.list_token_withdraws(sid)
    assert isinstance(withdraws, List)
    assert all(isinstance(w, WithdrawDto) for w in withdraws)


def test_rest_info_linked_signers(rc, sid):
    """Test retrieving list of linked signers for a specific subaccount."""
    linked_signers = rc.list_signers(sid)
    assert isinstance(linked_signers, List)
    assert all(isinstance(ls, SignerDto) for ls in linked_signers)
