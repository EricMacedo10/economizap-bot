# EconomiZap Bot - Setup Guide

## Quick Start

### 1. Create Your Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Choose a name for your bot (e.g., "EconomiZap Price Finder")
4. Choose a username (must end in 'bot', e.g., "economizap_bot")
5. Copy the token provided by BotFather

### 2. Setup Environment

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` and add your bot token:
```env
TELEGRAM_BOT_TOKEN=your_token_here
```

### 3. Install Dependencies

Create a virtual environment and install dependencies:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Run the Bot

```bash
python src/main.py
```

You should see:
```
Starting EconomiZap Bot...
Environment: development
✅ Configuration validated successfully
✅ Telegram application created successfully
✅ Command handlers registered
✅ Message handler registered
✅ Error handler registered
🚀 Starting bot polling...
Bot is now running! Press Ctrl+C to stop.
```

### 5. Test the Bot

1. Open Telegram
2. Search for your bot by username
3. Send `/start` command
4. Try sending a product name like "notebook"

## Next Steps

After Phase 1 is complete, we'll implement:
- Phase 2: Mercado Livre API integration
- Phase 3: Product normalization and price comparison
- Phase 4: Additional marketplace integrations

## Troubleshooting

### "Missing required environment variables"
- Make sure you created the `.env` file
- Check that `TELEGRAM_BOT_TOKEN` is set correctly

### "Failed to create Telegram application"
- Verify your bot token is correct
- Check your internet connection
- Make sure the token hasn't been revoked

### Import errors
- Ensure you're in the virtual environment
- Run `pip install -r requirements.txt` again

## Development Tips

- Keep the bot running in a terminal while testing
- Check logs for any errors
- Use `/help` command to see available features
- Press Ctrl+C to stop the bot gracefully
