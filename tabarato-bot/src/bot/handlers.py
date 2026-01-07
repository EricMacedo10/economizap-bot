"""
Message handlers for EconomiZap Bot.
Handles user messages and product searches.
"""

from telegram import Update
from telegram.ext import ContextTypes

from src.services.search_service import get_search_service
from src.database.connection import get_database
from src.database.repositories import UserRepository, SearchRepository
from src.utils.logger import get_logger

logger = get_logger(__name__)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle incoming text messages (product searches).
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user = update.effective_user
    message_text = update.message.text.strip()
    
    logger.info(f"User {user.id} searched for: {message_text}")
    
    # Validate search query
    if len(message_text) < 3:
        await update.message.reply_text(
            "⚠️ Por favor, digite pelo menos 3 caracteres para buscar.\n\n"
            "Exemplo: \"notebook gamer\""
        )
        return
    
    if len(message_text) > 100:
        await update.message.reply_text(
            "⚠️ Sua busca é muito longa. Por favor, use no máximo 100 caracteres.\n\n"
            "Seja mais específico com o produto que procura."
        )
        return
    
    # Send "searching" message
    searching_message = await update.message.reply_text(
        "🔍 Buscando os melhores preços...\n"
        "Aguarde alguns segundos! ⏳"
    )
    
    try:
        # Get search service
        search_service = get_search_service()
        
        # Perform search
        results = await search_service.search_all(message_text)
        
        # Save to database
        try:
            db = get_database()
            with db.session_scope() as session:
                # Get or create user
                db_user = UserRepository.get_or_create(
                    session=session,
                    telegram_id=str(user.id),
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name
                )
                
                # Save search
                SearchRepository.create_search(
                    session=session,
                    user=db_user,
                    search_result=results
                )
                
                logger.info(f"Saved search to database for user {user.id}")
        except Exception as db_error:
            # Log but don't fail the search if database save fails
            logger.error(f"Failed to save search to database: {db_error}", exc_info=True)
        
        # Delete "searching" message
        await searching_message.delete()
        
        # Check if we have results
        if not results.has_results:
            await update.message.reply_text(
                f"😔 Não encontrei resultados para: *{message_text}*\n\n"
                f"Tente:\n"
                f"• Usar termos mais genéricos\n"
                f"• Verificar a ortografia\n"
                f"• Remover caracteres especiais\n\n"
                f"Exemplo: \"notebook\" ao invés de \"notebook-gamer-rgb\"",
                parse_mode="Markdown"
            )
            return
        
        # Get best price
        best_product = results.best_price
        
        if not best_product:
            await update.message.reply_text(
                "😔 Ocorreu um erro ao processar os resultados.\n"
                "Por favor, tente novamente."
            )
            return
        
        # Format response message
        response_message = (
            f"🎯 *Melhor Preço Encontrado!*\n\n"
            f"{best_product.to_telegram_message()}\n\n"
            f"⏰ Preço verificado há alguns segundos\n"
            f"📊 Encontrados {results.total_results} resultado(s) em {results.search_time:.1f}s"
        )
        
        # Send response
        await update.message.reply_text(
            response_message,
            parse_mode="Markdown",
            disable_web_page_preview=False
        )
        
        logger.info(
            f"User {user.id} - Search successful: "
            f"{results.total_results} results, best price: R$ {best_product.price:.2f}"
        )
        
    except Exception as e:
        logger.error(f"Error handling search for user {user.id}: {e}", exc_info=True)
        
        # Delete "searching" message
        try:
            await searching_message.delete()
        except:
            pass
        
        # Send error message
        await update.message.reply_text(
            "😔 Desculpe, ocorreu um erro ao buscar produtos.\n"
            "Por favor, tente novamente em alguns instantes."
        )
