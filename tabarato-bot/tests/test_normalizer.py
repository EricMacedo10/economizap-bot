"""
Unit tests for normalizer utilities.
"""

import pytest
from src.utils.normalizer import ProductNormalizer, group_similar_products
from src.models.product import Product


class TestProductNormalizer:
    """Tests for ProductNormalizer."""
    
    def test_normalize_text(self):
        """Test text normalization."""
        text = "Notebook DELL Inspiron 15 - i5 8GB"
        normalized = ProductNormalizer.normalize_text(text)
        
        assert normalized == "notebook dell inspiron 15 i5 8gb"
        assert "DELL" not in normalized
        assert "-" not in normalized
    
    def test_remove_accents(self):
        """Test accent removal."""
        text = "Computação Móvel Açúcar"
        normalized = ProductNormalizer.normalize_text(text)
        
        assert "ç" not in normalized
        assert "ã" not in normalized
        assert "ó" not in normalized
        assert "ú" not in normalized
    
    def test_extract_keywords(self):
        """Test keyword extraction."""
        text = "Notebook Dell Inspiron 15 com i5 e 8GB de RAM"
        keywords = ProductNormalizer.extract_keywords(text)
        
        assert "notebook" in keywords
        assert "dell" in keywords
        assert "inspiron" in keywords
        assert "i5" in keywords
        assert "8gb" in keywords
        
        # Stop words should be removed
        assert "com" not in keywords
        assert "de" not in keywords
    
    def test_calculate_similarity(self):
        """Test similarity calculation."""
        text1 = "Notebook Dell Inspiron 15 i5 8GB"
        text2 = "DELL INSPIRON 15 NOTEBOOK INTEL i5 8GB RAM"
        
        similarity = ProductNormalizer.calculate_similarity(text1, text2)
        
        assert similarity > 70.0  # Should be very similar
        assert similarity <= 100.0
    
    def test_are_similar(self):
        """Test similarity check."""
        text1 = "iPhone 13 128GB Azul"
        text2 = "Apple iPhone 13 128GB Blue"
        
        # Should be similar (same product, different language)
        assert ProductNormalizer.are_similar(text1, text2, threshold=50.0)
    
    def test_are_not_similar(self):
        """Test dissimilar products."""
        text1 = "Notebook Dell"
        text2 = "iPhone 13"
        
        # Should not be similar
        assert not ProductNormalizer.are_similar(text1, text2, threshold=70.0)
    
    def test_extract_specs_ram(self):
        """Test RAM extraction."""
        text = "Notebook com 16GB de RAM"
        specs = ProductNormalizer.extract_specs(text)
        
        assert 'ram' in specs
        assert specs['ram'] == "16gb"
    
    def test_extract_specs_storage(self):
        """Test storage extraction."""
        text = "SSD 512GB NVMe"
        specs = ProductNormalizer.extract_specs(text)
        
        assert 'storage' in specs
        assert specs['storage'] == "512gb"
    
    def test_extract_specs_processor(self):
        """Test processor extraction."""
        text = "Notebook Intel Core i7"
        specs = ProductNormalizer.extract_specs(text)
        
        assert 'processor' in specs
        assert 'i7' in specs['processor']
    
    def test_extract_specs_screen(self):
        """Test screen size extraction."""
        text = "Monitor 27 polegadas"
        specs = ProductNormalizer.extract_specs(text)
        
        assert 'screen' in specs
        assert '27' in specs['screen']


class TestGroupSimilarProducts:
    """Tests for product grouping."""
    
    def test_group_similar_products(self):
        """Test grouping similar products."""
        products = [
            Product(
                id="1",
                name="Notebook Dell Inspiron 15 i5 8GB",
                price=2999.90,
                marketplace="Mercado Livre",
                url="https://test.com/1"
            ),
            Product(
                id="2",
                name="DELL INSPIRON 15 NOTEBOOK i5 8GB RAM",
                price=3199.90,
                marketplace="Amazon",
                url="https://test.com/2"
            ),
            Product(
                id="3",
                name="iPhone 13 128GB",
                price=4999.90,
                marketplace="Shopee",
                url="https://test.com/3"
            )
        ]
        
        groups = group_similar_products(products, threshold=70.0)
        
        # Should create 2 groups (2 Dell notebooks + 1 iPhone)
        assert len(groups) == 2
        
        # First group should have 2 Dell notebooks
        dell_group = [g for g in groups if len(g) == 2]
        assert len(dell_group) == 1
        
        # Second group should have 1 iPhone
        iphone_group = [g for g in groups if len(g) == 1]
        assert len(iphone_group) == 1
    
    def test_group_empty_list(self):
        """Test grouping empty list."""
        groups = group_similar_products([])
        assert groups == []
    
    def test_group_single_product(self):
        """Test grouping single product."""
        products = [
            Product(
                id="1",
                name="Test Product",
                price=100.0,
                marketplace="Test",
                url="https://test.com"
            )
        ]
        
        groups = group_similar_products(products)
        assert len(groups) == 1
        assert len(groups[0]) == 1
