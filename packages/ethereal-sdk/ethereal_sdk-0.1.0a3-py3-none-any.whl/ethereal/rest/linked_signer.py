from typing import Optional

from ethereal.constants import API_PREFIX
from ethereal.models.rest import (
    LinkSignerDto,
    LinkSignerDtoData,
    SignerDto,
    ListOfSignersDto,
    AccountSignerQuotaDto,
)
from ethereal.rest.rpc import get_signature_types
from ethereal.rest.util import generate_nonce


# TODO: Add revoke signer


def list_signers(
    self,
    subaccountId: str,
    active: Optional[bool] = None,
    **kwargs,
) -> ListOfSignersDto:
    """Lists signers for a subaccount.

    Endpoint: GET v1/linked-signer

    Args:
        subaccountId (str): UUID of the subaccount.
        active (bool, optional): Filter by active status.

    Returns:
        ListOfSignersDto: List of signer information.
    """
    endpoint = f"{API_PREFIX}/linked-signer"

    params = {
        "subaccountId": subaccountId,
    }

    if active is not None:
        params["active"] = active

    res = self.get(endpoint, params=params, **kwargs)
    return [SignerDto(**signer) for signer in res.get("data", [])]


def get_signer(
    self,
    id: str,
    **kwargs,
) -> SignerDto:
    """Gets a specific signer by ID.

    Endpoint: GET v1/linked-signer/{id}

    Args:
        id (str): UUID of the signer.

    Returns:
        SignerDto: Signer information.
    """
    params = {}

    endpoint = f"{API_PREFIX}/linked-signer/{id}"

    res = self.get(endpoint, params=params, **kwargs)
    return SignerDto(**res)


def get_signer_quota(
    self,
    subaccountId: str,
    **kwargs,
) -> AccountSignerQuotaDto:
    """Gets the signer quota for a subaccount.

    Endpoint: GET v1/linked-signer/quota

    Args:
        subaccountId (str): UUID of the subaccount.

    Returns:
        AccountSignerQuotaDto: Signer quota configuration.
    """
    endpoint = f"{API_PREFIX}/linked-signer/quota"

    params = {
        "subaccountId": subaccountId,
    }

    res = self.get(endpoint, params=params, **kwargs)
    return AccountSignerQuotaDto(**res)


def get_active_signer(
    self,
    subaccountId: str,
    **kwargs,
) -> SignerDto:
    """Gets the active signer for a subaccount.

    Endpoint: GET v1/linked-signer/active

    Args:
        subaccountId (str): UUID of the subaccount.

    Returns:
        SignerDto: Active signer information.
    """
    endpoint = f"{API_PREFIX}/linked-signer/active"

    params = {
        "subaccountId": subaccountId,
    }

    res = self.get(endpoint, params=params, **kwargs)
    return SignerDto(**res)


def link_signer(
    self,
    sender: str,
    signer: str,
    signerSignature: str,
    subaccount: str,
    subaccountId: str,
    **kwargs,
) -> SignerDto:
    """Links a signer to a subaccount.

    Endpoint: POST v1/linked-signer/link

    Args:
        sender (str): Address of the sender.
        signer (str): Address of the signer.
        signerSignature (str): Signature from the signer.
        subaccount (str): Address of the subaccount.
        subaccountId (str): UUID of the subaccount.

    Returns:
        SignerDto: Created signer information.
    """
    endpoint = f"{API_PREFIX}/linked-signer/link"

    domain = self.rpc_config.domain.model_dump(mode="json")
    primary_type = "LinkSigner"
    types = get_signature_types(self.rpc_config, primary_type)

    data = {
        "sender": sender,
        "signer": signer,
        "subaccountId": subaccountId,
        "subaccount": subaccount,
        "nonce": generate_nonce(),
    }
    model_data = LinkSignerDtoData(**data)
    message = model_data.model_dump(mode="json")
    signature = self.chain.sign_message(
        self.chain.private_key, domain, types, primary_type, message
    )

    link_signer = LinkSignerDto(
        data=data, signature=signature, signerSignature=signerSignature
    )
    res = self.post(endpoint, data=link_signer.model_dump(mode="json"), **kwargs)
    return SignerDto(**res)
