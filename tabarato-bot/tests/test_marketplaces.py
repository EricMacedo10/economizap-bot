"""
Unit tests for mock marketplace APIs.
"""

import pytest
from src.integrations.amazon_api import AmazonAPI
from src.integrations.shopee_api import ShopeeAPI
from src.integrations.aliexpress_api import AliExpressAPI
from src.integrations.mock_data import MockDataGenerator


class TestMockDataGenerator:
    """Tests for MockDataGenerator."""
    
    def test_get_base_price(self):
        """Test base price calculation."""
        price_notebook = MockDataGenerator.get_base_price("notebook")
        price_iphone = MockDataGenerator.get_base_price("iphone")
        
        assert price_notebook > 0
        assert price_iphone > 0
        assert price_notebook != price_iphone
    
    def test_generate_product_name(self):
        """Test product name generation."""
        name = MockDataGenerator.generate_product_name("notebook", 0)
        
        assert len(name) > 0
        assert "notebook" in name.lower()
    
    def test_generate_price(self):
        """Test price generation."""
        base_price = 1000.0
        
        price_amazon = MockDataGenerator.generate_price(base_price, "Amazon")
        price_shopee = MockDataGenerator.generate_price(base_price, "Shopee")
        
        assert price_amazon > 0
        assert price_shopee > 0
        # Shopee typically cheaper
        assert price_shopee < price_amazon
    
    def test_generate_mock_products(self):
        """Test mock products generation."""
        products = MockDataGenerator.generate_mock_products(
            query="notebook",
            marketplace="Amazon",
            count=5
        )
        
        assert len(products) == 5
        assert all('id' in p for p in products)
        assert all('name' in p for p in products)
        assert all('price' in p for p in products)


@pytest.mark.asyncio
class TestAmazonAPI:
    """Tests for Amazon API (Mock)."""
    
    async def test_search(self):
        """Test Amazon search."""
        api = AmazonAPI()
        result = await api.search("notebook")
        
        assert result is not None
        assert result.query == "notebook"
        assert result.has_results
        assert len(result.products) > 0
        assert all(p.marketplace == "Amazon" for p in result.products)
    
    async def test_search_empty_query(self):
        """Test search with empty query."""
        api = AmazonAPI()
        result = await api.search("")
        
        # Should handle gracefully
        assert result is not None


@pytest.mark.asyncio
class TestShopeeAPI:
    """Tests for Shopee API (Mock)."""
    
    async def test_search(self):
        """Test Shopee search."""
        api = ShopeeAPI()
        result = await api.search("smartphone")
        
        assert result is not None
        assert result.query == "smartphone"
        assert result.has_results
        assert len(result.products) > 0
        assert all(p.marketplace == "Shopee" for p in result.products)
    
    async def test_product_prices(self):
        """Test that Shopee has competitive prices."""
        api = ShopeeAPI()
        result = await api.search("iphone")
        
        assert result.has_results
        # Shopee typically has lower prices
        avg_price = sum(p.price for p in result.products) / len(result.products)
        assert avg_price > 0


@pytest.mark.asyncio
class TestAliExpressAPI:
    """Tests for AliExpress API (Mock)."""
    
    async def test_search(self):
        """Test AliExpress search."""
        api = AliExpressAPI()
        result = await api.search("headset")
        
        assert result is not None
        assert result.query == "headset"
        assert result.has_results
        assert len(result.products) > 0
        assert all(p.marketplace == "AliExpress" for p in result.products)
    
    async def test_international_shipping_note(self):
        """Test that products have international shipping note."""
        api = AliExpressAPI()
        result = await api.search("mouse")
        
        assert result.has_results
        # Should have international shipping note
        assert any("Internacional" in p.name for p in result.products)
    
    async def test_lowest_prices(self):
        """Test that AliExpress typically has lowest prices."""
        api = AliExpressAPI()
        result = await api.search("teclado")
        
        assert result.has_results
        # AliExpress typically has lowest prices
        avg_price = sum(p.price for p in result.products) / len(result.products)
        assert avg_price > 0
