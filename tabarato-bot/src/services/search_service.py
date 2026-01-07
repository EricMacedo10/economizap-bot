"""
Search service for EconomiZap Bot.
Orchestrates product searches across multiple marketplaces.
"""

from typing import List, Optional
from datetime import datetime
import asyncio

from src.models.product import Product, SearchResult
from src.integrations.mercadolivre_api import MercadoLivreAPI
from src.integrations.amazon_api import AmazonAPI
from src.integrations.shopee_api import ShopeeAPI
from src.integrations.aliexpress_api import AliExpressAPI
from src.services.price_service import get_price_service
from src.utils.logger import get_logger
from src.config import Config

logger = get_logger(__name__)


class SearchService:
    """
    Service to orchestrate product searches across marketplaces.
    """
    
    def __init__(self):
        """Initialize search service."""
        self.marketplaces = []
        
        # Phase 2: Mercado Livre (Real API)
        self.mercadolivre = MercadoLivreAPI()
        self.marketplaces.append(self.mercadolivre)
        
        # Phase 4: Additional marketplaces (Mock APIs)
        self.amazon = AmazonAPI()
        self.shopee = ShopeeAPI()
        self.aliexpress = AliExpressAPI()
        
        self.marketplaces.extend([
            self.amazon,
            self.shopee,
            self.aliexpress
        ])
        
        # Initialize price service
        self.price_service = get_price_service()
        
        logger.info(f"Search service initialized with {len(self.marketplaces)} marketplace(s)")
        logger.info(f"Marketplaces: {[m.marketplace_name for m in self.marketplaces]}")
    
    async def search_all(self, query: str) -> SearchResult:
        """
        Search for products across all marketplaces.
        
        Args:
            query: Search query string
            
        Returns:
            SearchResult: Aggregated search results from all marketplaces
        """
        start_time = datetime.now()
        
        logger.info(f"Starting search for: {query}")
        
        # Validate query
        if not self._validate_query(query):
            logger.warning(f"Invalid query: {query}")
            return SearchResult(
                query=query,
                products=[],
                total_results=0,
                search_time=0.0
            )
        
        # Search all marketplaces in parallel
        search_tasks = [
            marketplace.search(query)
            for marketplace in self.marketplaces
        ]
        
        try:
            # Wait for all searches to complete (with timeout)
            results = await asyncio.gather(*search_tasks, return_exceptions=True)
            
            # Aggregate products from all marketplaces
            all_products: List[Product] = []
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Marketplace search failed: {result}")
                    continue
                
                if isinstance(result, SearchResult):
                    all_products.extend(result.products)
                    logger.info(
                        f"{self.marketplaces[i].marketplace_name}: "
                        f"Found {len(result.products)} products"
                    )
            
            # Calculate total search time
            search_time = (datetime.now() - start_time).total_seconds()
            
            # Create initial search result
            initial_result = SearchResult(
                query=query,
                products=all_products,
                total_results=len(all_products),
                search_time=search_time
            )
            
            # Apply price comparison and coupons
            if all_products:
                logger.info("Applying coupons and comparing prices...")
                final_result = self.price_service.compare_prices(initial_result)
            else:
                final_result = initial_result
            
            logger.info(
                f"Search completed: {len(final_result.products)} total products "
                f"in {search_time:.2f}s"
            )
            
            return final_result
            
        except Exception as e:
            logger.error(f"Search failed: {e}", exc_info=True)
            return SearchResult(
                query=query,
                products=[],
                total_results=0,
                search_time=0.0
            )
    
    async def search_marketplace(
        self,
        query: str,
        marketplace_name: str
    ) -> Optional[SearchResult]:
        """
        Search in a specific marketplace.
        
        Args:
            query: Search query
            marketplace_name: Name of marketplace to search
            
        Returns:
            Optional[SearchResult]: Search results or None if marketplace not found
        """
        for marketplace in self.marketplaces:
            if marketplace.marketplace_name.lower() == marketplace_name.lower():
                return await marketplace.search(query)
        
        logger.warning(f"Marketplace not found: {marketplace_name}")
        return None
    
    def _validate_query(self, query: str) -> bool:
        """
        Validate search query.
        
        Args:
            query: Search query to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Check minimum length
        if len(query) < 3:
            return False
        
        # Check maximum length
        if len(query) > 100:
            return False
        
        # Check for dangerous characters
        dangerous_chars = ['<', '>', ';', '&', '|', '$']
        if any(char in query for char in dangerous_chars):
            return False
        
        return True
    
    async def close(self) -> None:
        """Close all marketplace API sessions."""
        close_tasks = [
            marketplace.close()
            for marketplace in self.marketplaces
        ]
        
        await asyncio.gather(*close_tasks, return_exceptions=True)
        logger.info("All marketplace sessions closed")
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()


# Global search service instance
_search_service: Optional[SearchService] = None


def get_search_service() -> SearchService:
    """
    Get the global search service instance.
    
    Returns:
        SearchService: Global search service
    """
    global _search_service
    
    if _search_service is None:
        _search_service = SearchService()
    
    return _search_service
