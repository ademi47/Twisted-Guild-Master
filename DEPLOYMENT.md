# Deployment Guide

This guide covers deploying your Discord bot to various platforms with PostgreSQL database integration.

## Quick Deploy to Railway (Recommended)

Railway offers the simplest deployment with built-in PostgreSQL:

### Step 1: Prepare Repository
1. Fork this repository to your GitHub account
2. Ensure all files are committed and pushed

### Step 2: Deploy to Railway
1. Visit [railway.app](https://railway.app) and sign up with GitHub
2. Click "Deploy from GitHub repo"
3. Select your forked repository
4. Railway will automatically detect the `railway.json` and start building

### Step 3: Add Database
1. In your Railway dashboard, click "Add Service"
2. Select "Database" → "PostgreSQL"
3. Railway automatically sets the `DATABASE_URL` environment variable

### Step 4: Configure Environment Variables
1. Go to your bot service → "Variables" tab
2. Add required variables:
   ```
   DISCORD_TOKEN=your_discord_bot_token_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Step 5: Deploy
- Railway automatically builds and deploys
- Check logs for "Bot is in X guilds" and "Synced X commands"
- Your bot is now live!

## Deploy to Heroku

### Prerequisites
- Heroku CLI installed
- Git repository

### Steps
1. **Create Heroku app**:
   ```bash
   heroku create your-discord-bot-name
   ```

2. **Add PostgreSQL addon**:
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

3. **Set environment variables**:
   ```bash
   heroku config:set DISCORD_TOKEN=your_token_here
   heroku config:set OPENAI_API_KEY=your_openai_key_here
   ```

4. **Create Procfile**:
   ```bash
   echo "worker: python main.py" > Procfile
   ```

5. **Deploy**:
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

6. **Scale worker**:
   ```bash
   heroku ps:scale worker=1
   ```

## Deploy with Docker

### Option 1: Docker Compose (includes PostgreSQL)

1. **Clone repository**:
   ```bash
   git clone <your-repo-url>
   cd discord-bot
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your tokens
   ```

3. **Start services**:
   ```bash
   docker-compose up -d
   ```

4. **Check logs**:
   ```bash
   docker-compose logs bot
   ```

### Option 2: Docker with External Database

1. **Build image**:
   ```bash
   docker build -t discord-bot .
   ```

2. **Run container**:
   ```bash
   docker run -d \
     --name discord-bot \
     --env-file .env \
     discord-bot
   ```

## VPS/Cloud Server Deployment

### Ubuntu/Debian Server

1. **Update system**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install dependencies**:
   ```bash
   sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib git -y
   ```

3. **Setup PostgreSQL**:
   ```bash
   sudo -u postgres psql
   CREATE DATABASE discord_bot;
   CREATE USER bot_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE discord_bot TO bot_user;
   \q
   ```

4. **Clone and setup bot**:
   ```bash
   git clone <your-repo-url>
   cd discord-bot
   python3 -m venv venv
   source venv/bin/activate
   pip install discord.py python-dotenv sqlalchemy psycopg2-binary openai
   ```

5. **Configure environment**:
   ```bash
   cp .env.example .env
   nano .env
   # Add your tokens and database URL
   ```

6. **Test run**:
   ```bash
   python main.py
   ```

7. **Setup systemd service**:
   ```bash
   sudo nano /etc/systemd/system/discord-bot.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Discord Bot
   After=network.target

   [Service]
   Type=simple
   User=your-username
   WorkingDirectory=/home/your-username/discord-bot
   Environment=PATH=/home/your-username/discord-bot/venv/bin
   ExecStart=/home/your-username/discord-bot/venv/bin/python main.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

8. **Enable and start service**:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable discord-bot
   sudo systemctl start discord-bot
   sudo systemctl status discord-bot
   ```

## Environment Variables Reference

### Required Variables
```env
DISCORD_TOKEN=your_discord_bot_token
DATABASE_URL=postgresql://username:password@host:port/database_name
```

### Optional Variables
```env
OPENAI_API_KEY=your_openai_api_key
BOT_PREFIX=!
LOG_LEVEL=INFO
DAILY_USER_LIMIT=25
DAILY_SERVER_LIMIT=500
MAX_INPUT_CHARS=4000
MAX_OUTPUT_TOKENS=600
```

## Database Setup Options

### Cloud PostgreSQL Providers

1. **Railway** (Recommended)
   - Built-in PostgreSQL with Railway deployment
   - Automatic DATABASE_URL configuration
   - $5/month for 1GB storage

2. **Heroku Postgres**
   - Mini plan: Free (10,000 rows)
   - Basic plan: $9/month (10M rows)

3. **AWS RDS**
   - db.t3.micro: ~$13/month
   - Requires VPC configuration

4. **Google Cloud SQL**
   - db-f1-micro: ~$7/month
   - Easy integration with GCP

5. **Supabase**
   - Free tier: 500MB storage
   - Pro: $25/month

### Self-hosted Options

1. **DigitalOcean Droplet** with PostgreSQL
2. **AWS EC2** with RDS or self-managed PostgreSQL
3. **Google Compute Engine** with Cloud SQL
4. **Local server** with PostgreSQL

## Monitoring and Maintenance

### Health Checks
```bash
# Check bot status
docker logs discord-bot

# Check database connection
docker exec -it postgres_container psql -U postgres -d discord_bot -c "SELECT COUNT(*) FROM guilds;"

# Monitor system resources
htop
```

### Log Management
```bash
# View recent logs
journalctl -u discord-bot -f

# Rotate logs
sudo logrotate -f /etc/logrotate.conf
```

### Backup Database
```bash
# Create backup
pg_dump postgresql://user:pass@host:port/discord_bot > backup.sql

# Restore backup
psql postgresql://user:pass@host:port/discord_bot < backup.sql
```

## Troubleshooting

### Common Deployment Issues

1. **Bot doesn't start**:
   - Check DISCORD_TOKEN is valid
   - Verify DATABASE_URL format
   - Review logs for specific errors

2. **Database connection fails**:
   - Test connection: `psql $DATABASE_URL`
   - Check firewall rules
   - Verify database exists

3. **Commands don't sync**:
   - Bot needs "applications.commands" scope
   - Check Discord permissions
   - Restart bot after code changes

4. **Memory issues**:
   - Monitor memory usage: `free -h`
   - Consider upgrading server plan
   - Optimize database queries

### Performance Optimization

1. **Database indexing**:
   ```sql
   CREATE INDEX idx_contributions_guild_member ON contributions(guild_id, member_id);
   CREATE INDEX idx_contributions_created_at ON contributions(created_at);
   ```

2. **Memory management**:
   - Use connection pooling
   - Implement query pagination
   - Cache frequent lookups

3. **Monitoring**:
   - Set up health check endpoints
   - Monitor database performance
   - Track bot response times

## Security Considerations

1. **Environment Variables**:
   - Never commit `.env` files
   - Use secrets management in production
   - Rotate tokens regularly

2. **Database Security**:
   - Use strong passwords
   - Enable SSL connections
   - Restrict network access

3. **Bot Permissions**:
   - Follow principle of least privilege
   - Regularly audit bot permissions
   - Monitor command usage

## Scaling

### Horizontal Scaling
- Use database connection pooling
- Implement Redis for caching
- Consider sharding for large deployments

### Vertical Scaling
- Monitor CPU and memory usage
- Upgrade server resources as needed
- Optimize database queries

For additional support, check the main README.md or open an issue in the repository.