from ethereal.constants import API_PREFIX
from ethereal.models.rest import ListOfFundingDtos, FundingDto, Range


def list_funding_rates(
    self, productId: str, range: Range, **kwargs
) -> ListOfFundingDtos:
    """Lists funding rates for a product.

    Endpoint: GET v1/funding/rate

    Args:
        productId (str): UUID of the product.
        range (Range): Time range for funding rates.

    Returns:
        ListOfFundingDtos: List of funding rate information.
    """
    endpoint = f"{API_PREFIX}/funding/rate"

    params = {"productId": productId, "range": range}

    res = self.get(endpoint, params=params, **kwargs)
    return [FundingDto(**rate) for rate in res.get("data", [])]
