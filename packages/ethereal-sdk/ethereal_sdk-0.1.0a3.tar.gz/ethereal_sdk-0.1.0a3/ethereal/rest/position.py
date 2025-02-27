from typing import Optional

from ethereal.constants import API_PREFIX
from ethereal.models.rest import PositionDto, ListOfPositionDtos


def list_positions(
    self,
    subaccountId: str,
    productId: Optional[str] = None,
    onlyOpen: Optional[bool] = None,
    **kwargs,
) -> ListOfPositionDtos:
    """Lists positions for a subaccount.

    Endpoint: GET v1/position

    Args:
        subaccountId (str): UUID of the subaccount.
        productId (str, optional): UUID of the product.
        onlyOpen (bool, optional): Filter for open positions only.

    Returns:
        ListOfPositionDtos: List of position information.
    """
    endpoint = f"{API_PREFIX}/position"

    params = {
        "subaccountId": subaccountId,
    }

    if productId is not None:
        params["productId"] = productId

    if onlyOpen is not None:
        params["open"] = str(onlyOpen).lower()

    res = self.get(endpoint, params=params, **kwargs)
    return [PositionDto(**position) for position in res.get("data", [])]


def get_position(
    self,
    positionId: str,
    **kwargs,
) -> PositionDto:
    """Gets a specific position by ID.

    Endpoint: GET v1/position/{positionId}

    Args:
        positionId (str): UUID of the position.

    Returns:
        PositionDto: Position information.
    """
    endpoint = f"{API_PREFIX}/position/{positionId}"
    res = self.get(endpoint, **kwargs)
    return PositionDto(**res)
