# Discord Bot with Contribution Tracking

A Python Discord bot with advanced database-integrated contribution tracking and AI-powered interaction capabilities, designed to provide robust guild member resource management with intelligent error handling.

## Features

- **Modern Discord Integration**: Slash commands (`/command`) with full autocomplete support
- **Contribution Tracking**: Advanced material contribution system with 29+ materials and autocomplete
- **Points-Based Ranking**: Sophisticated leaderboard system with material-specific point values  
- **Database Integration**: PostgreSQL with SQLAlchemy ORM supporting unlimited contribution amounts
- **AI Conversations**: OpenAI-powered `/ask` command with cost controls and usage quotas
- **Rich User Interface**: Discord embeds with detailed statistics and formatted displays
- **Comprehensive Error Handling**: Robust error management with detailed logging
- **Scalable Architecture**: Modular design supporting large-scale guild management

## Tech Stack

- **Discord.py** - Discord API wrapper and bot framework
- **Python 3.11** - Core programming language
- **PostgreSQL** - Database for persistent data storage
- **SQLAlchemy** - Object-relational mapping (ORM)
- **OpenAI API** - AI conversation capabilities
- **psycopg2** - PostgreSQL database adapter

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL database
- Discord bot token
- OpenAI API key (optional, for AI features)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd discord-bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your configuration:
   ```env
   DISCORD_TOKEN=your_discord_bot_token
   DATABASE_URL=postgresql://username:password@localhost:5432/database_name
   OPENAI_API_KEY=your_openai_api_key_optional
   ```

4. **Initialize the database**:
   ```bash
   python main.py
   ```
   The bot will automatically create all necessary database tables on first run.

5. **Invite bot to your server**:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Select your application → OAuth2 → URL Generator
   - Select scopes: `bot`, `applications.commands`
   - Select permissions: `Send Messages`, `Use Slash Commands`, `Read Message History`, `Embed Links`
   - Use the generated URL to invite your bot

## Discord Bot Setup

### 1. Create Discord Application

1. Visit [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and name your bot
3. Navigate to "Bot" section and click "Add Bot"
4. Copy the bot token for your `.env` file
5. Enable "Message Content Intent" under Privileged Gateway Intents

### 2. Bot Permissions Required

- Send Messages
- Use Slash Commands  
- Read Message History
- Embed Links
- Add Reactions
- Use External Emojis

## Database Setup

### PostgreSQL Configuration

The bot requires a PostgreSQL database. You can use:

**Local PostgreSQL**:
```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib

# Create database
sudo -u postgres psql
CREATE DATABASE discord_bot;
CREATE USER bot_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE discord_bot TO bot_user;
```

**Cloud PostgreSQL**:
- Heroku Postgres
- AWS RDS
- Google Cloud SQL
- Railway.app
- Supabase

### Environment Variables

Required variables in `.env`:

```env
# Required
DISCORD_TOKEN=your_discord_bot_token
DATABASE_URL=postgresql://username:password@host:port/database_name

# Optional  
OPENAI_API_KEY=your_openai_api_key
DAILY_USER_LIMIT=25
DAILY_SERVER_LIMIT=500
MAX_INPUT_CHARS=4000
MAX_OUTPUT_TOKENS=600
```

## Available Commands

### Core Commands
- `/ping` - Check bot latency and connection status
- `/hello` - Get a random greeting message (100+ variations)
- `/userinfo [@user]` - Display detailed user information

### Contribution System
- `/contribute [material] [amount]` - Add material contributions with autocomplete
- `/contributions [@user]` - View contribution statistics and total points
- `/leaderboard` - Display top contributors with points ranking

### AI Features
- `/ask [question]` - AI-powered conversations with usage limits
- `/testdb` - Database connection test (admin use)

### Material Categories
The bot supports 29+ materials across categories:
- **Ores**: Coal, Iron, Gold, Diamond, Netherite, etc.
- **Building**: Stone, Wood, Obsidian, etc.  
- **Food**: Bread, Cooked Beef, Golden Apple, etc.
- **Special**: Emerald, Ender Pearl, Nether Star, etc.

## Deployment Options

### Option 1: Railway.app (Recommended)

Railway provides simple deployment with built-in PostgreSQL:

1. **Fork this repository** to your GitHub
2. **Connect to Railway**:
   - Visit [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "Deploy from GitHub repo"
   - Select your forked repository
3. **Add PostgreSQL**:
   - Click "Add Service" → "Database" → "PostgreSQL"
   - Railway automatically sets DATABASE_URL
4. **Configure environment variables**:
   - Go to your service → Variables
   - Add `DISCORD_TOKEN` with your bot token
   - Add `OPENAI_API_KEY` (optional)
5. **Deploy**: Railway automatically builds and deploys

### Option 2: Heroku

1. **Create Heroku app**:
   ```bash
   heroku create your-bot-name
   ```

2. **Add PostgreSQL addon**:
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

3. **Set environment variables**:
   ```bash
   heroku config:set DISCORD_TOKEN=your_token
   heroku config:set OPENAI_API_KEY=your_key
   ```

4. **Deploy**:
   ```bash
   git push heroku main
   ```

### Option 3: Docker

1. **Using Docker Compose** (includes PostgreSQL):
   ```bash
   docker-compose up -d
   ```

2. **Using Docker only**:
   ```bash
   docker build -t discord-bot .
   docker run -d --env-file .env discord-bot
   ```

### Option 4: VPS/Cloud Server

1. **Clone and setup**:
   ```bash
   git clone <your-repo>
   cd discord-bot
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **Setup PostgreSQL and configure .env**

3. **Run with process manager**:
   ```bash
   # Using PM2
   npm install -g pm2
   pm2 start "python main.py" --name discord-bot
   
   # Using systemd (Linux)
   sudo systemctl enable discord-bot.service
   sudo systemctl start discord-bot
   ```

## Database Schema

The bot automatically creates these tables:

- **guilds**: Discord server information
- **members**: Guild member data  
- **materials**: Available materials with point values
- **contributions**: Member contribution records
- **ai_usage**: Daily AI command usage tracking

### Key Features:
- **Unlimited Contributions**: Uses PostgreSQL NUMERIC for virtually unlimited amounts
- **Material Points**: Each material has specific point values for fair ranking
- **Usage Tracking**: Built-in AI cost controls and daily limits
- **Auto-sync**: Slash commands automatically sync with Discord

## Development

### Running Locally

1. **Setup environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your tokens
   ```

2. **Install dependencies**:
   ```bash
   pip install discord.py python-dotenv sqlalchemy psycopg2-binary openai
   ```

3. **Run the bot**:
   ```bash
   python main.py
   ```

### Project Structure

```
discord-bot/
├── main.py              # Bot entry point and initialization
├── bot/
│   ├── commands.py      # Slash command implementations  
│   └── events.py        # Discord event handlers
├── models.py            # Database models and schema
├── database.py          # Database operations and queries
├── ai_service.py        # OpenAI integration and cost controls
├── .env.example         # Environment template
├── Dockerfile           # Container deployment
├── docker-compose.yml   # Local development with PostgreSQL
└── README.md           # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit: `git commit -m "Add feature description"`
5. Push: `git push origin feature-name`
6. Create a Pull Request

## Troubleshooting

### Common Issues

**Bot not responding to slash commands**:
- Ensure bot has "Use Slash Commands" permission
- Check that commands are synced (bot logs show "Synced X commands")
- Verify bot is online and connected

**Database connection errors**:
- Verify DATABASE_URL format: `postgresql://user:pass@host:port/db`
- Ensure PostgreSQL is running and accessible
- Check firewall settings for database port

**Material autocomplete not working**:
- Database must be initialized (run bot once to create tables)
- Check bot logs for material loading messages
- Verify database contains material data

**AI features not working**:
- Add valid OPENAI_API_KEY to environment variables
- Check daily usage limits haven't been exceeded
- Verify API key has sufficient credits

### Support

- **Issues**: Open a GitHub issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Discord**: Join our support server (link in repository)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
   