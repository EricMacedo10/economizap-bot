"""
AliExpress API integration (Mock implementation).
Uses mock data for development without requiring real API credentials.
"""

from typing import Optional, Dict, Any
from datetime import datetime
import asyncio
import random

from src.integrations.base_api import BaseMarketplaceAPI
from src.integrations.mock_data import MockDataGenerator
from src.models.product import Product, SearchResult
from src.utils.logger import get_logger
from src.config import Config

logger = get_logger(__name__)


class AliExpressAPI(BaseMarketplaceAPI):
    """
    AliExpress API integration (Mock).
    
    This is a mock implementation that generates realistic product data
    for development and testing without requiring real AliExpress API credentials.
    
    When ready for production, replace this with AliExpressAPIReal that uses
    the actual AliExpress Affiliate API.
    """
    
    # USD to BRL exchange rate (approximate, would be fetched from API in real implementation)
    USD_TO_BRL = 5.0
    
    def __init__(self):
        """Initialize AliExpress API."""
        super().__init__("AliExpress")
        
        # Get credentials from config (not used in mock, but ready for real API)
        self.app_key = Config.ALIEXPRESS_APP_KEY
        self.app_secret = Config.ALIEXPRESS_APP_SECRET
        self.tracking_id = Config.ALIEXPRESS_TRACKING_ID
        
        logger.info("AliExpress API initialized (MOCK MODE)")
    
    async def search(self, query: str) -> SearchResult:
        """
        Search for products on AliExpress (Mock).
        
        Args:
            query: Search query string
            
        Returns:
            SearchResult: Search results with mock products
        """
        start_time = datetime.now()
        
        # Normalize query
        normalized_query = self._normalize_query(query)
        logger.info(f"Searching AliExpress for: {normalized_query} (MOCK)")
        
        try:
            # Simulate API delay (AliExpress can be slower due to international connection)
            await asyncio.sleep(random.uniform(1.0, 2.0))
            
            # Generate mock products
            # AliExpress typically has lower prices
            mock_products_data = MockDataGenerator.generate_mock_products(
                query=normalized_query,
                marketplace=self.marketplace_name,
                count=self.max_results
            )
            
            # Parse to Product objects
            products = []
            for item in mock_products_data:
                product = self._parse_product(item)
                if product:
                    products.append(product)
            
            # Calculate search time
            search_time = (datetime.now() - start_time).total_seconds()
            
            logger.info(f"AliExpress: Found {len(products)} products (MOCK) in {search_time:.2f}s")
            
            return self._create_search_result(query, products, search_time)
            
        except Exception as e:
            logger.error(f"AliExpress: Search failed - {e}", exc_info=True)
            return self._create_search_result(query, [], 0.0)
    
    def _parse_product(self, item: Dict[str, Any]) -> Optional[Product]:
        """
        Parse a product from mock data.
        
        Args:
            item: Mock product data
            
        Returns:
            Optional[Product]: Parsed product or None if parsing fails
        """
        try:
            # Extract data
            product_id = item.get('id')
            name = item.get('name')
            price = item.get('price')
            original_price = item.get('original_price')
            image_url = item.get('image_url')
            
            # Validate required fields
            if not all([product_id, name, price]):
                logger.debug("AliExpress: Skipping item with missing required fields")
                return None
            
            # Add international shipping note to name
            name_with_note = f"{name} (Envio Internacional)"
            
            # Generate product URL (mock)
            product_code = random.randint(1000000000000, 9999999999999)
            url = f"https://pt.aliexpress.com/item/{product_code}.html"
            
            # Generate affiliate link
            affiliate_url = self._generate_affiliate_link(url)
            
            # Create Product object
            product = Product(
                id=str(product_id),
                name=name_with_note,
                price=float(price),
                original_price=float(original_price) if original_price else None,
                marketplace=self.marketplace_name,
                url=affiliate_url,
                image_url=image_url,
                currency="BRL",
                timestamp=datetime.now()
            )
            
            logger.debug(f"AliExpress: Parsed product - {name[:50]}... - R$ {price}")
            
            return product
            
        except Exception as e:
            logger.error(f"AliExpress: Failed to parse product - {e}")
            return None
    
    def _generate_affiliate_link(self, original_url: str) -> str:
        """
        Generate affiliate link for AliExpress.
        
        Args:
            original_url: Original product URL
            
        Returns:
            str: Affiliate link
        """
        # In mock mode, just return original URL
        # In real implementation, use AliExpress tracking link generation
        # Example: https://s.click.aliexpress.com/e/_tracking_id
        
        return original_url
    
    @staticmethod
    def convert_usd_to_brl(usd_price: float) -> float:
        """
        Convert USD price to BRL.
        
        Args:
            usd_price: Price in USD
            
        Returns:
            float: Price in BRL
        """
        return round(usd_price * AliExpressAPI.USD_TO_BRL, 2)
