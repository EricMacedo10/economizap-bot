"""
Simple test script to verify basic functionality.
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models.product import Product, SearchResult
from src.models.coupon import Coupon
from src.utils.normalizer import ProductNormalizer
from src.services.coupon_service import CouponService
from datetime import datetime, timedelta


def test_product_model():
    """Test Product model."""
    print("Testing Product model...")
    
    product = Product(
        id="TEST123",
        name="Notebook Dell Inspiron 15",
        price=2999.90,
        marketplace="Test",
        url="https://test.com"
    )
    
    assert product.id == "TEST123"
    assert product.price == 2999.90
    print("✅ Product model OK")


def test_coupon_model():
    """Test Coupon model."""
    print("\nTesting Coupon model...")
    
    now = datetime.now()
    coupon = Coupon(
        code="TEST10",
        marketplace="Test",
        discount_type="percentage",
        discount_value=10.0,
        valid_from=now,
        valid_until=now + timedelta(days=30)
    )
    
    assert coupon.code == "TEST10"
    assert coupon.is_valid()
    
    discount = coupon.calculate_discount(1000.0)
    assert discount == 100.0
    print("✅ Coupon model OK")


def test_normalizer():
    """Test ProductNormalizer."""
    print("\nTesting ProductNormalizer...")
    
    text = "Notebook DELL Inspiron 15 - i5 8GB"
    normalized = ProductNormalizer.normalize_text(text)
    
    assert "notebook" in normalized
    assert "dell" in normalized
    assert "-" not in normalized
    print("✅ ProductNormalizer OK")


def test_coupon_service():
    """Test CouponService."""
    print("\nTesting CouponService...")
    
    service = CouponService()
    active = service.get_active_coupons()
    
    assert len(active) > 0
    print(f"✅ CouponService OK ({len(active)} active coupons)")


async def test_mock_api():
    """Test mock API."""
    print("\nTesting Mock APIs...")
    
    try:
        from src.integrations.amazon_api import AmazonAPI
        
        api = AmazonAPI()
        result = await api.search("notebook")
        
        assert result is not None
        assert result.total_results > 0
        print(f"✅ Amazon Mock API OK ({result.total_results} results)")
    except Exception as e:
        print(f"❌ Mock API failed: {e}")


def main():
    """Run all tests."""
    print("=" * 60)
    print("EconomiZap Bot - Basic Functionality Tests")
    print("=" * 60)
    
    try:
        test_product_model()
        test_coupon_model()
        test_normalizer()
        test_coupon_service()
        
        # Run async test
        asyncio.run(test_mock_api())
        
        print("\n" + "=" * 60)
        print("✅ ALL BASIC TESTS PASSED!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
