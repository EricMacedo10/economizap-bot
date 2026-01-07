"""
Mock data generator for testing marketplace integrations.
Generates realistic product data without requiring real API credentials.
"""

import random
from typing import List, Dict, Any
from datetime import datetime

from src.utils.logger import get_logger

logger = get_logger(__name__)


class MockDataGenerator:
    """
    Generates realistic mock product data for testing.
    """
    
    # Product categories with typical price ranges (in BRL)
    PRODUCT_CATEGORIES = {
        'notebook': (2000, 8000),
        'laptop': (2000, 8000),
        'computador': (1500, 6000),
        'iphone': (3000, 8000),
        'smartphone': (800, 5000),
        'celular': (800, 5000),
        'tablet': (800, 3000),
        'monitor': (500, 3000),
        'teclado': (50, 500),
        'mouse': (30, 300),
        'headset': (100, 800),
        'fone': (50, 1000),
        'tv': (1000, 8000),
        'smart tv': (1500, 10000),
        'console': (2000, 4000),
        'playstation': (2500, 4500),
        'xbox': (2000, 4000),
        'camera': (800, 5000),
        'impressora': (300, 2000),
        'roteador': (100, 800),
        'ssd': (200, 1500),
        'hd': (200, 1000),
        'memoria': (150, 800),
        'placa': (500, 3000),
    }
    
    # Brand variations
    BRANDS = {
        'notebook': ['Dell', 'Lenovo', 'Acer', 'Asus', 'HP', 'Samsung'],
        'smartphone': ['Samsung', 'Xiaomi', 'Motorola', 'Apple', 'Realme'],
        'tv': ['Samsung', 'LG', 'Sony', 'TCL', 'Philips'],
        'monitor': ['Dell', 'LG', 'Samsung', 'AOC', 'Asus'],
    }
    
    # Specs variations
    SPECS = {
        'ram': ['4GB', '8GB', '16GB', '32GB'],
        'storage': ['128GB', '256GB', '512GB', '1TB', '2TB'],
        'processor': ['i3', 'i5', 'i7', 'i9', 'Ryzen 5', 'Ryzen 7'],
        'screen': ['13.3"', '14"', '15.6"', '17"', '24"', '27"', '32"', '43"', '50"', '55"', '65"'],
    }
    
    @staticmethod
    def get_base_price(query: str) -> float:
        """
        Get base price for a query.
        
        Args:
            query: Search query
            
        Returns:
            float: Base price in BRL
        """
        query_lower = query.lower()
        
        # Check each category
        for category, (min_price, max_price) in MockDataGenerator.PRODUCT_CATEGORIES.items():
            if category in query_lower:
                # Return middle of range
                return (min_price + max_price) / 2
        
        # Default price if category not found
        return 500.0
    
    @staticmethod
    def generate_product_name(query: str, index: int = 0) -> str:
        """
        Generate realistic product name based on query.
        
        Args:
            query: Search query
            index: Product index for variation
            
        Returns:
            str: Generated product name
        """
        query_lower = query.lower()
        
        # Determine category
        category = None
        for cat in MockDataGenerator.PRODUCT_CATEGORIES.keys():
            if cat in query_lower:
                category = cat
                break
        
        if not category:
            category = 'produto'
        
        # Get brand if available
        brand = ''
        if category in MockDataGenerator.BRANDS:
            brand = random.choice(MockDataGenerator.BRANDS[category])
        
        # Build name
        name_parts = []
        
        if brand:
            name_parts.append(brand)
        
        name_parts.append(query.title())
        
        # Add specs for tech products
        if category in ['notebook', 'laptop', 'computador']:
            processor = random.choice(MockDataGenerator.SPECS['processor'])
            ram = random.choice(MockDataGenerator.SPECS['ram'])
            storage = random.choice(MockDataGenerator.SPECS['storage'])
            name_parts.append(f"{processor} {ram} {storage}")
        
        elif category in ['smartphone', 'celular', 'iphone']:
            storage = random.choice(['64GB', '128GB', '256GB', '512GB'])
            name_parts.append(storage)
        
        elif category in ['tv', 'smart tv', 'monitor']:
            screen = random.choice(MockDataGenerator.SPECS['screen'])
            name_parts.append(screen)
        
        # Add model variation
        if index > 0:
            name_parts.append(f"- Modelo {index + 1}")
        
        return ' '.join(name_parts)
    
    @staticmethod
    def generate_price(base_price: float, marketplace: str) -> float:
        """
        Generate price with marketplace-specific variation.
        
        Args:
            base_price: Base price
            marketplace: Marketplace name
            
        Returns:
            float: Generated price
        """
        # Different marketplaces have different price ranges
        variations = {
            'Amazon': (0.95, 1.15),
            'Mercado Livre': (0.90, 1.10),
            'Shopee': (0.85, 1.05),
            'AliExpress': (0.70, 0.95),
        }
        
        min_var, max_var = variations.get(marketplace, (0.90, 1.10))
        variation = random.uniform(min_var, max_var)
        
        price = base_price * variation
        
        # Round to .90 or .99 (common pricing)
        if random.random() > 0.5:
            price = int(price) + 0.90
        else:
            price = int(price) + 0.99
        
        return round(price, 2)
    
    @staticmethod
    def generate_image_url(marketplace: str, product_id: str) -> str:
        """
        Generate placeholder image URL.
        
        Args:
            marketplace: Marketplace name
            product_id: Product ID
            
        Returns:
            str: Image URL
        """
        # Use placeholder image service
        return f"https://via.placeholder.com/300x300.png?text={marketplace}+Product"
    
    @staticmethod
    def should_have_discount() -> bool:
        """
        Randomly determine if product should have discount.
        
        Returns:
            bool: True if should have discount (30% chance)
        """
        return random.random() < 0.3
    
    @staticmethod
    def generate_discount_percentage() -> float:
        """
        Generate discount percentage.
        
        Returns:
            float: Discount percentage (5-40%)
        """
        return round(random.uniform(5, 40), 0)
    
    @staticmethod
    def generate_rating() -> float:
        """
        Generate product rating.
        
        Returns:
            float: Rating (3.5-5.0)
        """
        return round(random.uniform(3.5, 5.0), 1)
    
    @staticmethod
    def generate_review_count() -> int:
        """
        Generate review count.
        
        Returns:
            int: Number of reviews
        """
        return random.randint(10, 5000)
    
    @staticmethod
    def generate_mock_products(
        query: str,
        marketplace: str,
        count: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple mock products.
        
        Args:
            query: Search query
            marketplace: Marketplace name
            count: Number of products to generate
            
        Returns:
            List[Dict]: List of mock product data
        """
        base_price = MockDataGenerator.get_base_price(query)
        products = []
        
        for i in range(count):
            # Generate product data
            product_id = f"{marketplace[:3].upper()}{random.randint(100000, 999999)}"
            name = MockDataGenerator.generate_product_name(query, i)
            price = MockDataGenerator.generate_price(base_price, marketplace)
            
            # Discount
            original_price = None
            if MockDataGenerator.should_have_discount():
                discount_pct = MockDataGenerator.generate_discount_percentage()
                original_price = price / (1 - discount_pct / 100)
                original_price = round(original_price, 2)
            
            product = {
                'id': product_id,
                'name': name,
                'price': price,
                'original_price': original_price,
                'image_url': MockDataGenerator.generate_image_url(marketplace, product_id),
                'rating': MockDataGenerator.generate_rating(),
                'review_count': MockDataGenerator.generate_review_count(),
            }
            
            products.append(product)
        
        logger.debug(f"Generated {count} mock products for {marketplace}")
        
        return products
