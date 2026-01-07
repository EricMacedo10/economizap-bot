"""
Product data model for EconomiZap Bot.
Represents a product from any marketplace.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl, field_validator


class Product(BaseModel):
    """
    Product model representing an item from any marketplace.
    
    Attributes:
        id: Unique product identifier from marketplace
        name: Product name/title
        price: Current price
        original_price: Original price before discounts (optional)
        marketplace: Name of the marketplaPrice comparison service for EconomiZap Bot.c.)
        url: Product page URL
        image_url: Product image URL (optional)
        coupon_code: Applied coupon code (optional)
        discount_percentage: Discount percentage (optional)
        currency: Currency code (default: BRL)
    """
    
    id: str = Field(..., description="Product ID from marketplace")
    name: str = Field(..., min_length=1, max_length=500, description="Product name")
    price: float = Field(..., gt=0, description="Current price")
    original_price: Optional[float] = Field(None, description="Original price")
    marketplace: str = Field(..., description="Marketplace name")
    url: str = Field(..., description="Product URL")
    image_url: Optional[str] = Field(None, description="Product image URL")
    coupon_code: Optional[str] = Field(None, max_length=50, description="Coupon code")
    discount_percentage: Optional[float] = Field(None, ge=0, le=100, description="Discount %")
    currency: str = Field(default="BRL", description="Currency code")
    timestamp: datetime = Field(default_factory=datetime.now, description="Fetch timestamp")
    
    
    @property
    def final_price(self) -> float:
        """
        Get the final price after discounts.
        
        Returns:
            float: Final price
        """
        return self.price
    
    @property
    def has_discount(self) -> bool:
        """
        Check if product has a discount.
        
        Returns:
            bool: True if product has discount
        """
        return self.original_price is not None and self.original_price > self.price
    
    @property
    def savings(self) -> float:
        """
        Calculate savings amount.
        
        Returns:
            float: Savings amount (0 if no discount)
        """
        if self.has_discount and self.original_price:
            return self.original_price - self.price
        return 0.0
    
    def calculate_discount_percentage(self) -> float:
        """
        Calculate discount percentage.
        
        Returns:
            float: Discount percentage (0 if no discount)
        """
        if self.has_discount and self.original_price:
            return ((self.original_price - self.price) / self.original_price) * 100
        return 0.0
    
    def format_price(self) -> str:
        """
        Format price as Brazilian Real.
        
        Returns:
            str: Formatted price (e.g., "R$ 1.299,90")
        """
        return f"R$ {self.price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    def format_original_price(self) -> str:
        """
        Format original price as Brazilian Real.
        
        Returns:
            str: Formatted original price
        """
        if self.original_price:
            return f"R$ {self.original_price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return ""
    
    def to_telegram_message(self) -> str:
        """
        Format product as Telegram message.
        
        Returns:
            str: Formatted message for Telegram
        """
        message_parts = [
            f"📦 *{self.name}*\n",
            f"🏪 {self.marketplace}\n"
        ]
        
        # Show discount if available
        if self.has_discount and self.original_price:
            discount_pct = self.calculate_discount_percentage()
            message_parts.append(f"💰 ~~{self.format_original_price()}~~ → *{self.format_price()}*\n")
            message_parts.append(f"📉 {discount_pct:.0f}% OFF (Economia: R$ {self.savings:.2f})\n")
        else:
            message_parts.append(f"💰 *{self.format_price()}*\n")
        
        # Show coupon if available
        if self.coupon_code:
            message_parts.append(f"🎟️ Cupom: `{self.coupon_code}`\n")
        
        # Add link
        message_parts.append(f"\n🔗 [Comprar Agora]({self.url})")
        
        return "".join(message_parts)
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        validate_assignment = True


class SearchResult(BaseModel):
    """
    Search service for EconomiZap Bot.ntaining multiple products.
    
    Attributes:
        query: Original search query
        products: List of products found
        total_results: Total number of results
        timestamp: When the search was performed
    """
    
    query: str = Field(..., min_length=1, description="Search query")
    products: list[Product] = Field(default_factory=list, description="Products found")
    total_results: int = Field(default=0, ge=0, description="Total results")
    search_time: float = Field(default=0.0, ge=0, description="Search time in seconds")
    timestamp: datetime = Field(default_factory=datetime.now, description="Search timestamp")
    
    @property
    def has_results(self) -> bool:
        """Check if search has results."""
        return len(self.products) > 0
    
    @property
    def best_price(self) -> Optional[Product]:
        """
        Get product with best price.
        
        Returns:
            Optional[Product]: Product with lowest price, or None
        """
        if not self.products:
            return None
        return min(self.products, key=lambda p: p.final_price)
    
    def get_products_by_marketplace(self, marketplace: str) -> list[Product]:
        """
        Get products from specific marketplace.
        
        Args:
            marketplace: Marketplace name
            
        Returns:
            list[Product]: Products from that marketplace
        """
        return [p for p in self.products if p.marketplace == marketplace]
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
