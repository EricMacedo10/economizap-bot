# API Credentials Guide

## 📋 Overview

This guide explains how to obtain API credentials for each marketplace integration.

**Note:** The bot works with mock APIs by default (no credentials needed for testing). Real APIs are only needed for production use with actual marketplace data.

---

## 🔑 Telegram Bot Token (Required)

**What:** Your bot's authentication token  
**Cost:** FREE  
**Required:** YES (bot won't work without it)

### Steps:

1. **Open Telegram**
   - Search for `@BotFather`
   - Start a conversation

2. **Create New Bot**
   - Send `/newbot`
   - Choose a name (e.g., "EconomiZap Bot")
   - Choose a username (e.g., "tabarato_bot")

3. **Get Token**
   - BotFather will give you a token
   - Format: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
   - **Keep this secret!**

4. **Add to .env**
   ```
   TELEGRAM_BOT_TOKEN=your_token_here
   ```

### Optional: Create Channel

1. **Create Channel**
   - In Telegram, create a new channel
   - Make it public or private

2. **Add Bot as Admin**
   - Add your bot to the channel
   - Make it an administrator

3. **Get Channel ID**
   - For public: `@channel_username`
   - For private: Use `@userinfobot` (forward a message)

4. **Add to .env**
   ```
   TELEGRAM_CHANNEL_ID=@your_channel
   ```

---

## 🛒 Mercado Livre API (Optional - Real API)

**What:** Access to Mercado Livre product search  
**Cost:** FREE  
**Required:** NO (uses real API by default, no auth needed for search)

### Current Status:

The bot uses Mercado Livre's **public API** which doesn't require authentication for basic product searches.

### For Affiliate Links (Optional):

1. **Join Affiliate Program**
   - Go to: https://www.mercadolivre.com.br/afiliados
   - Sign up for affiliate program
   - Wait for approval (1-3 days)

2. **Get Credentials**
   - Access your affiliate dashboard
   - Get your App ID and Secret Key

3. **Add to .env**
   ```
   MERCADOLIVRE_APP_ID=your_app_id
   MERCADOLIVRE_SECRET_KEY=your_secret_key
   ```

---

## 📦 Amazon Product Advertising API (Optional - Real API)

**What:** Access to Amazon product data  
**Cost:** FREE (with conditions)  
**Required:** NO (mock API works for testing)

### Requirements:

- Must be approved for Amazon Associates program
- Must generate sales within 180 days to keep access
- U.S. based or international with tax info

### Steps:

1. **Join Amazon Associates**
   - Go to: https://affiliate-program.amazon.com.br/
   - Sign up for Associates program
   - Provide tax information
   - Wait for approval (1-7 days)

2. **Request API Access**
   - Log in to Associates Central
   - Go to Tools → Product Advertising API
   - Request access
   - Wait for approval (1-3 days)

3. **Get Credentials**
   - Access Key ID
   - Secret Access Key
   - Associate Tag (Tracking ID)

4. **Add to .env**
   ```
   AMAZON_ACCESS_KEY=your_access_key
   AMAZON_SECRET_KEY=your_secret_key
   AMAZON_PARTNER_TAG=your_associate_tag
   AMAZON_REGION=us-east-1
   ```

### Alternative:

Use the **mock API** (default) - no credentials needed!

---

## 🛍️ Shopee Affiliate API (Optional - Real API)

**What:** Access to Shopee product data  
**Cost:** FREE  
**Required:** NO (mock API works for testing)

### Steps:

1. **Join Shopee Affiliate**
   - Go to: https://affiliate.shopee.com.br/
   - Sign up for affiliate program
   - Provide business information
   - Wait for approval (3-7 days)

2. **Access Developer Portal**
   - Go to: https://open.shopee.com/
   - Register as developer
   - Create new app

3. **Get Credentials**
   - Partner ID
   - Partner Key

4. **Add to .env**
   ```
   SHOPEE_PARTNER_ID=your_partner_id
   SHOPEE_PARTNER_KEY=your_partner_key
   ```

### Alternative:

Use the **mock API** (default) - no credentials needed!

---

## 🌐 AliExpress Affiliate API (Optional - Real API)

**What:** Access to AliExpress product data  
**Cost:** FREE  
**Required:** NO (mock API works for testing)

### Steps:

1. **Join AliExpress Affiliate**
   - Go to: https://portals.aliexpress.com/
   - Sign up for Admitad or Impact affiliate program
   - Wait for approval (3-7 days)

2. **Get API Access**
   - Access affiliate dashboard
   - Request API credentials
   - Get App Key and Secret

3. **Get Tracking ID**
   - In dashboard, get your tracking ID
   - Used for commission tracking

4. **Add to .env**
   ```
   ALIEXPRESS_APP_KEY=your_app_key
   ALIEXPRESS_APP_SECRET=your_app_secret
   ALIEXPRESS_TRACKING_ID=your_tracking_id
   ```

### Alternative:

Use the **mock API** (default) - no credentials needed!

---

## 🗄️ Database (PostgreSQL)

**What:** Database for storing search history  
**Cost:** FREE (Railway/Heroku) or $5-15/month  
**Required:** NO (SQLite works for local testing)

### Option 1: Railway (Recommended)

1. **Create Railway Account**
   - Go to: https://railway.app
   - Sign up with GitHub

2. **Add PostgreSQL**
   - In your project, click "New"
   - Select "PostgreSQL"
   - Railway auto-configures

3. **Get Connection String**
   - Automatically available as `DATABASE_URL`
   - No manual configuration needed!

### Option 2: Local SQLite (Testing)

**No setup needed!** Just use:
```
DATABASE_URL=sqlite:///tabarato.db
```

### Option 3: Heroku Postgres

1. **Add to Heroku App**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

2. **Get URL**
   ```bash
   heroku config:get DATABASE_URL
   ```

---

## 🔄 Switching from Mock to Real APIs

### Current Setup (Default):

```env
# Mock APIs (no credentials needed)
USE_MOCK_APIS=true
```

### To Use Real APIs:

1. **Get Credentials** (follow guides above)

2. **Update .env**
   ```env
   USE_MOCK_APIS=false
   
   # Add real credentials
   AMAZON_ACCESS_KEY=your_key
   SHOPEE_PARTNER_ID=your_id
   ALIEXPRESS_APP_KEY=your_key
   ```

3. **Update Code** (if needed)
   - Replace mock API classes with real ones
   - See `src/integrations/` folder

---

## 💰 Cost Summary

### Free Tier (Recommended for Start):

| Service | Cost | Limits |
|---------|------|--------|
| Telegram Bot | FREE | Unlimited |
| Mercado Livre | FREE | Public API |
| Mock APIs | FREE | Unlimited |
| SQLite Database | FREE | Local only |
| Railway (Free) | FREE | 500 hours/month |

**Total: R$ 0/month** ✅

### Production Setup:

| Service | Cost | Benefits |
|---------|------|----------|
| Telegram Bot | FREE | Unlimited |
| Real APIs | FREE | Real products |
| Railway Pro | $5/month | More resources |
| PostgreSQL | Included | In Railway |

**Total: ~$5/month** 💵

---

## 🆘 Troubleshooting

### "Invalid Bot Token"

- Check token is correct
- No spaces before/after
- Token format: `number:letters`

### "API Access Denied"

- Verify credentials are correct
- Check API is enabled
- Ensure account is approved

### "Database Connection Failed"

- Check `DATABASE_URL` format
- Verify database is running
- Test connection manually

---

## ✅ Checklist

Before deploying to production:

- [ ] Telegram bot token obtained
- [ ] Channel created (optional)
- [ ] Database configured
- [ ] Decide: mock or real APIs
- [ ] If real APIs: get credentials
- [ ] Test locally first
- [ ] Deploy to Railway/Heroku
- [ ] Verify bot works
- [ ] Monitor for errors

---

## 📚 Additional Resources

- [Telegram Bot API Docs](https://core.telegram.org/bots/api)
- [Mercado Livre API Docs](https://developers.mercadolivre.com.br/)
- [Amazon PA API Docs](https://webservices.amazon.com/paapi5/documentation/)
- [Shopee Open Platform](https://open.shopee.com/documents)
- [AliExpress Affiliate](https://portals.aliexpress.com/)

---

**Remember:** You can start with mock APIs (FREE) and add real APIs later when needed!
