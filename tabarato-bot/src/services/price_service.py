"""
Price comparison service for EconomiZap Bot.
"""Compares prices across products and applies coupons.
"""

from typing import List, Optional, Dict, Tuple
from datetime import datetime

from src.models.product import Product, SearchResult
from src.services.coupon_service import get_coupon_service
from src.utils.normalizer import ProductNormalizer, group_similar_products
from src.utils.logger import get_logger
from src.config import Config

logger = get_logger(__name__)


class PriceService:
    """
    Service for comparing prices and finding best deals.
    """
    
    def __init__(self):
        """Initialize price service."""
        self.coupon_service = get_coupon_service()
        self.similarity_threshold = Config.SIMILARITY_THRESHOLD
        
        logger.info("Price service initialized")
    
    def compare_prices(self, search_result: SearchResult) -> SearchResult:
        """
        Compare prices and apply coupons to search results.
        
        Args:
            search_result: Original search results
            
        Returns:
            SearchResult: Enhanced results with coupons applied
        """
        if not search_result.has_results:
            return search_result
        
        logger.info(f"Comparing prices for {len(search_result.products)} products")
        
        # Apply coupons to all products
        enhanced_products = []
        
        for product in search_result.products:
            enhanced_product = self._apply_coupon_to_product(product)
            enhanced_products.append(enhanced_product)
        
        # Create new search result with enhanced products
        enhanced_result = SearchResult(
            query=search_result.query,
            products=enhanced_products,
            total_results=len(enhanced_products),
            search_time=search_result.search_time,
            timestamp=search_result.timestamp
        )
        
        logger.info(
            f"Price comparison complete. Best price: "
            f"R$ {enhanced_result.best_price.final_price:.2f}"
            if enhanced_result.best_price else "No products"
        )
        
        return enhanced_result
    
    def _apply_coupon_to_product(self, product: Product) -> Product:
        """
        Apply best coupon to a product.
        
        Args:
            product: Original product
            
        Returns:
            Product: Product with coupon applied
        """
        # Find best coupon
        coupon_result = self.coupon_service.apply_best_coupon(
            marketplace=product.marketplace,
            price=product.price
        )
        
        if not coupon_result['coupon_applied']:
            return product
        
        # Create new product with coupon applied
        enhanced_product = Product(
            id=product.id,
            name=product.name,
            price=coupon_result['final_price'],
            original_price=coupon_result['original_price'],
            marketplace=product.marketplace,
            url=product.url,
            image_url=product.image_url,
            coupon_code=coupon_result['coupon_code'],
            discount_percentage=coupon_result['discount_percentage'],
            currency=product.currency,
            timestamp=product.timestamp
        )
        
        logger.debug(
            f"Applied coupon {coupon_result['coupon_code']} to {product.name[:50]}... "
            f"(R$ {product.price:.2f} → R$ {coupon_result['final_price']:.2f})"
        )
        
        return enhanced_product
    
    def find_best_deal(
        self,
        products: List[Product],
        apply_coupons: bool = True
    ) -> Optional[Product]:
        """
        Find the best deal among products.
        
        Args:
            products: List of products
            apply_coupons: Whether to apply coupons
            
        Returns:
            Optional[Product]: Best deal or None
        """
        if not products:
            return None
        
        # Apply coupons if requested
        if apply_coupons:
            products = [self._apply_coupon_to_product(p) for p in products]
        
        # Find product with lowest final price
        best_product = min(products, key=lambda p: p.final_price)
        
        return best_product
    
    def group_and_compare(
        self,
        search_result: SearchResult
    ) -> Dict[str, List[Product]]:
        """
        Group similar products and compare prices within groups.
        
        Args:
            search_result: Search results
            
        Returns:
            Dict: Grouped products with best deal in each group
        """
        if not search_result.has_results:
            return {}
        
        # Group similar products
        groups = group_similar_products(
            search_result.products,
            threshold=self.similarity_threshold
        )
        
        # For each group, find best deal
        result = {}
        
        for i, group in enumerate(groups):
            # Apply coupons to group
            enhanced_group = [
                self._apply_coupon_to_product(p) for p in group
            ]
            
            # Sort by price
            enhanced_group.sort(key=lambda p: p.final_price)
            
            # Use first product name as group key
            group_key = f"group_{i}_{group[0].name[:30]}"
            result[group_key] = enhanced_group
        
        logger.info(f"Created {len(result)} product groups")
        
        return result
    
    def calculate_savings(
        self,
        original_price: float,
        final_price: float
    ) -> Dict[str, float]:
        """
        Calculate savings information.
        
        Args:
            original_price: Original price
            final_price: Final price after discounts
            
        Returns:
            Dict: Savings information
        """
        savings_amount = original_price - final_price
        savings_percentage = (
            (savings_amount / original_price * 100)
            if original_price > 0 else 0
        )
        
        return {
            'original_price': original_price,
            'final_price': final_price,
            'savings_amount': savings_amount,
            'savings_percentage': savings_percentage
        }
    
    def compare_two_products(
        self,
        product1: Product,
        product2: Product
    ) -> Dict[str, any]:
        """
        Compare two products.
        
        Args:
            product1: First product
            product2: Second product
            
        Returns:
            Dict: Comparison result
        """
        # Apply coupons
        p1 = self._apply_coupon_to_product(product1)
        p2 = self._apply_coupon_to_product(product2)
        
        # Calculate similarity
        similarity = ProductNormalizer.calculate_similarity(
            p1.name,
            p2.name
        )
        
        # Determine cheaper product
        if p1.final_price < p2.final_price:
            cheaper = p1
            more_expensive = p2
            price_difference = p2.final_price - p1.final_price
        else:
            cheaper = p2
            more_expensive = p1
            price_difference = p1.final_price - p2.final_price
        
        return {
            'product1': p1,
            'product2': p2,
            'similarity': similarity,
            'are_similar': similarity >= self.similarity_threshold,
            'cheaper_product': cheaper,
            'more_expensive_product': more_expensive,
            'price_difference': price_difference,
            'price_difference_percentage': (
                (price_difference / more_expensive.final_price * 100)
                if more_expensive.final_price > 0 else 0
            )
        }


# Global price service instance
_price_service: Optional[PriceService] = None


def get_price_service() -> PriceService:
    """
    Get the global price service instance.
    
    Returns:
        PriceService: Global price service
    """
    global _price_service
    
    if _price_service is None:
        _price_service = PriceService()
    
    return _price_service
