"""
Unit tests for product models.
"""

import pytest
from datetime import datetime
from src.models.product import Product, SearchResult


class TestProduct:
    """Tests for Product model."""
    
    def test_create_product(self):
        """Test creating a basic product."""
        product = Product(
            id="MLB123456",
            name="Notebook Dell Inspiron 15",
            price=2999.90,
            marketplace="Mercado Livre",
            url="https://mercadolivre.com.br/product/123"
        )
        
        assert product.id == "MLB123456"
        assert product.name == "Notebook Dell Inspiron 15"
        assert product.price == 2999.90
        assert product.marketplace == "Mercado Livre"
        assert product.currency == "BRL"
    
    def test_product_with_discount(self):
        """Test product with discount."""
        product = Product(
            id="MLB123",
            name="Test Product",
            price=1000.00,
            original_price=1500.00,
            marketplace="Mercado Livre",
            url="https://test.com"
        )
        
        assert product.has_discount is True
        assert product.savings == 500.00
        assert product.calculate_discount_percentage() == pytest.approx(33.33, 0.01)
    
    def test_product_without_discount(self):
        """Test product without discount."""
        product = Product(
            id="MLB123",
            name="Test Product",
            price=1000.00,
            marketplace="Mercado Livre",
            url="https://test.com"
        )
        
        assert product.has_discount is False
        assert product.savings == 0.0
        assert product.calculate_discount_percentage() == 0.0
    
    def test_format_price(self):
        """Test price formatting."""
        product = Product(
            id="MLB123",
            name="Test",
            price=1299.90,
            marketplace="Mercado Livre",
            url="https://test.com"
        )
        
        formatted = product.format_price()
        assert "1.299,90" in formatted
        assert "R$" in formatted


class TestSearchResult:
    """Tests for SearchResult model."""
    
    def test_create_search_result(self):
        """Test creating a search result."""
        products = [
            Product(
                id="1",
                name="Product 1",
                price=100.00,
                marketplace="Mercado Livre",
                url="https://test.com/1"
            ),
            Product(
                id="2",
                name="Product 2",
                price=200.00,
                marketplace="Mercado Livre",
                url="https://test.com/2"
            )
        ]
        
        result = SearchResult(
            query="test",
            products=products,
            total_results=2,
            search_time=1.5
        )
        
        assert result.query == "test"
        assert len(result.products) == 2
        assert result.total_results == 2
        assert result.has_results is True
    
    def test_best_price(self):
        """Test getting product with best price."""
        products = [
            Product(
                id="1",
                name="Expensive",
                price=500.00,
                marketplace="Mercado Livre",
                url="https://test.com/1"
            ),
            Product(
                id="2",
                name="Cheap",
                price=100.00,
                marketplace="Mercado Livre",
                url="https://test.com/2"
            ),
            Product(
                id="3",
                name="Medium",
                price=300.00,
                marketplace="Mercado Livre",
                url="https://test.com/3"
            )
        ]
        
        result = SearchResult(
            query="test",
            products=products
        )
        
        best = result.best_price
        assert best is not None
        assert best.price == 100.00
        assert best.name == "Cheap"
    
    def test_empty_search_result(self):
        """Test empty search result."""
        result = SearchResult(
            query="test",
            products=[]
        )
        
        assert result.has_results is False
        assert result.best_price is None
