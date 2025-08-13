import discord
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

async def setup_events(bot: commands.Bot):
    """Setup event handlers for the bot"""
    
    @bot.event
    async def on_ready():
        """Event triggered when bot is ready"""
        logger.info(f'{bot.user} has connected to Discord!')
        logger.info(f'Bot is in {len(bot.guilds)} guilds')
        
        # Set bot activity status
        activity = discord.Game(name="Type !help for commands")
        await bot.change_presence(activity=activity)
        
        # Sync slash commands
        try:
            synced = await bot.tree.sync()
            logger.info(f"Synced {len(synced)} slash commands")
        except Exception as e:
            logger.error(f"Failed to sync slash commands: {e}")

    @bot.event
    async def on_guild_join(guild):
        """Event triggered when bot joins a guild"""
        logger.info(f'Bot joined guild: {guild.name} (ID: {guild.id})')
        
        # Send welcome message to the first available text channel
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                embed = discord.Embed(
                    title="Hello! 👋",
                    description=f"Thanks for adding me to **{guild.name}**!\n\nType `!help` to see available commands or use `/` for slash commands.",
                    color=0x00ff00
                )
                embed.add_field(
                    name="Quick Start",
                    value="• Use `!ping` to test if I'm working\n• Use `!hello` to get a greeting\n• Use `/ping` for slash command version",
                    inline=False
                )
                try:
                    await channel.send(embed=embed)
                    break
                except discord.Forbidden:
                    continue

    @bot.event
    async def on_message(message):
        """Event triggered when a message is sent"""
        # Ignore messages from the bot itself
        if message.author == bot.user:
            return
            
        # Log messages for debugging (optional)
        logger.debug(f"Message from {message.author}: {message.content}")
        
        # Process commands
        await bot.process_commands(message)

    @bot.event
    async def on_command_error(ctx, error):
        """Event triggered when a command error occurs"""
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title="Command Not Found ❌",
                description=f"The command `{ctx.invoked_with}` doesn't exist. Type `!help` to see available commands.",
                color=0xff0000
            )
            await ctx.send(embed=embed, delete_after=10)
            
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Missing Arguments ❌",
                description=f"You're missing required arguments for this command.\nUsage: `{ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}`",
                color=0xff0000
            )
            await ctx.send(embed=embed, delete_after=15)
            
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Missing Permissions ❌",
                description="You don't have the required permissions to use this command.",
                color=0xff0000
            )
            await ctx.send(embed=embed, delete_after=10)
            
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                title="Bot Missing Permissions ❌",
                description="I don't have the required permissions to execute this command.",
                color=0xff0000
            )
            await ctx.send(embed=embed, delete_after=10)
            
        else:
            # Log unexpected errors
            logger.error(f"Unexpected error in command {ctx.command}: {error}")
            embed = discord.Embed(
                title="An Error Occurred ❌",
                description="An unexpected error occurred while processing your command. Please try again later.",
                color=0xff0000
            )
            await ctx.send(embed=embed, delete_after=10)

    @bot.event
    async def on_disconnect():
        """Event triggered when bot disconnects"""
        logger.warning("Bot disconnected from Discord")

    @bot.event
    async def on_resumed():
        """Event triggered when bot resumes connection"""
        logger.info("Bot resumed connection to Discord")

    logger.info("Event handlers setup complete")
