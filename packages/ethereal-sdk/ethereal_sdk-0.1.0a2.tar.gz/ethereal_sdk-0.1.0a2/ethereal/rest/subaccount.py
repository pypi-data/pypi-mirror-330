from ethereal.constants import API_PREFIX
from ethereal.models.rest import (
    SubaccountDto,
    ListOfSubaccountDtos,
    SubaccountBalanceDto,
    ListOfSubaccountBalanceDtos,
)


def list_subaccounts(self, sender, **kwargs) -> ListOfSubaccountDtos:
    """Lists subaccounts for a sender.

    Endpoint: GET v1/subaccount

    Args:
        sender (str): Address of the sender.

    Returns:
        ListOfSubaccountDtos: List of subaccount information.
    """
    endpoint = f"{API_PREFIX}/subaccount/"

    params = {
        "sender": sender,
    }

    res = self.get(endpoint, params=params, **kwargs)
    # TODO handle 'hasNext' in res
    return [SubaccountDto(**subaccount) for subaccount in res["data"]]


def get_subaccount(self, subaccountId, **kwargs) -> SubaccountDto:
    """Gets a specific subaccount by ID.

    Endpoint: GET v1/subaccount/{subaccountId}

    Args:
        subaccountId (str): UUID of the subaccount.

    Returns:
        SubaccountDto: Subaccount information.
    """
    endpoint = f"{API_PREFIX}/subaccount/{subaccountId}"

    res = self.get(endpoint, **kwargs)
    return SubaccountDto(**res)


def get_subaccount_balances(
    self, subaccountId, **kwargs
) -> ListOfSubaccountBalanceDtos:
    """Gets balances for a subaccount.

    Endpoint: GET v1/subaccount/balance

    Args:
        subaccountId (str): UUID of the subaccount.

    Returns:
        ListOfSubaccountBalanceDtos: List of balance information.
    """
    endpoint = f"{API_PREFIX}/subaccount/balance"

    params = {
        "subaccountId": subaccountId,
    }

    res = self.get(endpoint, params=params, **kwargs)
    # TODO handle 'hasNext' in res
    return [SubaccountBalanceDto(**balance) for balance in res["data"]]
