"""
Shopee API integration (Mock implementation).
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


class ShopeeAPI(BaseMarketplaceAPI):
    """
    Shopee API integration (Mock).
    
    This is a mock implementation that generates realistic product data
    for development and testing without requiring real Shopee API credentials.
    
    When ready for production, replace this with ShopeeAPIReal that uses
    the actual Shopee Open Platform API.
    """
    
    def __init__(self):
        """Initialize Shopee API."""
        super().__init__("Shopee")
        
        # Get credentials from config (not used in mock, but ready for real API)
        self.partner_id = Config.SHOPEE_PARTNER_ID
        self.partner_key = Config.SHOPEE_PARTNER_KEY
        
        logger.info("Shopee API initialized (MOCK MODE)")
    
    async def search(self, query: str) -> SearchResult:
        """
        Search for products on Shopee (Mock).
        
        Args:
            query: Search query string
            
        Returns:
            SearchResult: Search results with mock products
        """
        start_time = datetime.now()
        
        # Normalize query
        normalized_query = self._normalize_query(query)
        logger.info(f"Searching Shopee for: {normalized_query} (MOCK)")
        
        try:
            # Simulate API delay
            await asyncio.sleep(random.uniform(0.5, 1.5))
            
            # Generate mock products
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
            
            logger.info(f"Shopee: Found {len(products)} products (MOCK) in {search_time:.2f}s")
            
            return self._create_search_result(query, products, search_time)
            
        except Exception as e:
            logger.error(f"Shopee: Search failed - {e}", exc_info=True)
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
                logger.debug("Shopee: Skipping item with missing required fields")
                return None
            
            # Generate product URL (mock)
            # Shopee uses itemid and shopid in URLs
            shop_id = random.randint(100000000, 999999999)
            item_id = random.randint(1000000000, 9999999999)
            url = f"https://shopee.com.br/product/{shop_id}/{item_id}"
            
            # Generate affiliate link
            affiliate_url = self._generate_affiliate_link(url)
            
            # Create Product object
            product = Product(
                id=str(product_id),
                name=name,
                price=float(price),
                original_price=float(original_price) if original_price else None,
                marketplace=self.marketplace_name,
                url=affiliate_url,
                image_url=image_url,
                currency="BRL",
                timestamp=datetime.now()
            )
            
            logger.debug(f"Shopee: Parsed product - {name[:50]}... - R$ {price}")
            
            return product
            
        except Exception as e:
            logger.error(f"Shopee: Failed to parse product - {e}")
            return None
    
    def _generate_affiliate_link(self, original_url: str) -> str:
        """
        Generate affiliate link for Shopee.
        
        Args:
            original_url: Original product URL
            
        Returns:
            str: Affiliate link
        """
        # In mock mode, just return original URL
        # In real implementation, use Shopee's affiliate link generation API
        
        return original_url
