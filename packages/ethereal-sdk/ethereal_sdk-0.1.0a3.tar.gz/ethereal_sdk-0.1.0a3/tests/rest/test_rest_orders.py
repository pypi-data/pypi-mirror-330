"""Test simple REST API calls for submitting orders"""

from typing import List
from ethereal.models.rest import OrderDto, CancelOrderResultDto


def test_rest_limit_order_submit_cancel(rc, sid):
    """Test submitting and cancelling a limit order."""
    subaccount = [s for s in rc.subaccounts if s.id == sid][0]

    pid = rc.products[0].id
    tick_size = float(rc.products_by_id[pid].tickSize)
    prices = rc.list_market_prices([pid])[0]
    best_bid_price = float(prices.bestBidPrice)

    # bid 10% below the best bid price
    bid_price = best_bid_price * 0.90
    bid_price = round(bid_price / tick_size) * tick_size
    order_params = {
        "order_type": "LIMIT",
        "product_id": pid,
        "side": 0,
        "price": bid_price,
        "quantity": 0.001,
        "time_in_force": "GTC",
        "post_only": False,
    }
    order = rc.create_order(**order_params)
    rc.logger.info(f"Limit order: {order}")
    assert isinstance(order, OrderDto)

    # cancel the order
    cancelled_orders = rc.cancel_order(
        sender=rc.chain.address, subaccount=subaccount.name, orderId=order.id
    )
    rc.logger.info(f"Cancelled orders: {cancelled_orders}")
    assert isinstance(cancelled_orders, List)
    assert all(isinstance(o, CancelOrderResultDto) for o in cancelled_orders)


def test_rest_market_order_submit(rc, sid):
    """Test submitting a market order."""
    pid = rc.products[0].id
    order_params = {
        "order_type": "MARKET",
        "product_id": pid,
        "side": 0,
        "quantity": 0.001,
    }
    order = rc.create_order(**order_params)
    rc.logger.info(f"Market order: {order}")
    assert isinstance(order, OrderDto)
