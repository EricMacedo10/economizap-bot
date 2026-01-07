"""
Coupon data model for EconomiZap Bot.
Represents discount coupons for marketplaces.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class Coupon(BaseModel):
    """
    Coupon model representing a discount code.
    
    Attributes:
        code: Coupon code (e.g., "TECH10")
        marketplace: Marketplace name
        discount_type: Type of discount ("percentage" or "fixed")
        discount_value: Discount value (percentage or amount)
        valid_from: Start date of validity
        valid_until: End date of validity
        minimum_purchase: Minimum purchase amount (optional)
        maximum_discount: Maximum discount amount (optional)
        categories: Applicable categories (optional)
        description: Coupon description
        is_active: Whether coupon is currently active
    """
    
    code: str = Field(..., min_length=1, max_length=50, description="Coupon code")
    marketplace: str = Field(..., description="Marketplace name")
    discount_type: str = Field(..., description="Discount type: percentage or fixed")
    discount_value: float = Field(..., gt=0, description="Discount value")
    valid_from: datetime = Field(..., description="Start date")
    valid_until: datetime = Field(..., description="End date")
    minimum_purchase: Optional[float] = Field(None, ge=0, description="Minimum purchase")
    maximum_discount: Optional[float] = Field(None, gt=0, description="Maximum discount")
    categories: Optional[List[str]] = Field(None, description="Applicable categories")
    description: Optional[str] = Field(None, max_length=200, description="Description")
    is_active: bool = Field(default=True, description="Is active")
    
    @field_validator('discount_type')
    @classmethod
    def validate_discount_type(cls, v: str) -> str:
        """Validate discount type."""
        valid_types = ['percentage', 'fixed']
        if v.lower() not in valid_types:
            raise ValueError(f"Discount type must be one of: {valid_types}")
        return v.lower()
    
    @field_validator('discount_value')
    @classmethod
    def validate_discount_value(cls, v: float, info) -> float:
        """Validate discount value based on type."""
        # If percentage, must be between 0 and 100
        if info.data.get('discount_type') == 'percentage' and v > 100:
            raise ValueError("Percentage discount cannot exceed 100%")
        return v
    
    def is_valid(self, current_date: Optional[datetime] = None) -> bool:
        """
        Check if coupon is currently valid.
        
        Args:
            current_date: Date to check (default: now)
            
        Returns:
            bool: True if valid
        """
        if not self.is_active:
            return False
        
        now = current_date or datetime.now()
        
        return self.valid_from <= now <= self.valid_until
    
    def can_apply_to_price(self, price: float) -> bool:
        """
        Check if coupon can be applied to a price.
        
        Args:
            price: Product price
            
        Returns:
            bool: True if applicable
        """
        if not self.is_valid():
            return False
        
        if self.minimum_purchase and price < self.minimum_purchase:
            return False
        
        return True
    
    def calculate_discount(self, price: float) -> float:
        """
        Calculate discount amount for a price.
        
        Args:
            price: Original price
            
        Returns:
            float: Discount amount
        """
        if not self.can_apply_to_price(price):
            return 0.0
        
        if self.discount_type == 'percentage':
            discount = price * (self.discount_value / 100)
        else:  # fixed
            discount = self.discount_value
        
        # Apply maximum discount limit
        if self.maximum_discount:
            discount = min(discount, self.maximum_discount)
        
        # Discount cannot exceed price
        discount = min(discount, price)
        
        return discount
    
    def apply_to_price(self, price: float) -> float:
        """
        Apply coupon to price and return final price.
        
        Args:
            price: Original price
            
        Returns:
            float: Final price after discount
        """
        discount = self.calculate_discount(price)
        return max(0.0, price - discount)
    
    def format_discount(self) -> str:
        """
        Format discount for display.
        
        Returns:
            str: Formatted discount (e.g., "10% OFF" or "R$ 50 OFF")
        """
        if self.discount_type == 'percentage':
            return f"{self.discount_value:.0f}% OFF"
        else:
            return f"R$ {self.discount_value:.2f} OFF"
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        validate_assignment = True
