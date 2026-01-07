"""
Bot command handlers for EconomiZap Bot.
Handles /start, /help, and other bot commands.
"""

from telegram import Update
from telegram.ext import ContextTypes

from src.utils.logger import get_logger
from src.bot.stats import stats_command

logger = get_logger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /start command.
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started the bot")
    
    welcome_message = (
        f"🎉 *Bem-vindo ao EconomiZap!* 🎉\n\n"
        f"Olá, {user.first_name}! 👋\n\n"
        f"Eu sou seu assistente pessoal para encontrar os *melhores preços* "
        f"em produtos de diversos marketplaces brasileiros! 🛒\n\n"
        f"*Como usar:*\n"
        f"📝 Simplesmente me envie o nome do produto que você procura\n"
        f"⚡ Eu vou buscar nos principais marketplaces\n"
        f"💰 E te mostrar o melhor preço com cupons aplicados!\n\n"
        f"*Exemplo:*\n"
        f"\"notebook gamer\"\n"
        f"\"fone bluetooth\"\n"
        f"\"smart tv 50 polegadas\"\n\n"
        f"*Marketplaces integrados:*\n"
        f"🟠 Amazon Brasil\n"
        f"🔵 Mercado Livre\n"
        f"🟠 Shopee\n"
        f"🔴 AliExpress\n\n"
        f"Digite /help para mais informações!\n\n"
        f"Vamos economizar juntos! 💸"
    )
    
    await update.message.reply_text(
        welcome_message,
        parse_mode="Markdown"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /help command.
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user = update.effective_user
    logger.info(f"User {user.id} requested help")
    
    help_message = (
        "📚 *Ajuda - EconomiZap Bot* 📚\n\n"
        "📖 *Comandos Disponíveis:*\n\n"
        "/start - Iniciar o bot\n"
        "/help - Ver esta mensagem de ajuda\n"
        "/about - Sobre o EconomiZap Bot\n"
        "/stats - Ver suas estatísticas\n\n"
        "*Como buscar produtos:*\n"
        "Envie uma mensagem com o nome do produto que você procura. "
        "Seja específico para melhores resultados!\n\n"
        "*Exemplos de buscas:*\n"
        "✅ \"notebook dell inspiron 15\"\n"
        "✅ \"iphone 13 128gb\"\n"
        "✅ \"air fryer philco 4l\"\n\n"
        "❌ \"notebook\" (muito genérico)\n"
        "❌ \"celular barato\" (muito vago)\n\n"
        "*O que eu faço:*\n"
        "1️⃣ Busco o produto em 4 marketplaces\n"
        "2️⃣ Comparo os preços\n"
        "3️⃣ Aplico cupons de desconto automaticamente\n"
        "4️⃣ Mostro o melhor preço para você!\n\n"
        "*Dicas:*\n"
        "💡 Seja específico na busca\n"
        "💡 Inclua marca e modelo quando possível\n"
        "💡 Verifique as especificações antes de comprar\n\n"
        "*Precisa de ajuda?*\n"
        "Entre em contato: @seu_usuario\n\n"
        "Boas compras! 🛍️"
    )
    
    await update.message.reply_text(
        help_message,
        parse_mode="Markdown"
    )


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /about command.
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user = update.effective_user
    logger.info(f"User {user.id} requested about info")
    
    about_message = (
        "ℹ️ *Sobre o EconomiZap* ℹ️\n\n"
        "*Versão:* 1.0.0\n"
        "*Desenvolvedor:* Eric M.\n\n"
        "*O que é o EconomiZap?*\n"
        "Um bot inteligente que compara preços em múltiplos marketplaces "
        "brasileiros e encontra o melhor negócio para você, com cupons "
        "de desconto aplicados automaticamente! 🎯\n\n"
        "*Marketplaces integrados:*\n"
        "• Amazon Brasil 🟠\n"
        "• Mercado Livre 🔵\n"
        "• Shopee 🟠\n"
        "• AliExpress 🔴\n\n"
        "*Recursos:*\n"
        "✅ Busca em múltiplos marketplaces\n"
        "✅ Comparação inteligente de preços\n"
        "✅ Aplicação automática de cupons\n"
        "✅ Normalização de produtos\n"
        "✅ Canal com ofertas automáticas\n\n"
        "*Tecnologia:*\n"
        "🐍 Python\n"
        "🤖 python-telegram-bot\n"
        "🗄️ PostgreSQL\n"
        "☁️ Railway.app\n\n"
        "*Privacidade:*\n"
        "Não armazenamos dados pessoais além do necessário "
        "para o funcionamento do bot. Suas buscas são anônimas.\n\n"
        "*Siga nosso canal:*\n"
        "@economizap_ofertas (em breve)\n\n"
        "Feito com ❤️ para economizar seu dinheiro!"
    )
    
    await update.message.reply_text(
        about_message,
        parse_mode="Markdown"
    )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle errors in the bot.
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    logger.error(f"Update {update} caused error {context.error}", exc_info=context.error)
    
    # Send a friendly error message to the user
    if update and update.effective_message:
        error_message = (
            "😔 Desculpe, ocorreu um erro ao processar sua solicitação.\n\n"
            "Por favor, tente novamente em alguns instantes.\n"
            "Se o problema persistir, entre em contato com o suporte."
        )
        
        try:
            await update.effective_message.reply_text(error_message)
        except Exception as e:
            logger.error(f"Failed to send error message to user: {e}")
