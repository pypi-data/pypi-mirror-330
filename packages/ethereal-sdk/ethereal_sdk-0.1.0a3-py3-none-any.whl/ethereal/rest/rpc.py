from typing import Dict, List

from ethereal.constants import API_PREFIX
from ethereal.models.rest import RpcConfigDto, SignatureTypesDto, DomainTypeDto


def get_rpc_config(self, **kwargs) -> RpcConfigDto:
    """Gets RPC configuration.

    Endpoint: GET v1/rpc/config

    Returns:
        RpcConfigDto: EIP-712 Domain Data necessary for message signing.
    """
    endpoint = f"{API_PREFIX}/rpc/config"

    res = self.get(endpoint, **kwargs)
    domain = DomainTypeDto(**res["domain"])
    signatureTypes = SignatureTypesDto(**res["signatureTypes"])
    return RpcConfigDto(domain=domain, signatureTypes=signatureTypes)


def get_signature_types(rpc_config: RpcConfigDto, primary_type: str):
    """Gets EIP-712 signature types.

    Args:
        rpc_config (RpcConfigDto): RPC configuration.
        primary_type (str): Primary type for the signature.

    Returns:
        dict: Dictionary containing signature type definitions.
    """
    return {
        "EIP712Domain": [
            {"name": "name", "type": "string"},
            {"name": "version", "type": "string"},
            {"name": "chainId", "type": "uint256"},
            {"name": "verifyingContract", "type": "address"},
        ],
        primary_type: convert_types(getattr(rpc_config.signatureTypes, primary_type)),
    }


def convert_types(type_string: str) -> List[Dict[str, str]]:
    """Converts type string into EIP-712 field format.

    Args:
        type_string (str): String containing type definitions.

    Returns:
        List[Dict[str, str]]: List of field definitions.
    """
    fields = [comp.strip() for comp in type_string.split(",")]
    type_fields = []
    for field in fields:
        field_type, field_name = field.rsplit(" ", 1)
        type_fields.append({"name": field_name, "type": field_type})
    return type_fields
