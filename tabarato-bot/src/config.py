"""
Configuration management for EconomiZap Bot.
Loads and validates environment variables.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration loaded from environment variables."""
    
    # ====================================
    # TELEGRAM CONFIGURATION
    # ====================================
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHANNEL_ID: str = os.getenv("TELEGRAM_CHANNEL_ID", "")
    
    # ====================================
    # DATABASE CONFIGURATION
    # ====================================
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///tabarato.db")
    
    # ====================================
    # MARKETPLACE API CREDENTIALS
    # ====================================
    
    # Mercado Livre
    MERCADOLIVRE_APP_ID: str = os.getenv("MERCADOLIVRE_APP_ID", "")
    MERCADOLIVRE_SECRET_KEY: str = os.getenv("MERCADOLIVRE_SECRET_KEY", "")
    
    # Amazon
    AMAZON_ACCESS_KEY: str = os.getenv("AMAZON_ACCESS_KEY", "")
    AMAZON_SECRET_KEY: str = os.getenv("AMAZON_SECRET_KEY", "")
    AMAZON_PARTNER_TAG: str = os.getenv("AMAZON_PARTNER_TAG", "")
    AMAZON_REGION: str = os.getenv("AMAZON_REGION", "us-east-1")
    
    # Shopee
    SHOPEE_PARTNER_ID: str = os.getenv("SHOPEE_PARTNER_ID", "")
    SHOPEE_PARTNER_KEY: str = os.getenv("SHOPEE_PARTNER_KEY", "")
    
    # AliExpress
    ALIEXPRESS_APP_KEY: str = os.getenv("ALIEXPRESS_APP_KEY", "")
    ALIEXPRESS_APP_SECRET: str = os.getenv("ALIEXPRESS_APP_SECRET", "")
    ALIEXPRESS_TRACKING_ID: str = os.getenv("ALIEXPRESS_TRACKING_ID", "")
    
    # ====================================
    # APPLICATION SETTINGS
    # ====================================
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Search settings
    SEARCH_TIMEOUT: int = int(os.getenv("SEARCH_TIMEOUT", "10"))
    MAX_RESULTS_PER_MARKETPLACE: int = int(os.getenv("MAX_RESULTS_PER_MARKETPLACE", "5"))
    
    # Normalization settings
    SIMILARITY_THRESHOLD: int = int(os.getenv("SIMILARITY_THRESHOLD", "70"))
    
    # Channel posting settings
    MIN_DISCOUNT_FOR_CHANNEL: int = int(os.getenv("MIN_DISCOUNT_FOR_CHANNEL", "30"))
    
    # Rate limiting
    MAX_SEARCHES_PER_MINUTE: int = int(os.getenv("MAX_SEARCHES_PER_MINUTE", "10"))
    
    # Cache settings
    CACHE_EXPIRATION: int = int(os.getenv("CACHE_EXPIRATION", "3600"))
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate that required configuration is present.
        
        Returns:
            bool: True if configuration is valid
            
        Raises:
            ValueError: If required configuration is missing
        """
        required_vars = {
            "TELEGRAM_BOT_TOKEN": cls.TELEGRAM_BOT_TOKEN,
        }
        
        missing_vars = [
            var_name for var_name, var_value in required_vars.items()
            if not var_value
        ]
        
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}\n"
                f"Please check your .env file or environment configuration."
            )
        
        return True
    
    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development mode."""
        return cls.ENVIRONMENT.lower() == "development"
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production mode."""
        return cls.ENVIRONMENT.lower() == "production"
    
    @classmethod
    def get_log_level(cls) -> str:
        """Get the configured log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        level = cls.LOG_LEVEL.upper()
        return level if level in valid_levels else "INFO"


# Validate configuration on import (only in production)
if Config.ENVIRONMENT.lower() != "development":
    Config.validate()
