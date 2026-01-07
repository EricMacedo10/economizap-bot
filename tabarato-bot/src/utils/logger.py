"""
Logging configuration for EconomiZap Bot.
Provides structured logging with proper formatting and security.
"""

import logging
import sys
from typing import Optional
from pathlib import Path

from src.config import Config


class SensitiveDataFilter(logging.Filter):
    """Filter to mask sensitive data in logs."""
    
    SENSITIVE_PATTERNS = [
        "token", "password", "secret", "key", "api_key",
        "access_key", "partner_key", "app_secret"
    ]
    
    def filter(self, record: logging.LogRecord) -> bool:
        """
        Filter log records to mask sensitive data.
        
        Args:
            record: Log record to filter
            
        Returns:
            bool: Always True (we modify but don't block records)
        """
        # Mask sensitive data in the message
        message = record.getMessage()
        for pattern in self.SENSITIVE_PATTERNS:
            if pattern in message.lower():
                # Replace potential sensitive values
                record.msg = self._mask_sensitive_value(str(record.msg))
        
        return True
    
    @staticmethod
    def _mask_sensitive_value(text: str) -> str:
        """
        Mask sensitive values in text.
        
        Args:
            text: Text potentially containing sensitive data
            
        Returns:
            str: Text with sensitive data masked
        """
        # Simple masking - show first 4 chars, rest as asterisks
        if len(text) > 10:
            return f"{text[:4]}{'*' * (len(text) - 4)}"
        return "****"


def setup_logger(
    name: str,
    log_level: Optional[str] = None,
    log_file: Optional[Path] = None
) -> logging.Logger:
    """
    Setup and configure a logger.
    
    Args:
        name: Logger name (usually __name__)
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to write logs
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Set log level
    level = log_level or Config.get_log_level()
    logger.setLevel(getattr(logging, level))
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level))
    console_handler.setFormatter(formatter)
    console_handler.addFilter(SensitiveDataFilter())
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(getattr(logging, level))
        file_handler.setFormatter(formatter)
        file_handler.addFilter(SensitiveDataFilter())
        logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


# Create default application logger
app_logger = setup_logger("economizap_bot")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        logging.Logger: Logger instance
    """
    return setup_logger(name)
