# Discord Bot

A Python Discord bot with basic command handling and message interaction capabilities.

## Features

- 🤖 Basic command handling with prefix commands (`!command`)
- ⚡ Modern slash commands (`/command`)
- 🏓 Ping command to check bot latency
- 👋 Greeting commands
- 📊 Server and user information commands
- 🎲 Fun commands (dice roll, coin flip)
- 📈 Contribution tracking system with material autocomplete
- 🏆 Leaderboards and contribution statistics
- 🧠 AI conversations via `/ask` command with cost controls
- 🔧 Comprehensive error handling
- 📝 Detailed logging
- 🎨 Rich embed messages

## Setup Instructions

### 1. Create a Discord Application

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section in the left sidebar
4. Click "Add Bot"
5. Under the "Token" section, click "Copy" to copy your bot token
6. Save this token securely - you'll need it for the configuration

### 2. Configure Bot Permissions

In the Discord Developer Portal:

1. Go to the "Bot" section
2. Enable the following "Privileged Gateway Intents":
   - Message Content Intent (required for reading message content)
3. Go to the "OAuth2" → "URL Generator" section
4. Select "bot" and "applications.commands" scopes
5. Select the following bot permissions:
   - Send Messages
   - Use Slash Commands
   - Read Message History
   - Embed Links
   - Add Reactions
   - Use External Emojis

### 3. Environment Configuration

1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your Discord bot token:
   