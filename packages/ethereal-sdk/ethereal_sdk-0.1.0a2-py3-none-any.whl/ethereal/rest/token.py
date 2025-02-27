from typing import Optional

from ethereal.constants import API_PREFIX
from ethereal.models.rest import (
    TokenDto,
    ListOfTokenDtos,
    WithdrawDto,
    ListOfWithdrawDtos,
    TransferDto,
    ListOfTransfersDtos,
    InitiateWithdrawDto,
    InitiateWithdrawDtoData,
)
from ethereal.rest.rpc import get_signature_types
from ethereal.rest.util import generate_nonce

# TODO: Add token withdrawal


def list_tokens(
    self,
    **kwargs,
) -> ListOfTokenDtos:
    """Lists all tokens.

    Endpoint: GET v1/token

    Returns:
        ListOfTokenDtos: A list containing all token information.
    """
    endpoint = f"{API_PREFIX}/token"

    params = {}

    res = self.get(endpoint, params=params, **kwargs)
    return [TokenDto(**token) for token in res.get("data", [])]


def get_token(
    self,
    id: str,
    **kwargs,
) -> TokenDto:
    """Gets a specific token by ID.

    Endpoint: GET v1/token/{id}

    Args:
        id (str): The token identifier.

    Returns:
        TokenDto: The requested token information.
    """
    params = {}

    endpoint = f"{API_PREFIX}/token/{id}"

    res = self.get(endpoint, params=params, **kwargs)
    return TokenDto(**res)


def list_token_withdraws(
    self,
    subaccountId: str,
    active: Optional[bool] = None,
    **kwargs,
) -> ListOfWithdrawDtos:
    """Lists token withdrawals for a subaccount.

    Endpoint: GET v1/token/withdraw

    Args:
        subaccountId (str): UUID of the registered subaccount.
        active (bool, optional): Filter by active status.

    Returns:
        ListOfWithdrawDtos: A list of withdrawal information.
    """
    endpoint = f"{API_PREFIX}/token/withdraw"

    params = {"subaccountId": subaccountId}

    if active is not None:
        params["active"] = active

    res = self.get(endpoint, params=params, **kwargs)
    return [WithdrawDto(**withdraw) for withdraw in res.get("data", [])]


def list_token_transfers(
    self,
    subaccountId: str,
    active: Optional[bool] = None,
    **kwargs,
) -> ListOfTransfersDtos:
    """Lists token transfers for a subaccount.

    Endpoint: GET v1/token/transfer

    Args:
        subaccountId (str): UUID of the registered subaccount.
        active (bool, optional): Filter by active status.

    Returns:
        ListOfTransfersDtos: A list of transfer information.
    """
    endpoint = f"{API_PREFIX}/token/transfer"

    params = {"subaccountId": subaccountId}

    res = self.get(endpoint, params=params, **kwargs)
    return [TransferDto(**transfer) for transfer in res.get("data", [])]


def withdraw_token(
    self,
    subaccount: str,
    tokenId: str,
    token: str,
    amount: int,
    account: str,
    **kwargs,
):
    """Initiates a token withdrawal.

    Endpoint: POST v1/token/{tokenId}/withdraw

    Args:
        subaccount (str): UUID of the registered subaccount.
        tokenId (str): UUID of the token.
        token (str): Token address.
        amount (int): Amount to withdraw.
        account (str): Destination account.

    Returns:
        WithdrawDto: The withdrawal information.
    """
    endpoint = f"{API_PREFIX}/token/{tokenId}/withdraw"

    domain = self.rpc_config.domain.model_dump(mode="json")
    primary_type = "InitiateWithdraw"
    types = get_signature_types(self.rpc_config, primary_type)

    nonce = generate_nonce()

    data = InitiateWithdrawDtoData(
        account=account,
        subaccount=subaccount,
        token=token,
        amount=amount,
        nonce=nonce,
    )

    # Prepare message for signing
    message = data.model_dump(mode="json")
    signature = self.chain.sign_message(
        self.chain.private_key, domain, types, primary_type, message
    )

    initiate_withdraw = InitiateWithdrawDto(data=data, signature=signature)
    response = self.post(
        endpoint, data=initiate_withdraw.model_dump(mode="json"), **kwargs
    )
    return WithdrawDto(**response)
