# EconomiZap Bot - Deployment Guide

## 🚀 Deployment Options

### Option 1: Railway.app (Recommended - Free Tier Available)

**Why Railway?**
- ✅ Free tier with 500 hours/month
- ✅ Automatic deployments from GitHub
- ✅ Built-in PostgreSQL database
- ✅ Easy environment variable management
- ✅ Automatic HTTPS

**Steps:**

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `economizap-bot` repository

3. **Add PostgreSQL Database**
   - In your project, click "New"
   - Select "Database" → "PostgreSQL"
   - Railway will create and configure automatically

4. **Configure Environment Variables**
   - Go to your service settings
   - Add variables tab
   - Add all variables from `.env.example`:

   ```
   TELEGRAM_BOT_TOKEN=your_bot_token
   TELEGRAM_CHANNEL_ID=@your_channel
   DATABASE_URL=${{Postgres.DATABASE_URL}}  # Auto-filled by Railway
   ENVIRONMENT=production
   LOG_LEVEL=INFO
   MIN_DISCOUNT_FOR_CHANNEL=20
   ```

5. **Deploy**
   - Railway will automatically deploy
   - Check logs for any errors
   - Bot should start automatically

6. **Verify**
   - Send `/start` to your bot
   - Test a search
   - Check logs in Railway dashboard

---

### Option 2: Heroku

**Steps:**

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

8. **Start Service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable economizap-bot
   sudo systemctl start economizap-bot
   sudo systemctl status economizap-bot
   ```

3. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set TELEGRAM_BOT_TOKEN=your_token
   heroku config:set TELEGRAM_CHANNEL_ID=@your_channel
   heroku config:set ENVIRONMENT=production
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **Scale Worker**
   ```bash
   heroku ps:scale worker=1
   ```

---

### Option 3: VPS (DigitalOcean, AWS, etc.)

**Requirements:**
- Ubuntu 20.04+ server
- Python 3.11+
- PostgreSQL 14+

**Steps:**

1. **Connect to Server**
   ```bash
   ssh user@your-server-ip
   ```

2. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3.11 python3.11-venv postgresql
   ```

3. **Clone Repository**
   ```bash
   git clone https://github.com/your-username/economizap-bot.git
   cd economizap-bot
   ```

4. **Create Virtual Environment**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Configure PostgreSQL**
   ```bash
   sudo -u postgres createdb tabarato
   sudo -u postgres createuser tabarato_user
   sudo -u postgres psql
   ```
   
   In PostgreSQL:
   ```sql
   -- IMPORTANTE: Use uma senha FORTE!
   -- Gere uma senha segura com: openssl rand -base64 32
   ALTER USER tabarato_user WITH PASSWORD 'SUBSTITUA_POR_SENHA_FORTE_AQUI';
   GRANT ALL PRIVILEGES ON DATABASE tabarato TO tabarato_user;
   \q
   ```

6. **Configure Environment**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your values
   ```

7. **Create Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/economizap-bot.service
   ```
   
   Content:
   ```ini
   [Unit]
   Description=EconomiZap Telegram Bot
   After=network.target

   [Service]
   Type=simple
   User=your-user
   WorkingDirectory=/path/to/economizap-bot
   Environment="PATH=/path/to/economizap-bot/venv/bin"
   ExecStart=/path/to/economizap-bot/venv/bin/python src/main.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

8. **Start Service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable tabarato-bot
   sudo systemctl start tabarato-bot
   sudo systemctl status tabarato-bot
   ```

---

### Option 4: Docker

**Steps:**

1. **Build Image**
   ```bash
   docker build -t economizap-bot .
   ```

2. **Run Container**
   ```bash
   docker run -d \
     --name economizap-bot \
     --env-file .env \
     economizap-bot
   ```

3. **With Docker Compose**
   
   Create `docker-compose.yml`:
   ```yaml
   version: '3.8'
   
   services:
     bot:
       build: .
       env_file: .env
       depends_on:
         - db
       restart: unless-stopped
     
     db:
       image: postgres:14
       environment:
         POSTGRES_DB: tabarato
         POSTGRES_USER: tabarato_user
         POSTGRES_PASSWORD: your_password
       volumes:
         - postgres_data:/var/lib/postgresql/data
   
   volumes:
     postgres_data:
   ```
   
   Run:
   ```bash
   docker-compose up -d
   ```

---

## 🔧 Post-Deployment

### 1. Verify Bot is Running

Send `/start` to your bot in Telegram.

### 2. Test Functionality

- Search for a product
- Check `/stats`
- Verify database is saving searches

### 3. Monitor Logs

**Railway:**
- Check deployment logs in dashboard

**VPS:**
```bash
sudo journalctl -u economizap-bot -f
```

**Docker:**
```bash
docker logs -f economizap-bot
```

### 4. Set Up Monitoring (Optional)

- Use Railway metrics
- Set up UptimeRobot for health checks
- Configure error notifications

---

## 💰 Cost Estimates

### Free Tier Options

**Railway:**
- Free: 500 hours/month
- Enough for 1 bot running 24/7

**Heroku:**
- Free tier discontinued
- Eco plan: $5/month

**VPS:**
- DigitalOcean: $4-6/month (smallest droplet)
- AWS Free Tier: 12 months free

### Recommended for Production

**Railway Pro:**
- $5/month
- More resources
- Better for production

---

## 🔒 Security Checklist

- [ ] Never commit `.env` file
- [ ] Use strong database passwords
- [ ] Enable 2FA on deployment platform
- [ ] Regularly update dependencies
- [ ] Monitor logs for suspicious activity
- [ ] Use environment variables for all secrets

---

## 📊 Scaling

### When to Scale

- Bot becomes slow
- Many concurrent users
- Database queries slow

### How to Scale

**Railway:**
- Upgrade plan for more resources
- Add read replicas for database

**VPS:**
- Upgrade server size
- Use load balancer for multiple instances

---

## 🆘 Troubleshooting

### Bot Not Starting

1. Check logs for errors
2. Verify environment variables
3. Test database connection
4. Check Telegram token is valid

### Database Connection Failed

1. Verify `DATABASE_URL` is correct
2. Check database is running
3. Test connection manually
4. Check firewall rules

### Bot Responds Slowly

1. Check server resources
2. Optimize database queries
3. Add caching
4. Scale up resources

---

## 📝 Maintenance

### Regular Tasks

- **Weekly:** Check logs for errors
- **Monthly:** Update dependencies
- **Quarterly:** Review and optimize database

### Updates

```bash
# Pull latest code
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart bot
sudo systemctl restart economizap-bot  # VPS
# or redeploy on Railway
```

---

## ✅ Success Criteria

Your deployment is successful when:

- ✅ Bot responds to `/start`
- ✅ Searches return results
- ✅ Database saves search history
- ✅ `/stats` shows data
- ✅ No errors in logs
- ✅ Bot runs 24/7 without crashes
