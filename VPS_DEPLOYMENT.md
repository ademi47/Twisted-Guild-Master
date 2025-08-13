# VPS Deployment Guide for Discord Bot

This guide walks you through deploying your Discord bot to a Virtual Private Server (VPS) with PostgreSQL database.

## Prerequisites

- Ubuntu/Debian VPS with root access
- Domain name (optional, for reverse proxy)
- Basic SSH knowledge

## Step 1: Initial Server Setup

### Connect to your VPS
```bash
ssh root@your-server-ip
# or
ssh your-username@your-server-ip
```

### Update system packages
```bash
sudo apt update && sudo apt upgrade -y
```

### Install required packages
```bash
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    postgresql \
    postgresql-contrib \
    git \
    nginx \
    ufw \
    htop \
    curl \
    wget
```

## Step 2: Setup PostgreSQL Database

### Start PostgreSQL service
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Create database and user
```bash
sudo -u postgres psql
```

In PostgreSQL shell:
```sql
CREATE DATABASE discord_bot;
CREATE USER bot_user WITH PASSWORD 'your_secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE discord_bot TO bot_user;
ALTER USER bot_user CREATEDB;
\q
```

### Test database connection
```bash
psql -h localhost -U bot_user -d discord_bot
# Enter password when prompted
# Type \q to exit
```

## Step 3: Clone and Setup Bot

### Create bot user (security best practice)
```bash
sudo adduser botuser
sudo usermod -aG sudo botuser
sudo su - botuser
```

### Clone your repository
```bash
git clone https://github.com/your-username/your-bot-repo.git
cd your-bot-repo
```

### Create Python virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Python dependencies
```bash
pip install --upgrade pip
pip install discord.py python-dotenv sqlalchemy psycopg2-binary openai
```

## Step 4: Configure Environment

### Create environment file
```bash
cp .env.example .env
nano .env
```

### Add your configuration
```env
# Required
DISCORD_TOKEN=your_discord_bot_token_here
DATABASE_URL=postgresql://bot_user:your_secure_password_here@localhost:5432/discord_bot

# Optional
OPENAI_API_KEY=your_openai_api_key_here
BOT_PREFIX=!
LOG_LEVEL=INFO
DAILY_USER_LIMIT=25
DAILY_SERVER_LIMIT=500
MAX_INPUT_CHARS=4000
MAX_OUTPUT_TOKENS=600
```

### Test bot startup
```bash
python main.py
```

You should see:
```
INFO:__main__:Database initialized successfully
INFO:bot.events:Bot is in X guilds
INFO:bot.events:Synced 8 slash commands
```

Press `Ctrl+C` to stop the test.

## Step 5: Create Systemd Service

### Create service file
```bash
sudo nano /etc/systemd/system/discord-bot.service
```

### Add service configuration
```ini
[Unit]
Description=Discord Bot with Contribution Tracking
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=simple
User=botuser
Group=botuser
WorkingDirectory=/home/botuser/your-bot-repo
Environment=PATH=/home/botuser/your-bot-repo/venv/bin
ExecStart=/home/botuser/your-bot-repo/venv/bin/python main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=discord-bot

[Install]
WantedBy=multi-user.target
```

### Enable and start service
```bash
sudo systemctl daemon-reload
sudo systemctl enable discord-bot
sudo systemctl start discord-bot
```

### Check service status
```bash
sudo systemctl status discord-bot
```

### View logs
```bash
sudo journalctl -u discord-bot -f
```

## Step 6: Setup Firewall

### Configure UFW firewall
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### Check firewall status
```bash
sudo ufw status
```

## Step 7: Setup Log Rotation

### Create logrotate configuration
```bash
sudo nano /etc/logrotate.d/discord-bot
```

### Add log rotation rules
```
/var/log/discord-bot.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 0644 botuser botuser
    postrotate
        systemctl reload discord-bot
    endscript
}
```

## Step 8: Setup Monitoring (Optional)

### Create monitoring script
```bash
nano /home/botuser/monitor-bot.sh
```

### Add monitoring content
```bash
#!/bin/bash

# Check if bot service is running
if ! systemctl is-active --quiet discord-bot; then
    echo "$(date): Discord bot is not running, attempting to restart..." >> /var/log/bot-monitor.log
    sudo systemctl restart discord-bot
fi

# Check memory usage
MEMORY_USAGE=$(ps aux | grep "python main.py" | grep -v grep | awk '{print $4}')
if [ ! -z "$MEMORY_USAGE" ] && (( $(echo "$MEMORY_USAGE > 80" | bc -l) )); then
    echo "$(date): High memory usage detected: $MEMORY_USAGE%" >> /var/log/bot-monitor.log
fi
```

### Make script executable
```bash
chmod +x /home/botuser/monitor-bot.sh
```

### Add to crontab (runs every 5 minutes)
```bash
crontab -e
```

Add line:
```
*/5 * * * * /home/botuser/monitor-bot.sh
```

## Step 9: Database Backup Setup

### Create backup script
```bash
nano /home/botuser/backup-db.sh
```

### Add backup content
```bash
#!/bin/bash

BACKUP_DIR="/home/botuser/db-backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="discord_bot"
DB_USER="bot_user"

# Create backup directory
mkdir -p $BACKUP_DIR

# Create backup
pg_dump -h localhost -U $DB_USER -d $DB_NAME > $BACKUP_DIR/discord_bot_$DATE.sql

# Keep only last 7 days of backups
find $BACKUP_DIR -name "discord_bot_*.sql" -mtime +7 -delete

echo "$(date): Database backup completed: discord_bot_$DATE.sql" >> /var/log/db-backup.log
```

### Make script executable
```bash
chmod +x /home/botuser/backup-db.sh
```

### Add daily backup to crontab
```bash
crontab -e
```

Add line:
```
0 2 * * * /home/botuser/backup-db.sh
```

## Step 10: SSL and Domain Setup (Optional)

If you want to add a web interface or webhook endpoint:

### Install Certbot
```bash
sudo apt install certbot python3-certbot-nginx
```

### Setup Nginx reverse proxy
```bash
sudo nano /etc/nginx/sites-available/discord-bot
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Enable site and get SSL
```bash
sudo ln -s /etc/nginx/sites-available/discord-bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
sudo certbot --nginx -d your-domain.com
```

## Management Commands

### Service Management
```bash
# Start bot
sudo systemctl start discord-bot

# Stop bot
sudo systemctl stop discord-bot

# Restart bot
sudo systemctl restart discord-bot

# Check status
sudo systemctl status discord-bot

# View logs
sudo journalctl -u discord-bot -f

# View recent logs
sudo journalctl -u discord-bot --since "1 hour ago"
```

### Database Management
```bash
# Connect to database
psql -h localhost -U bot_user -d discord_bot

# View tables
\dt

# Check contributions
SELECT COUNT(*) FROM contributions;

# View materials
SELECT * FROM materials;
```

### Bot Updates
```bash
# Navigate to bot directory
cd /home/botuser/your-bot-repo

# Pull latest changes
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install any new dependencies
pip install -r requirements.txt

# Restart bot service
sudo systemctl restart discord-bot

# Check logs
sudo journalctl -u discord-bot -f
```

## Troubleshooting

### Bot won't start
```bash
# Check service status
sudo systemctl status discord-bot

# Check logs for errors
sudo journalctl -u discord-bot --since "10 minutes ago"

# Test bot manually
cd /home/botuser/your-bot-repo
source venv/bin/activate
python main.py
```

### Database connection issues
```bash
# Test database connection
psql -h localhost -U bot_user -d discord_bot

# Check PostgreSQL status
sudo systemctl status postgresql

# Restart PostgreSQL
sudo systemctl restart postgresql
```

### Memory issues
```bash
# Check memory usage
free -h
htop

# Check bot memory usage
ps aux | grep python

# Restart bot if needed
sudo systemctl restart discord-bot
```

### Permission issues
```bash
# Fix file permissions
sudo chown -R botuser:botuser /home/botuser/your-bot-repo

# Fix service permissions
sudo chmod 644 /etc/systemd/system/discord-bot.service
sudo systemctl daemon-reload
```

## Security Best Practices

1. **Regular Updates**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Monitor Logs**:
   ```bash
   sudo tail -f /var/log/auth.log
   sudo journalctl -u discord-bot -f
   ```

3. **Backup Configuration**:
   ```bash
   # Backup environment file
   cp .env .env.backup
   
   # Backup service file
   sudo cp /etc/systemd/system/discord-bot.service /home/botuser/
   ```

4. **Monitor Failed Login Attempts**:
   ```bash
   sudo grep "Failed password" /var/log/auth.log
   ```

## Performance Optimization

### Database Optimization
```sql
-- Connect to database
psql -h localhost -U bot_user -d discord_bot

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_contributions_guild_member ON contributions(guild_id, member_id);
CREATE INDEX IF NOT EXISTS idx_contributions_created_at ON contributions(created_at);
CREATE INDEX IF NOT EXISTS idx_materials_name ON materials(name);

-- Check database size
SELECT pg_size_pretty(pg_database_size('discord_bot'));
```

### System Monitoring
```bash
# Monitor system resources
htop

# Check disk usage
df -h

# Monitor network connections
netstat -tulnp | grep python
```

Your Discord bot is now deployed and running on your VPS with professional monitoring, backup, and security configurations!