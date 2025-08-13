import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN', 'your_discord_token_here')
BOT_PREFIX = os.getenv('BOT_PREFIX', '!')

# Create bot instance with intents
intents = discord.Intents.default()
intents.message_content = True  # Required for message content access
intents.guilds = True
intents.guild_messages = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

# Import event handlers and commands
from bot.events import setup_events
from bot.commands import setup_commands

async def main():
    """Main function to start the bot"""
    try:
        # Setup events and commands
        await setup_events(bot)
        await setup_commands(bot)
        
        # Start the bot
        logger.info("Starting Discord bot...")
        await bot.start(DISCORD_TOKEN)
        
    except discord.LoginFailure:
        logger.error("Invalid Discord token provided!")
    except discord.HTTPException as e:
        logger.error(f"HTTP error occurred: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        if not bot.is_closed():
            await bot.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
