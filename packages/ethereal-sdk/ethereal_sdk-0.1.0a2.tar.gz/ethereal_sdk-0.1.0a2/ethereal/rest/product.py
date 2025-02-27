from typing import List

from ethereal.constants import API_PREFIX
from ethereal.models.rest import (
    ProductDto,
    ListOfProductDtos,
    MarketLiquidityDto,
    MarketPriceDto,
    ListOfMarketPriceDtos,
)


def list_products(self, **kwargs) -> ListOfProductDtos:
    """Lists all products and their configurations.

    Endpoint: GET v1/product

    Returns:
        ListOfProductDtos: List of product configurations.
    """
    endpoint = f"{API_PREFIX}/product"
    res = self.get(endpoint, **kwargs)
    # TODO handle 'hasNext' in res
    return [ProductDto(**product) for product in res.get("data", [])]


def get_market_liquidity(self, productId, **kwargs) -> MarketLiquidityDto:
    """Gets market liquidity for a product.

    Endpoint: GET v1/product/market-liquidity

    Args:
        productId (str): UUID of the product.

    Returns:
        MarketLiquidityDto: Market liquidity information.
    """
    endpoint = f"{API_PREFIX}/product/market-liquidity"

    params = {
        "productId": productId,
    }

    res = self.get(endpoint, params=params, **kwargs)
    return MarketLiquidityDto(**res)


def list_market_prices(self, productIds: List[str], **kwargs) -> ListOfMarketPriceDtos:
    """Gets market prices for multiple products.

    Endpoint: GET v1/product/market-price

    Args:
        productIds (List[str]): List of product UUIDs.

    Returns:
        ListOfMarketPriceDtos: List of market prices.
    """
    endpoint = f"{API_PREFIX}/product/market-price"

    params = {
        "productIds": productIds,
    }

    res = self.get(endpoint, params=params, **kwargs)
    return [MarketPriceDto(**market_price) for market_price in res.get("data", [])]
