"""
Admin commands for bot management.
Only accessible by bot administrators.
"""

from telegram import Update
from telegram.ext import ContextTypes

from src.services.channel_service import get_channel_service
from src.services.search_service import get_search_service
from src.database.connection import get_database
from src.database.repositories import SearchRepository
from src.config import Config
from src.utils.logger import get_logger

logger = get_logger(__name__)


# Admin user IDs (configure in .env)
ADMIN_IDS = [
    # Add your Telegram user ID here
    # You can get it by messaging @userinfobot
]


def is_admin(user_id: int) -> bool:
    """
    Check if user is an admin.
    
    Args:
        user_id: Telegram user ID
        
    Returns:
        bool: True if user is admin
    """
    return user_id in ADMIN_IDS


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Broadcast a message to all users.
    Admin only command.
    
    Usage: /broadcast <message>
    """
    user = update.effective_user
    
    if not is_admin(user.id):
        await update.message.reply_text("⛔ Este comando é apenas para administradores.")
        return
    
    # Get message to broadcast
    if not context.args:
        await update.message.reply_text(
            "📢 *Broadcast*\n\n"
            "Uso: `/broadcast <mensagem>`\n\n"
            "Exemplo: `/broadcast Novidade! Agora buscamos em 4 marketplaces!`",
            parse_mode="Markdown"
        )
        return
    
    message = " ".join(context.args)
    
    await update.message.reply_text(
        f"📢 Broadcast em desenvolvimento.\n\n"
        f"Mensagem que seria enviada:\n{message}"
    )


async def post_deal_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Manually post a deal to channel.
    Admin only command.
    
    Usage: /postdeal <search query>
    """
    user = update.effective_user
    
    if not is_admin(user.id):
        await update.message.reply_text("⛔ Este comando é apenas para administradores.")
        return
    
    if not context.args:
        await update.message.reply_text(
            "📢 *Post Deal*\n\n"
            "Uso: `/postdeal <produto>`\n\n"
            "Exemplo: `/postdeal notebook gamer`",
            parse_mode="Markdown"
        )
        return
    
    query = " ".join(context.args)
    
    await update.message.reply_text(f"🔍 Buscando ofertas de: {query}...")
    
    try:
        # Search
        search_service = get_search_service()
        results = await search_service.search_all(query)
        
        if not results.has_results:
            await update.message.reply_text("😔 Nenhum resultado encontrado.")
            return
        
        # Post best deals
        channel_service = get_channel_service(context.bot)
        posted = await channel_service.post_best_deals(results.products, max_posts=3)
        
        if posted > 0:
            await update.message.reply_text(
                f"✅ {posted} oferta(s) postada(s) no canal!"
            )
        else:
            await update.message.reply_text(
                "ℹ️ Nenhuma oferta boa o suficiente para postar.\n"
                f"(Desconto mínimo: {Config.MIN_DISCOUNT_FOR_CHANNEL}%)"
            )
            
    except Exception as e:
        logger.error(f"Error in post_deal command: {e}", exc_info=True)
        await update.message.reply_text("😔 Erro ao postar ofertas.")


async def stats_admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Show global statistics.
    Admin only command.
    """
    user = update.effective_user
    
    if not is_admin(user.id):
        await update.message.reply_text("⛔ Este comando é apenas para administradores.")
        return
    
    try:
        db = get_database()
        with db.session_scope() as session:
            total_searches = SearchRepository.get_total_searches(session)
            popular = SearchRepository.get_popular_queries(session, days=7, limit=10)
            
            message_parts = [
                "📊 *Estatísticas Globais*\n\n",
                f"🔍 Total de buscas: {total_searches}\n\n",
                "*🔥 Top 10 Buscas (7 dias):*\n"
            ]
            
            for i, (query, count) in enumerate(popular, 1):
                message_parts.append(f"{i}. {query} ({count}x)\n")
            
            await update.message.reply_text(
                "".join(message_parts),
                parse_mode="Markdown"
            )
            
    except Exception as e:
        logger.error(f"Error in stats_admin command: {e}", exc_info=True)
        await update.message.reply_text("😔 Erro ao buscar estatísticas.")
