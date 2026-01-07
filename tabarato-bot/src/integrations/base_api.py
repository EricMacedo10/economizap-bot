"""
Base API class for marketplace integrations.
Provides common functionality for all marketplace APIs.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import aiohttp
import asyncio
from datetime import datetime

from src.models.product import Product, SearchResult
from src.utils.logger import get_logger
from src.config import Config

logger = get_logger(__name__)


class BaseMarketplaceAPI(ABC):
    """
    Abstract base class for marketplace API integrations.
    
    All marketplace integrations should inherit from this class
    and implement the required abstract methods.
    """
    
    def __init__(self, marketplace_name: str):
        """
        Initialize the base API.
        
        Args:
            marketplace_name: Name of the marketplace
        """
        self.marketplace_name = marketplace_name
        self.timeout = Config.SEARCH_TIMEOUT
        self.max_results = Config.MAX_RESULTS_PER_MARKETPLACE
        self.session: Optional[aiohttp.ClientSession] = None
        
        logger.info(f"Initialized {marketplace_name} API integration")
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """
        Get or create aiohttp session.
        
        Returns:
            aiohttp.ClientSession: HTTP session
        """
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
    
    async def close(self) -> None:
        """Close the HTTP session."""
        if self.session and not self.session.closed:
            await self.session.close()
            logger.debug(f"Closed {self.marketplace_name} API session")
    
    @abstractmethod
    async def search(self, query: str) -> SearchResult:
        """
        Search for products in the marketplace.
        
        Args:
            query: Search query string
            
        Returns:
            SearchResult: Search results with products
            
        Raises:
            Exception: If search fails
        """
        pass
    
    @abstractmethod
    def _parse_product(self, item: Dict[str, Any]) -> Optional[Product]:
        """
        Parse a product from API response.
        
        Args:
            item: Raw product data from API
            
        Returns:
            Optional[Product]: Parsed product or None if parsing fails
        """
        pass
    
    async def _make_request(
        self,
        url: str,
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Make HTTP request to API.
        
        Args:
            url: Request URL
            method: HTTP method (GET, POST, etc.)
            params: Query parameters
            headers: Request headers
            json_data: JSON body data
            
        Returns:
            Optional[Dict]: Response JSON or None if request fails
        """
        session = await self._get_session()
        
        try:
            logger.debug(f"{self.marketplace_name}: {method} {url}")
            
            async with session.request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                json=json_data
            ) as response:
                
                # Check status code
                if response.status != 200:
                    logger.warning(
                        f"{self.marketplace_name} API returned status {response.status}"
                    )
                    return None
                
                # Parse JSON
                data = await response.json()
                logger.debug(f"{self.marketplace_name}: Request successful")
                return data
                
        except asyncio.TimeoutError:
            logger.warning(f"{self.marketplace_name}: Request timeout after {self.timeout}s")
            return None
            
        except aiohttp.ClientError as e:
            logger.error(f"{self.marketplace_name}: Client error - {e}")
            return None
            
        except Exception as e:
            logger.error(f"{self.marketplace_name}: Unexpected error - {e}", exc_info=True)
            return None
    
    def _create_search_result(
        self,
        query: str,
        products: list[Product],
        search_time: float
    ) -> SearchResult:
        """
        Create a SearchResult object.
        
        Args:
            query: Original search query
            products: List of products found
            search_time: Time taken to search
            
        Returns:
            SearchResult: Search result object
        """
        return SearchResult(
            query=query,
            products=products,
            total_results=len(products),
            search_time=search_time,
            timestamp=datetime.now()
        )
    
    def _normalize_query(self, query: str) -> str:
        """
        Normalize search query.
        
        Args:
            query: Original query
            
        Returns:
            str: Normalized query
        """
        # Remove extra whitespace
        normalized = " ".join(query.split())
        
        # Convert to lowercase for API (some APIs are case-sensitive)
        # We'll keep original case for now, can adjust per marketplace
        
        return normalized.strip()
    
    def _generate_affiliate_link(self, original_url: str) -> str:
        """
        Generate affiliate link from original product URL.
        
        Args:
            original_url: Original product URL
            
        Returns:
            str: Affiliate link (or original if not implemented)
        """
        # Default implementation returns original URL
        # Override in subclasses to add affiliate parameters
        return original_url
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
