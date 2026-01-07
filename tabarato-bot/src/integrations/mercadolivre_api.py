"""
Mercado Livre API integration.
Implements product search using Mercado Livre's public API.
"""

from typing import Optional, Dict, Any
from datetime import datetime
import urllib.parse

from src.integrations.base_api import BaseMarketplaceAPI
from src.models.product import Product, SearchResult
from src.utils.logger import get_logger
from src.config import Config

logger = get_logger(__name__)


class MercadoLivreAPI(BaseMarketplaceAPI):
    """
    Mercado Livre API integration.
    
    Uses the public Mercado Livre API to search for products.
    Documentation: https://developers.mercadolivre.com.br/
    """
    
    # API endpoints
    BASE_URL = "https://api.mercadolibre.com"
    SEARCH_ENDPOINT = "/sites/MLB/search"
    
    def __init__(self):
        """Initialize Mercado Livre API."""
        super().__init__("Mercado Livre")
        
        # Get credentials from config (for future affiliate features)
        self.app_id = Config.MERCADOLIVRE_APP_ID
        self.secret_key = Config.MERCADOLIVRE_SECRET_KEY
        
        logger.info("Mercado Livre API initialized")
    
    async def search(self, query: str) -> SearchResult:
        """
        Search for products on Mercado Livre.
        
        Args:
            query: Search query string
            
        Returns:
            SearchResult: Search results with products
        """
        start_time = datetime.now()
        
        # Normalize query
        normalized_query = self._normalize_query(query)
        logger.info(f"Searching Mercado Livre for: {normalized_query}")
        
        # Build search URL
        url = f"{self.BASE_URL}{self.SEARCH_ENDPOINT}"
        
        # Build parameters
        params = {
            "q": normalized_query,
            "limit": self.max_results,
            "offset": 0,
            # Sort by relevance (can also use 'price_asc', 'price_desc')
            "sort": "relevance",
            # Only new items
            "condition": "new",
            # Only items with free shipping (optional, can remove)
            # "shipping": "free",
        }
        
        try:
            # Make API request
            data = await self._make_request(url, params=params)
            
            if not data:
                logger.warning("Mercado Livre: No data returned from API")
                return self._create_search_result(query, [], 0.0)
            
            # Parse products
            products = []
            results = data.get("results", [])
            
            logger.info(f"Mercado Livre: Found {len(results)} results")
            
            for item in results:
                product = self._parse_product(item)
                if product:
                    products.append(product)
            
            # Calculate search time
            search_time = (datetime.now() - start_time).total_seconds()
            
            logger.info(f"Mercado Livre: Parsed {len(products)} products in {search_time:.2f}s")
            
            return self._create_search_result(query, products, search_time)
            
        except Exception as e:
            logger.error(f"Mercado Livre: Search failed - {e}", exc_info=True)
            return self._create_search_result(query, [], 0.0)
    
    def _parse_product(self, item: Dict[str, Any]) -> Optional[Product]:
        """
        Parse a product from Mercado Livre API response.
        
        Args:
            item: Raw product data from API
            
        Returns:
            Optional[Product]: Parsed product or None if parsing fails
        """
        try:
            # Extract basic info
            product_id = item.get("id")
            title = item.get("title")
            price = item.get("price")
            permalink = item.get("permalink")
            
            # Validate required fields
            if not all([product_id, title, price, permalink]):
                logger.debug("Mercado Livre: Skipping item with missing required fields")
                return None
            
            # Extract image (use thumbnail or first image)
            thumbnail = item.get("thumbnail")
            image_url = thumbnail.replace("I.jpg", "O.jpg") if thumbnail else None
            
            # Check for original price (discount)
            original_price = item.get("original_price")
            
            # Extract currency
            currency = item.get("currency_id", "BRL")
            
            # Check for free shipping
            shipping = item.get("shipping", {})
            free_shipping = shipping.get("free_shipping", False)
            
            # Generate affiliate link
            affiliate_url = self._generate_affiliate_link(permalink)
            
            # Create Product object
            product = Product(
                id=str(product_id),
                name=title,
                price=float(price),
                original_price=float(original_price) if original_price else None,
                marketplace=self.marketplace_name,
                url=affiliate_url,
                image_url=image_url,
                currency=currency,
                timestamp=datetime.now()
            )
            
            logger.debug(f"Mercado Livre: Parsed product - {title[:50]}... - R$ {price}")
            
            return product
            
        except Exception as e:
            logger.error(f"Mercado Livre: Failed to parse product - {e}")
            return None
    
    def _generate_affiliate_link(self, original_url: str) -> str:
        """
        Generate affiliate link for Mercado Livre.
        
        Args:
            original_url: Original product URL
            
        Returns:
            str: Affiliate link
        """
        # For now, return original URL
        # In the future, add affiliate parameters if you have an affiliate account
        
        # Example with affiliate tag (when you have one):
        # if self.app_id:
        #     separator = "&" if "?" in original_url else "?"
        #     return f"{original_url}{separator}pdp_source=affiliate&tracking_id={self.app_id}"
        
        return original_url
    
    async def get_product_details(self, product_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific product.
        
        Args:
            product_id: Mercado Livre product ID
            
        Returns:
            Optional[Dict]: Product details or None if request fails
        """
        url = f"{self.BASE_URL}/items/{product_id}"
        
        try:
            data = await self._make_request(url)
            return data
        except Exception as e:
            logger.error(f"Mercado Livre: Failed to get product details - {e}")
            return None
