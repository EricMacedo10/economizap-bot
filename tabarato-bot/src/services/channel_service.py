"""
Channel service for posting deals to Telegram channel.
"""

from typing import Optional, List
from datetime import datetime, timedelta
from telegram import Bot
from telegram.error import TelegramError

from src.models.product import Product
from src.database.connection import get_database
from src.database.models import ChannelPost
from src.config import Config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ChannelService:
    """
    Service for managing Telegram channel posts.
    """
    
    def __init__(self, bot: Optional[Bot] = None):
        """
        Initialize channel service.
        
        Args:
            bot: Telegram Bot instance (optional)
        """
        self.bot = bot
        self.channel_id = Config.TELEGRAM_CHANNEL_ID
        self.min_discount = Config.MIN_DISCOUNT_FOR_CHANNEL
        
        logger.info(f"Channel service initialized (min discount: {self.min_discount}%)")
    
    def is_good_deal(self, product: Product) -> bool:
        """
        Check if product is a good deal worth posting.
        
        Args:
            product: Product to check
            
        Returns:
            bool: True if it's a good deal
        """
        # Must have discount
        if not product.has_discount:
            return False
        
        # Calculate discount percentage
        discount_pct = product.calculate_discount_percentage()
        
        # Must meet minimum discount threshold
        if discount_pct < self.min_discount:
            return False
        
        # Price must be reasonable (not too cheap = suspicious)
        if product.price < 10:
            return False
        
        return True
    
    async def post_deal(self, product: Product) -> Optional[str]:
        """
        Post a deal to the Telegram channel.
        
        Args:
            product: Product to post
            
        Returns:
            Optional[str]: Message ID if posted successfully
        """
        if not self.bot:
            logger.warning("Bot not initialized, cannot post to channel")
            return None
        
        if not self.channel_id:
            logger.warning("Channel ID not configured")
            return None
        
        # Check if it's a good deal
        if not self.is_good_deal(product):
            logger.debug(f"Product {product.name[:30]}... is not a good deal")
            return None
        
        # Check if already posted recently
        if self._was_recently_posted(product):
            logger.debug(f"Product {product.name[:30]}... was recently posted")
            return None
        
        try:
            # Format message
            message = self._format_channel_message(product)
            
            # Post to channel
            sent_message = await self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode="Markdown",
                disable_web_page_preview=False
            )
            
            # Save to database
            self._save_channel_post(product, str(sent_message.message_id))
            
            logger.info(f"Posted deal to channel: {product.name[:50]}...")
            
            return str(sent_message.message_id)
            
        except TelegramError as e:
            logger.error(f"Failed to post to channel: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error posting to channel: {e}", exc_info=True)
            return None
    
    def _format_channel_message(self, product: Product) -> str:
        """
        Format product as channel message.
        
        Args:
            product: Product to format
            
        Returns:
            str: Formatted message
        """
        discount_pct = product.calculate_discount_percentage()
        
        message_parts = [
            "🔥 *OFERTA IMPERDÍVEL!* 🔥\n\n",
            f"📦 {product.name}\n\n",
            f"🏪 *{product.marketplace}*\n",
        ]
        
        # Price info
        if product.original_price:
            message_parts.append(
                f"💰 ~~R$ {product.format_original_price()}~~ → "
                f"*R$ {product.format_price()}*\n"
            )
            message_parts.append(
                f"📉 *{discount_pct:.0f}% OFF* "
                f"(Economia: R$ {product.savings:.2f})\n"
            )
        else:
            message_parts.append(f"💰 *{product.format_price()}*\n")
        
        # Coupon
        if product.coupon_code:
            message_parts.append(f"🎟️ Cupom: `{product.coupon_code}`\n")
        
        # Link
        message_parts.append(f"\n🔗 [COMPRAR AGORA]({product.url})\n")
        
        # Timestamp
        message_parts.append(f"\n⏰ Oferta verificada agora")
        
        return "".join(message_parts)
    
    def _was_recently_posted(self, product: Product, hours: int = 24) -> bool:
        """
        Check if product was posted recently.
        
        Args:
            product: Product to check
            hours: Number of hours to look back
            
        Returns:
            bool: True if posted recently
        """
        try:
            db = get_database()
            with db.session_scope() as session:
                since = datetime.utcnow() - timedelta(hours=hours)
                
                existing = session.query(ChannelPost).filter(
                    ChannelPost.product_external_id == product.id,
                    ChannelPost.marketplace == product.marketplace,
                    ChannelPost.posted_at >= since
                ).first()
                
                return existing is not None
                
        except Exception as e:
            logger.error(f"Error checking recent posts: {e}")
            return False
    
    def _save_channel_post(self, product: Product, message_id: str) -> None:
        """
        Save channel post to database.
        
        Args:
            product: Posted product
            message_id: Telegram message ID
        """
        try:
            db = get_database()
            with db.session_scope() as session:
                post = ChannelPost(
                    product_external_id=product.id,
                    marketplace=product.marketplace,
                    product_name=product.name,
                    price=product.price,
                    original_price=product.original_price,
                    discount_percentage=product.calculate_discount_percentage(),
                    url=product.url,
                    message_id=message_id
                )
                session.add(post)
                
        except Exception as e:
            logger.error(f"Error saving channel post: {e}")
    
    async def post_best_deals(self, products: List[Product], max_posts: int = 3) -> int:
        """
        Post best deals from a list of products.
        
        Args:
            products: List of products
            max_posts: Maximum number of posts
            
        Returns:
            int: Number of deals posted
        """
        # Filter good deals
        good_deals = [p for p in products if self.is_good_deal(p)]
        
        if not good_deals:
            logger.debug("No good deals found to post")
            return 0
        
        # Sort by discount percentage (best first)
        good_deals.sort(
            key=lambda p: p.calculate_discount_percentage(),
            reverse=True
        )
        
        # Post top deals
        posted_count = 0
        for product in good_deals[:max_posts]:
            message_id = await self.post_deal(product)
            if message_id:
                posted_count += 1
        
        logger.info(f"Posted {posted_count} deals to channel")
        return posted_count


# Global channel service instance
_channel_service: Optional[ChannelService] = None


def get_channel_service(bot: Optional[Bot] = None) -> ChannelService:
    """
    Get the global channel service instance.
    
    Args:
        bot: Telegram Bot instance
        
    Returns:
        ChannelService: Global channel service
    """
    global _channel_service
    
    if _channel_service is None:
        _channel_service = ChannelService(bot)
    elif bot and not _channel_service.bot:
        _channel_service.bot = bot
    
    return _channel_service
