"""
Database models for EconomiZap Bot.
Defines SQLAlchemy models for persistence.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, Index
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()


class User(Base):
    """
    User model for tracking bot users.
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(50), unique=True, nullable=False, index=True)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_seen = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    searches = relationship("Search", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"


class Search(Base):
    """
    Search history model.
    """
    __tablename__ = 'searches'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    query = Column(String(200), nullable=False, index=True)
    results_count = Column(Integer, default=0)
    best_price = Column(Float)
    best_marketplace = Column(String(50))
    search_time = Column(Float)  # Time taken in seconds
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="searches")
    products = relationship("ProductCache", back_populates="search", cascade="all, delete-orphan")
    
    # Indexes for common queries
    __table_args__ = (
        Index('idx_user_created', 'user_id', 'created_at'),
        Index('idx_query_created', 'query', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Search(query={self.query}, results={self.results_count})>"


class ProductCache(Base):
    """
    Cached product data from searches.
    """
    __tablename__ = 'product_cache'
    
    id = Column(Integer, primary_key=True)
    search_id = Column(Integer, ForeignKey('searches.id'), nullable=False, index=True)
    
    # Product data
    external_id = Column(String(100), nullable=False)  # ID from marketplace
    name = Column(String(500), nullable=False)
    price = Column(Float, nullable=False)
    original_price = Column(Float)
    marketplace = Column(String(50), nullable=False, index=True)
    url = Column(Text, nullable=False)
    image_url = Column(Text)
    coupon_code = Column(String(50))
    discount_percentage = Column(Float)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    search = relationship("Search", back_populates="products")
    
    # Indexes
    __table_args__ = (
        Index('idx_marketplace_created', 'marketplace', 'created_at'),
        Index('idx_external_id_marketplace', 'external_id', 'marketplace'),
    )
    
    def __repr__(self):
        return f"<ProductCache(name={self.name[:30]}..., price={self.price})>"


class PriceHistory(Base):
    """
    Price history tracking for products.
    """
    __tablename__ = 'price_history'
    
    id = Column(Integer, primary_key=True)
    external_id = Column(String(100), nullable=False, index=True)
    marketplace = Column(String(50), nullable=False, index=True)
    name = Column(String(500), nullable=False)
    price = Column(Float, nullable=False)
    original_price = Column(Float)
    url = Column(Text)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Indexes for price tracking queries
    __table_args__ = (
        Index('idx_product_tracking', 'external_id', 'marketplace', 'recorded_at'),
    )
    
    def __repr__(self):
        return f"<PriceHistory(product={self.external_id}, price={self.price})>"


class ChannelPost(Base):
    """
    Track posts made to Telegram channel.
    """
    __tablename__ = 'channel_posts'
    
    id = Column(Integer, primary_key=True)
    product_external_id = Column(String(100), nullable=False)
    marketplace = Column(String(50), nullable=False)
    product_name = Column(String(500), nullable=False)
    price = Column(Float, nullable=False)
    original_price = Column(Float)
    discount_percentage = Column(Float)
    url = Column(Text, nullable=False)
    
    # Post metadata
    message_id = Column(String(50))  # Telegram message ID
    posted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_product_posted', 'product_external_id', 'marketplace', 'posted_at'),
    )
    
    def __repr__(self):
        return f"<ChannelPost(product={self.product_name[:30]}...)>"


class Analytics(Base):
    """
    Analytics and statistics.
    """
    __tablename__ = 'analytics'
    
    id = Column(Integer, primary_key=True)
    metric_name = Column(String(100), nullable=False, index=True)
    metric_value = Column(Float, nullable=False)
    metadata = Column(JSONB)  # Additional data as JSON
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Indexes
    __table_args__ = (
        Index('idx_metric_time', 'metric_name', 'recorded_at'),
    )
    
    def __repr__(self):
        return f"<Analytics(metric={self.metric_name}, value={self.metric_value})>"
