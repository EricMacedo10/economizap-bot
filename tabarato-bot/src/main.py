"""
Main entry point for EconomiZap Bot.
"""

import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from src.config import Config
from src.bot.commands import start_command, help_command, about_command, error_handler
from src.bot.stats import stats_command
from src.bot.admin import post_deal_command, stats_admin_command
from src.bot.handlers import handle_message
from src.database.connection import init_database, close_database
from src.services.channel_service import get_channel_service
from src.utils.logger import get_logger

logger = get_logger(__name__)


async def main() -> None:
    """
    Main function to run the bot.
    """
    try:
        # Load and validate configuration
        logger.info("Loading configuration...")
        Config.validate()
        logger.info("Configuration loaded successfully")
        
        # Initialize database
        logger.info("Initializing database...")
        try:
            init_database()
            logger.info("Database initialized successfully")
        except Exception as db_error:
            logger.warning(f"Database initialization failed: {db_error}")
            logger.warning("Bot will continue without database persistence")
        
        # Create the Application
        logger.info("Creating Telegram bot application...")
        application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
        
        # Initialize channel service with bot instance
        get_channel_service(application.bot)
        logger.info("Channel service initialized")
        
        # Register command handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("about", about_command))
        application.add_handler(CommandHandler("stats", stats_command))
        
        # Admin commands
        application.add_handler(CommandHandler("postdeal", post_deal_command))
        application.add_handler(CommandHandler("adminstats", stats_admin_command))
        
        # Register message handler (for product searches)
        application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
        )
        
        # Register error handler
        application.add_error_handler(error_handler)
        
        logger.info("All handlers registered successfully")
        
        # Start the bot
        logger.info("Starting bot...")
        logger.info("Bot is now running. Press Ctrl+C to stop.")
        
        await application.run_polling(allowed_updates=["message"])
        
    except KeyboardInterrupt:
        logger.info("Received shutdown signal (Ctrl+C)")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise
    finally:
        # Cleanup
        logger.info("Shutting down...")
        try:
            close_database()
        except:
            pass
        logger.info("Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
