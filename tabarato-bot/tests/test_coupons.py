"""
Unit tests for coupon models and service.
"""

import pytest
from datetime import datetime, timedelta
from src.models.coupon import Coupon
from src.services.coupon_service import CouponService


class TestCoupon:
    """Tests for Coupon model."""
    
    def test_create_percentage_coupon(self):
        """Test creating percentage coupon."""
        now = datetime.now()
        
        coupon = Coupon(
            code="TEST10",
            marketplace="Test Store",
            discount_type="percentage",
            discount_value=10.0,
            valid_from=now,
            valid_until=now + timedelta(days=30)
        )
        
        assert coupon.code == "TEST10"
        assert coupon.discount_type == "percentage"
        assert coupon.discount_value == 10.0
    
    def test_create_fixed_coupon(self):
        """Test creating fixed discount coupon."""
        now = datetime.now()
        
        coupon = Coupon(
            code="SAVE50",
            marketplace="Test Store",
            discount_type="fixed",
            discount_value=50.0,
            valid_from=now,
            valid_until=now + timedelta(days=30)
        )
        
        assert coupon.discount_type == "fixed"
        assert coupon.discount_value == 50.0
    
    def test_is_valid(self):
        """Test coupon validity check."""
        now = datetime.now()
        
        coupon = Coupon(
            code="VALID",
            marketplace="Test",
            discount_type="percentage",
            discount_value=10.0,
            valid_from=now - timedelta(days=1),
            valid_until=now + timedelta(days=1)
        )
        
        assert coupon.is_valid() is True
    
    def test_is_expired(self):
        """Test expired coupon."""
        now = datetime.now()
        
        coupon = Coupon(
            code="EXPIRED",
            marketplace="Test",
            discount_type="percentage",
            discount_value=10.0,
            valid_from=now - timedelta(days=30),
            valid_until=now - timedelta(days=1),
            is_active=True
        )
        
        assert coupon.is_valid() is False
    
    def test_calculate_percentage_discount(self):
        """Test percentage discount calculation."""
        now = datetime.now()
        
        coupon = Coupon(
            code="PERCENT20",
            marketplace="Test",
            discount_type="percentage",
            discount_value=20.0,
            valid_from=now,
            valid_until=now + timedelta(days=30)
        )
        
        discount = coupon.calculate_discount(1000.0)
        assert discount == 200.0  # 20% of 1000
    
    def test_calculate_fixed_discount(self):
        """Test fixed discount calculation."""
        now = datetime.now()
        
        coupon = Coupon(
            code="FIXED50",
            marketplace="Test",
            discount_type="fixed",
            discount_value=50.0,
            valid_from=now,
            valid_until=now + timedelta(days=30)
        )
        
        discount = coupon.calculate_discount(1000.0)
        assert discount == 50.0
    
    def test_minimum_purchase(self):
        """Test minimum purchase requirement."""
        now = datetime.now()
        
        coupon = Coupon(
            code="MIN500",
            marketplace="Test",
            discount_type="percentage",
            discount_value=10.0,
            valid_from=now,
            valid_until=now + timedelta(days=30),
            minimum_purchase=500.0
        )
        
        # Below minimum
        assert coupon.can_apply_to_price(400.0) is False
        
        # Above minimum
        assert coupon.can_apply_to_price(600.0) is True
    
    def test_maximum_discount(self):
        """Test maximum discount limit."""
        now = datetime.now()
        
        coupon = Coupon(
            code="MAX100",
            marketplace="Test",
            discount_type="percentage",
            discount_value=20.0,
            valid_from=now,
            valid_until=now + timedelta(days=30),
            maximum_discount=100.0
        )
        
        # 20% of 1000 = 200, but max is 100
        discount = coupon.calculate_discount(1000.0)
        assert discount == 100.0
    
    def test_apply_to_price(self):
        """Test applying coupon to price."""
        now = datetime.now()
        
        coupon = Coupon(
            code="APPLY10",
            marketplace="Test",
            discount_type="percentage",
            discount_value=10.0,
            valid_from=now,
            valid_until=now + timedelta(days=30)
        )
        
        final_price = coupon.apply_to_price(1000.0)
        assert final_price == 900.0  # 1000 - 100


class TestCouponService:
    """Tests for CouponService."""
    
    def test_get_active_coupons(self):
        """Test getting active coupons."""
        service = CouponService()
        active = service.get_active_coupons()
        
        assert len(active) > 0
        assert all(c.is_valid() for c in active)
    
    def test_get_coupons_for_marketplace(self):
        """Test getting coupons for specific marketplace."""
        service = CouponService()
        ml_coupons = service.get_coupons_for_marketplace("Mercado Livre")
        
        assert len(ml_coupons) > 0
        assert all(c.marketplace == "Mercado Livre" for c in ml_coupons)
    
    def test_find_best_coupon(self):
        """Test finding best coupon."""
        service = CouponService()
        
        # Find best coupon for Mercado Livre with price 1000
        best = service.find_best_coupon("Mercado Livre", 1000.0)
        
        assert best is not None
        assert best.marketplace == "Mercado Livre"
    
    def test_apply_best_coupon(self):
        """Test applying best coupon."""
        service = CouponService()
        
        result = service.apply_best_coupon("Mercado Livre", 1000.0)
        
        assert 'original_price' in result
        assert 'final_price' in result
        assert 'discount' in result
        assert result['original_price'] == 1000.0
        
        if result['coupon_applied']:
            assert result['final_price'] < result['original_price']
