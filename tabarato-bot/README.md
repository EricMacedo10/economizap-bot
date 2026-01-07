**EconomiZap** is an intelligent Telegram bot that automatically searches for products across multiple marketplaces, compares prices, applies coupons, and returns the best deal - all in seconds!

---

## ✨ Features

### 🔍 Multi-Marketplace Search
- Searches **4 marketplaces** simultaneously
- **Mercado Livre** (real API)
- **Amazon** (mock/real)
- **Shopee** (mock/real)
- **AliExpress** (mock/real)

### 🎯 Intelligent Price Comparison
- **Fuzzy matching** to group similar products
- **Automatic coupon application**
- **Best price detection** across all marketplaces
- **Savings calculation** and discount percentages

### 💾 Database & Analytics
- **PostgreSQL/SQLite** support
- **Search history** tracking
- **User statistics** (`/stats` command)
- **Popular queries** analytics

### 📢 Channel Automation
- **Automatic deal posting** to Telegram channel
- **Configurable discount threshold**
- **Anti-spam** (won't post same product within 24h)
- **Admin commands** for manual control

### 🛡️ Production Ready
- **Comprehensive error handling**
- **Sensitive data filtering** in logs
- **Rate limiting** ready
- **Docker support**
- **Railway/Heroku** deployment configs

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Telegram Bot Token ([Get from @BotFather](https://t.me/BotFather))
- PostgreSQL (optional - SQLite works for testing)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/economizap-bot.git
   cd economizap-bot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Telegram bot token
   ```

5. **Run the bot**
   ```bash
   python src/main.py
   ```

---

## 📖 Usage

### Basic Commands

- `/start` - Start the bot
- `/help` - Show help message
- `/about` - About the bot
- `/stats` - Your search statistics

### Searching for Products

Just send a message with the product name:

```
notebook gamer
```

The bot will:
1. Search 4 marketplaces in parallel
2. Apply available coupons
3. Compare prices
4. Return the best deal

**Example Response:**
```
🎯 Melhor Preço Encontrado!

📦 Notebook Gamer Dell G15 i7 16GB 512GB
🏪 Shopee
💰 R$ 4.299,90
📉 15% OFF (Economia: R$ 750,00)
🎟️ Cupom: TECH15

🔗 Comprar Agora

⏰ Preço verificado há alguns segundos
📊 Encontrados 18 resultado(s) em 2.3s
```

### Admin Commands (Optional)

- `/postdeal <product>` - Manually post deal to channel
- `/adminstats` - Global bot statistics

---

## 🛠️ Technology Stack

- **Language:** Python 3.11+
- **Bot Framework:** python-telegram-bot 20.x
- **Database:** PostgreSQL / SQLite
- **ORM:** SQLAlchemy
- **HTTP Client:** aiohttp (async)
- **Fuzzy Matching:** fuzzywuzzy
- **Scheduler:** APScheduler
- **Deployment:** Railway / Heroku / Docker

---

## 📁 Project Structure

```
economizap-bot/
├── src/
│   ├── bot/              # Bot handlers and commands
│   ├── services/         # Business logic services
│   ├── integrations/     # Marketplace API integrations
│   ├── models/           # Data models (Pydantic)
│   ├── database/         # Database models and repositories
│   ├── utils/            # Utilities (logger, normalizer)
│   ├── config.py         # Configuration management
│   └── main.py           # Entry point
├── tests/                # Unit and integration tests
├── docs/                 # Documentation
├── .env.example          # Environment variables template
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker configuration
├── railway.toml          # Railway deployment config
└── README.md             # This file
```

---

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run with Coverage
```bash
pytest tests/ --cov=src --cov-report=html
```

### Test Specific Module
```bash
pytest tests/test_models.py -v
```

---

## 🚢 Deployment

### Railway.app (Recommended)

1. Fork this repository
2. Create account on [Railway.app](https://railway.app)
3. Create new project from GitHub repo
4. Add PostgreSQL database
5. Configure environment variables
6. Deploy!

**Detailed guide:** [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

### Docker

```bash
docker build -t economizap-bot .
docker run -d --env-file .env economizap-bot
```

### VPS

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for complete VPS setup guide.

---

## 🔧 Configuration

### Required Environment Variables

```env
# Telegram (Required)
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather

# Database (Optional - uses SQLite if not set)
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Environment
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Optional Environment Variables

```env
# Channel automation
TELEGRAM_CHANNEL_ID=@your_channel
MIN_DISCOUNT_FOR_CHANNEL=20

# API Credentials (optional - uses mocks by default)
MERCADOLIVRE_APP_ID=your_app_id
AMAZON_ACCESS_KEY=your_key
SHOPEE_PARTNER_ID=your_id
ALIEXPRESS_APP_KEY=your_key
```

**Full guide:** [docs/API_CREDENTIALS.md](docs/API_CREDENTIALS.md)

---

## 💰 Cost

### Free Tier (Perfect for Testing)

- **Telegram Bot:** FREE
- **Mock APIs:** FREE
- **SQLite Database:** FREE
- **Railway Free Tier:** 500 hours/month

**Total: R$ 0/month** ✅

### Production (Recommended)

- **Railway Pro:** $5/month
- **PostgreSQL:** Included
- **Real APIs:** FREE (affiliate programs)

**Total: ~$5/month** 💵

---

## 📚 Documentation

- [Setup Guide](docs/SETUP.md) - Quick setup instructions
- [API Credentials](docs/API_CREDENTIALS.md) - How to get API keys
- [Deployment Guide](docs/DEPLOYMENT.md) - Deploy to production

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- Inspired by the need for better price comparison tools in Brazil
- Thanks to all marketplace APIs for making this possible

---

## 🎯 Roadmap

- [x] Multi-marketplace search
- [x] Intelligent price comparison
- [x] Automatic coupon application
- [x] Database integration
- [x] Channel automation
- [ ] Price history tracking
- [ ] Price drop alerts
- [ ] Web dashboard
- [ ] Mobile app

---

**Made with ❤️ in Brazil**
