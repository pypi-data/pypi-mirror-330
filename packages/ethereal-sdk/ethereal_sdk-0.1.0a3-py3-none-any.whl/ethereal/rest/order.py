from typing import List, Optional

from ethereal.constants import API_PREFIX
from ethereal.rest.util import generate_nonce, uuid_to_bytes32
from ethereal.rest.rpc import get_signature_types
from ethereal.models.rest import (
    OrderDto,
    ListOfOrderDtos,
    ListOfOrderFillDtos,
    ListOfTradeDtos,
    SubmitOrderDto,
    SubmitOrderLimitDtoData,
    SubmitOrderMarketDtoData,
    CancelOrderDto,
    CancelOrderDtoData,
    ListOfCancelOrderResultDtos,
    V1OrderGetParametersQuery,
    V1OrderFillGetParametersQuery,
    V1OrderTradeGetParametersQuery,
)


def list_orders(self, **kwargs) -> ListOfOrderDtos:
    """Lists orders for a subaccount.

    Endpoint: GET v1/order

    Returns:
        ListOfOrderDtos: List of order information.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/order",
        request_model=V1OrderGetParametersQuery,
        response_model=ListOfOrderDtos,
        **kwargs,
    )
    return res.data


def list_fills(
    self,
    **kwargs,
) -> ListOfOrderFillDtos:
    """Lists order fills.

    Endpoint: GET v1/order/fill

    Returns:
        ListOfOrderFillDtos: List of order fill information.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/order/fill",
        request_model=V1OrderFillGetParametersQuery,
        response_model=ListOfOrderFillDtos,
        **kwargs,
    )
    return res.data


def list_trades(
    self,
    **kwargs,
) -> ListOfTradeDtos:
    """Lists order trades.

    Endpoint: GET v1/order/trade

    Args:
        productId (str, optional): UUID of the product.

    Returns:
        ListOfTradeDtos: List of trade information.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/order/trade",
        request_model=V1OrderTradeGetParametersQuery,
        response_model=ListOfTradeDtos,
        **kwargs,
    )
    return res.data


def get_order(self, id: str, **kwargs) -> OrderDto:
    """Gets a specific order by ID.

    Endpoint: GET v1/order/{id}

    Args:
        id (str): UUID of the order.

    Returns:
        OrderDto: Order information.
    """
    params = {}
    endpoint = f"{API_PREFIX}/order/{id}"
    response = self.get(endpoint, params=params, **kwargs)
    return OrderDto(**response)


def submit_order(
    self,
    sender: str,
    price: str,
    quantity: str,
    side: int,
    subaccount: str,
    onchainId: float,
    orderType: str,
    timeInForce: Optional[str] = None,
    postOnly: Optional[bool] = False,
    **kwargs,
) -> OrderDto:
    """Submits a new order.

    Endpoint: POST v1/order/submit

    Args:
        sender (str): Address of the sender.
        price (str): Order price.
        quantity (str): Order quantity.
        side (Side): Order side (BUY/SELL).
        subaccount (str): Subaccount address.
        onchainId (float): On-chain product ID.
        orderType (str): Type of order (LIMIT/MARKET).
        timeInForce (str, optional): Time in force for limit orders.
        postOnly (bool, optional): Post-only flag for limit orders.

    Returns:
        OrderDto: Created order information.
    """
    endpoint = f"{API_PREFIX}/order/submit"

    domain = self.rpc_config.domain.model_dump(mode="json")
    primary_type = "TradeOrder"
    types = get_signature_types(self.rpc_config, primary_type)

    nonce = generate_nonce()

    # Common order data
    order_data = {
        "sender": sender,
        "subaccount": subaccount,
        "quantity": quantity,
        "price": price,
        "side": side,
        "engineType": 0,  # PERP
        "onchainId": onchainId,
        "nonce": nonce,
        "type": orderType,
        "reduceOnly": False,  # TODO: make this configurable
    }

    message = {
        "sender": sender,
        "subaccount": subaccount,
        "quantity": int(float(quantity) * 1e9),
        "price": int(float(price) * 1e9),
        "side": side,
        "engineType": 0,
        "productId": int(onchainId),
        "nonce": nonce,
    }

    # Create specific order data based on type
    if orderType == "LIMIT":
        order_data.update(
            {
                "timeInForce": timeInForce,
                "postOnly": postOnly,
            }
        )
        data_model = SubmitOrderLimitDtoData(**order_data)
    elif orderType == "MARKET":
        data_model = SubmitOrderMarketDtoData(**order_data)
    else:
        raise ValueError(f"Invalid order type: {orderType}")

    # Prepare signature
    signature = self.chain.sign_message(
        self.chain.private_key, domain, types, primary_type, message
    )
    submit_order = SubmitOrderDto(data=data_model, signature=signature)

    res = self.post(endpoint, data=submit_order.model_dump(mode="json"), **kwargs)
    return OrderDto(**res)


def cancel_order(
    self, orderId: str, sender: str, subaccount: str, **kwargs
) -> List[OrderDto]:
    """Cancels an existing order.

    Endpoint: POST v1/order/cancel

    Args:
        orderId (str): UUID of the order to cancel.
        sender (str): Address of the sender.
        subaccount (str): Subaccount address.

    Returns:
        List[OrderDto]: List of canceled orders.
    """
    endpoint = f"{API_PREFIX}/order/cancel"

    domain = self.rpc_config.domain.model_dump(mode="json")
    primary_type = "CancelOrder"
    types = get_signature_types(self.rpc_config, primary_type)

    nonce = generate_nonce()

    data = CancelOrderDtoData(
        sender=sender, subaccount=subaccount, nonce=nonce, orderIds=[orderId]
    )

    # Prepare message for signing
    message = data.model_dump(mode="json")
    message["orderIds"] = [uuid_to_bytes32(orderId)]

    signature = self.chain.sign_message(
        self.chain.private_key, domain, types, primary_type, message
    )

    cancel_order = CancelOrderDto(data=data, signature=signature)

    response = self.post(endpoint, data=cancel_order.model_dump(mode="json"), **kwargs)
    return ListOfCancelOrderResultDtos(**response).data
