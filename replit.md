# Discord Bot Project

## Overview

This is a Python-based Discord bot built using the discord.py library. The bot provides basic command handling capabilities with both traditional prefix commands (e.g., `!command`) and modern slash commands (e.g., `/command`). It includes fundamental features like ping/latency checking, greeting commands, server information, fun commands (dice roll, coin flip), and comprehensive error handling with detailed logging.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Bot Framework Architecture
- **Core Framework**: Built on discord.py library with commands extension for structured command handling
- **Command System**: Dual command support using both prefix commands (`!`) and slash commands (`/`) for maximum compatibility
- **Event-Driven Design**: Modular event handling system for bot lifecycle events (ready, guild join, etc.)

### Code Organization
- **Modular Structure**: Code is organized into separate modules (`bot/commands.py`, `bot/events.py`) for maintainability
- **Main Entry Point**: `main.py` serves as the application entry point with centralized bot initialization
- **Configuration Management**: Environment-based configuration using `.env` files for secure token storage

### Discord Integration
- **Intent Management**: Configured with necessary Discord intents (message_content, guilds, guild_messages) for proper functionality
- **Permission Handling**: Implements proper permission checking before sending messages or performing actions
- **Rich Messaging**: Uses Discord embeds for enhanced visual presentation of bot responses

### Error Handling & Logging
- **Comprehensive Logging**: Structured logging system using Python's logging module for debugging and monitoring
- **Exception Management**: Proper error handling for Discord API failures, authentication issues, and network problems
- **Graceful Degradation**: Bot continues operating even when individual commands fail

### Bot Features
- **Latency Monitoring**: Real-time API and WebSocket latency measurement for performance monitoring
- **Auto-sync Commands**: Automatic synchronization of slash commands with Discord on bot startup
- **Dynamic Status**: Configurable bot presence and activity status
- **Welcome System**: Automated welcome messages when joining new servers
- **Contribution Tracking**: Database-powered system for logging and tracking guild member contributions with material autocomplete
- **Leaderboards**: View top contributors and detailed contribution breakdowns per member
- **AI Conversations**: OpenAI-powered `/ask` command with cost controls including daily usage limits (25 per user, 500 per server), prompt trimming, and token limits using gpt-4o-mini model

## External Dependencies

### Core Dependencies
- **discord.py**: Primary Discord API wrapper library for bot functionality
- **python-dotenv**: Environment variable management for secure configuration
- **asyncio**: Asynchronous programming support for Discord's async API
- **sqlalchemy**: Database ORM for contribution tracking and data persistence
- **psycopg2-binary**: PostgreSQL database adapter for Python
- **openai**: OpenAI API client for AI conversation features

### Discord API Integration
- **Discord Developer Portal**: Bot token and application management
- **Discord Gateway**: Real-time event streaming and bot presence
- **Discord REST API**: Command registration and message sending

### Configuration Requirements
- **Environment Variables**: Discord bot token, OpenAI API key, and configuration settings via `.env` file
- **Discord Permissions**: Requires specific bot permissions (Send Messages, Use Slash Commands, Read Message History, Embed Links, Add Reactions)
- **Gateway Intents**: Message Content Intent enabled for reading message content
- **AI Cost Controls**: Built-in usage tracking with configurable daily limits (DAILY_USER_LIMIT=25, DAILY_SERVER_LIMIT=500), input trimming (MAX_INPUT_CHARS=4000), output token limits (MAX_OUTPUT_TOKENS=600), and cost-effective model selection (gpt-4o-mini)