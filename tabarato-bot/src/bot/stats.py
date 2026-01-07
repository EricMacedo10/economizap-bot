"""
Statistics command for EconomiZap Bot.
Shows user search history and popular queries.
"""

from telegram import Update
from telegram.ext import ContextTypes

from src.database.connection import get_database
from src.database.repositories import UserRepository, SearchRepository
from src.utils.logger import get_logger

logger = get_logger(__name__)


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /stats command - show user statistics.
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user = update.effective_user
    
    try:
        db = get_database()
        with db.session_scope() as session:
            # Get user
            db_user = UserRepository.get_by_telegram_id(session, str(user.id))
            
            if not db_user:
                await update.message.reply_text(
                    "📊 *Suas Estatísticas*\n\n"
                    "Você ainda não fez nenhuma busca!\n\n"
                    "Envie o nome de um produto para começar.",
                    parse_mode="Markdown"
                )
                return
            
            # Get user's recent searches
            recent_searches = SearchRepository.get_user_searches(
                session, db_user, limit=5
            )
            
            # Get popular queries
            popular_queries = SearchRepository.get_popular_queries(
                session, days=7, limit=5
            )
            
            # Format message
            message_parts = [
                "📊 *Suas Estatísticas*\n",
                f"👤 Usuário desde: {db_user.created_at.strftime('%d/%m/%Y')}\n",
                f"🔍 Total de buscas: {len(db_user.searches)}\n\n"
            ]
            
            # Recent searches
            if recent_searches:
                message_parts.append("*🕐 Buscas Recentes:*\n")
                for search in recent_searches:
                    date = search.created_at.strftime('%d/%m %H:%M')
                    message_parts.append(
                        f"• {search.query} - {search.results_count} resultado(s) ({date})\n"
                    )
                message_parts.append("\n")
            
            # Popular queries
            if popular_queries:
                message_parts.append("*🔥 Buscas Populares (7 dias):*\n")
                for query, count in popular_queries[:5]:
                    message_parts.append(f"• {query} ({count}x)\n")
            
            await update.message.reply_text(
                "".join(message_parts),
                parse_mode="Markdown"
            )
            
    except Exception as e:
        logger.error(f"Error in stats command: {e}", exc_info=True)
        await update.message.reply_text(
            "😔 Desculpe, ocorreu um erro ao buscar suas estatísticas.\n"
            "Por favor, tente novamente mais tarde."
        )
