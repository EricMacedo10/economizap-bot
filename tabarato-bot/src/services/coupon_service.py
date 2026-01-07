"""
Coupon service for managing discount coupons.
"""

from typing import List, Optional, Dict
from datetime import datetime, timedelta

from src.models.coupon import Coupon
from src.utils.logger import get_logger

logger = get_logger(__name__)


class CouponService:
    """
    Service for managing and applying coupons.
    """
    
    def __init__(self):
        """Initialize coupon service."""
        # In-memory coupon storage (will be replaced with database in Phase 5)
        self._coupons: List[Coupon] = []
        
        # Load initial coupons
        self._load_default_coupons()
        
        logger.info(f"Coupon service initialized with {len(self._coupons)} coupons")
    
    def _load_default_coupons(self) -> None:
        """Load default coupons for testing."""
        # These are example coupons - in production, these would come from database
        now = datetime.now()
        
        default_coupons = [
            # Mercado Livre coupons
            Coupon(
                code="TECH10",
                marketplace="Mercado Livre",
                discount_type="percentage",
                discount_value=10.0,
                valid_from=now - timedelta(days=30),
                valid_until=now + timedelta(days=30),
                minimum_purchase=500.0,
                maximum_discount=100.0,
                description="10% off em tecnologia (mín R$ 500)"
            ),
            Coupon(
                code="FRETEGRATIS",
                marketplace="Mercado Livre",
                discount_type="fixed",
                discount_value=0.0,  # Free shipping
                valid_from=now - timedelta(days=30),
                valid_until=now + timedelta(days=30),
                description="Frete grátis"
            ),
            
            # Amazon coupons
            Coupon(
                code="PRIME15",
                marketplace="Amazon",
                discount_type="percentage",
                discount_value=15.0,
                valid_from=now - timedelta(days=30),
                valid_until=now + timedelta(days=30),
                minimum_purchase=300.0,
                maximum_discount=150.0,
                description="15% off para Prime (mín R$ 300)"
            ),
            
            # Shopee coupons
            Coupon(
                code="SHOPEE20",
                marketplace="Shopee",
                discount_type="percentage",
                discount_value=20.0,
                valid_from=now - timedelta(days=30),
                valid_until=now + timedelta(days=30),
                minimum_purchase=200.0,
                maximum_discount=50.0,
                description="20% off (mín R$ 200)"
            ),
            
            # AliExpress coupons
            Coupon(
                code="ALI50",
                marketplace="AliExpress",
                discount_type="fixed",
                discount_value=50.0,
                valid_from=now - timedelta(days=30),
                valid_until=now + timedelta(days=30),
                minimum_purchase=400.0,
                description="R$ 50 off (mín R$ 400)"
            ),
        ]
        
        self._coupons.extend(default_coupons)
    
    def get_all_coupons(self) -> List[Coupon]:
        """
        Get all coupons.
        
        Returns:
            List[Coupon]: All coupons
        """
        return self._coupons.copy()
    
    def get_active_coupons(self) -> List[Coupon]:
        """
        Get all currently active coupons.
        
        Returns:
            List[Coupon]: Active coupons
        """
        return [coupon for coupon in self._coupons if coupon.is_valid()]
    
    def get_coupons_for_marketplace(self, marketplace: str) -> List[Coupon]:
        """
        Get active coupons for a specific marketplace.
        
        Args:
            marketplace: Marketplace name
            
        Returns:
            List[Coupon]: Active coupons for marketplace
        """
        return [
            coupon for coupon in self._coupons
            if coupon.marketplace.lower() == marketplace.lower() and coupon.is_valid()
        ]
    
    def find_best_coupon(
        self,
        marketplace: str,
        price: float,
        category: Optional[str] = None
    ) -> Optional[Coupon]:
        """
        Find the best coupon for a product.
        
        Args:
            marketplace: Marketplace name
            price: Product price
            category: Product category (optional)
            
        Returns:
            Optional[Coupon]: Best coupon or None
        """
        # Get applicable coupons
        coupons = self.get_coupons_for_marketplace(marketplace)
        
        # Filter by price and category
        applicable = [
            coupon for coupon in coupons
            if coupon.can_apply_to_price(price)
        ]
        
        if category:
            # Filter by category if specified
            applicable = [
                coupon for coupon in applicable
                if not coupon.categories or category in coupon.categories
            ]
        
        if not applicable:
            return None
        
        # Find coupon with maximum discount
        best_coupon = max(
            applicable,
            key=lambda c: c.calculate_discount(price)
        )
        
        logger.debug(
            f"Found best coupon for {marketplace}: {best_coupon.code} "
            f"(saves R$ {best_coupon.calculate_discount(price):.2f})"
        )
        
        return best_coupon
    
    def apply_best_coupon(
        self,
        marketplace: str,
        price: float,
        category: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Apply best coupon to a price.
        
        Args:
            marketplace: Marketplace name
            price: Original price
            category: Product category (optional)
            
        Returns:
            Dict: Result with final_price, discount, coupon_code
        """
        best_coupon = self.find_best_coupon(marketplace, price, category)
        
        if not best_coupon:
            return {
                'original_price': price,
                'final_price': price,
                'discount': 0.0,
                'coupon_code': None,
                'coupon_applied': False
            }
        
        discount = best_coupon.calculate_discount(price)
        final_price = best_coupon.apply_to_price(price)
        
        return {
            'original_price': price,
            'final_price': final_price,
            'discount': discount,
            'coupon_code': best_coupon.code,
            'coupon_applied': True,
            'discount_percentage': (discount / price * 100) if price > 0 else 0
        }
    
    def add_coupon(self, coupon: Coupon) -> None:
        """
        Add a new coupon.
        
        Args:
            coupon: Coupon to add
        """
        self._coupons.append(coupon)
        logger.info(f"Added coupon: {coupon.code} for {coupon.marketplace}")
    
    def remove_coupon(self, code: str, marketplace: str) -> bool:
        """
        Remove a coupon.
        
        Args:
            code: Coupon code
            marketplace: Marketplace name
            
        Returns:
            bool: True if removed, False if not found
        """
        for i, coupon in enumerate(self._coupons):
            if (coupon.code.lower() == code.lower() and
                coupon.marketplace.lower() == marketplace.lower()):
                del self._coupons[i]
                logger.info(f"Removed coupon: {code} for {marketplace}")
                return True
        
        return False
    
    def cleanup_expired_coupons(self) -> int:
        """
        Remove expired coupons.
        
        Returns:
            int: Number of coupons removed
        """
        initial_count = len(self._coupons)
        self._coupons = [c for c in self._coupons if c.is_valid()]
        removed = initial_count - len(self._coupons)
        
        if removed > 0:
            logger.info(f"Cleaned up {removed} expired coupons")
        
        return removed


# Global coupon service instance
_coupon_service: Optional[CouponService] = None


def get_coupon_service() -> CouponService:
    """
    Get the global coupon service instance.
    
    Returns:
        CouponService: Global coupon service
    """
    global _coupon_service
    
    if _coupon_service is None:
        _coupon_service = CouponService()
    
    return _coupon_service
