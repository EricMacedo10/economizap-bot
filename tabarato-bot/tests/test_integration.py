"""
Integration tests for search service.
"""

import pytest
from src.services.search_service import SearchService


@pytest.mark.asyncio
class TestSearchServiceIntegration:
    """Integration tests for SearchService."""
    
    async def test_search_all_marketplaces(self):
        """Test searching all marketplaces."""
        service = SearchService()
        
        result = await service.search_all("notebook")
        
        # Should have results from multiple marketplaces
        assert result is not None
        assert result.query == "notebook"
        assert result.total_results > 0
        
        # Should have products from different marketplaces
        marketplaces = {p.marketplace for p in result.products}
        assert len(marketplaces) >= 2  # At least 2 marketplaces
        
        # Should have best price
        assert result.best_price is not None
        assert result.best_price.price > 0
    
    async def test_search_with_coupons(self):
        """Test that coupons are applied."""
        service = SearchService()
        
        result = await service.search_all("smartphone")
        
        # Some products should have coupons applied
        products_with_coupons = [
            p for p in result.products 
            if p.coupon_code is not None
        ]
        
        # At least some products should have coupons
        assert len(products_with_coupons) > 0
    
    async def test_search_performance(self):
        """Test search performance."""
        service = SearchService()
        
        result = await service.search_all("mouse")
        
        # Should complete in reasonable time (< 10 seconds)
        assert result.search_time < 10.0
        
        # Should return multiple results
        assert result.total_results >= 5
    
    async def test_empty_query(self):
        """Test search with empty query."""
        service = SearchService()
        
        result = await service.search_all("")
        
        # Should handle gracefully
        assert result is not None
        assert result.total_results == 0
    
    async def test_no_results_query(self):
        """Test search with query that returns no results."""
        service = SearchService()
        
        result = await service.search_all("xyzabc123notfound999")
        
        # Should handle gracefully
        assert result is not None
        # May have 0 results or mock results depending on implementation
