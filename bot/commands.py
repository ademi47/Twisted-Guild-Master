import discord
from discord.ext import commands
from discord import app_commands
import random
import time
import logging

logger = logging.getLogger(__name__)

async def setup_commands(bot: commands.Bot):
    """Setup commands for the bot"""
    
    # ==================== PREFIX COMMANDS ====================
    
    @bot.command(name='hello', help='Get a friendly greeting from the bot')
    async def hello(ctx):
        """Simple hello command"""
        greetings = [
            f"Hello there, {ctx.author.mention}! 👋",
            f"Hi {ctx.author.mention}! How are you doing? 😊",
            f"Greetings, {ctx.author.mention}! Nice to see you! 🎉",
            f"Hey {ctx.author.mention}! Hope you're having a great day! ✨"
        ]
        
        embed = discord.Embed(
            description=random.choice(greetings),
            color=0x00ff00
        )
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @bot.command(name='ping', help='Check the bot\'s latency')
    async def ping(ctx):
        """Ping command to check bot latency"""
        start_time = time.time()
        message = await ctx.send("🏓 Pinging...")
        end_time = time.time()
        
        # Calculate latencies
        api_latency = round((end_time - start_time) * 1000)
        websocket_latency = round(bot.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 Pong!",
            color=0x00ff00
        )
        embed.add_field(name="API Latency", value=f"{api_latency}ms", inline=True)
        embed.add_field(name="WebSocket Latency", value=f"{websocket_latency}ms", inline=True)
        
        # Add status indicator based on latency
        if websocket_latency < 100:
            embed.add_field(name="Status", value="🟢 Excellent", inline=True)
        elif websocket_latency < 200:
            embed.add_field(name="Status", value="🟡 Good", inline=True)
        else:
            embed.add_field(name="Status", value="🔴 Poor", inline=True)
            
        await message.edit(content="", embed=embed)

    @bot.command(name='serverinfo', help='Get information about the current server')
    async def serverinfo(ctx):
        """Get server information"""
        if ctx.guild is None:
            await ctx.send("This command can only be used in a server!")
            return
            
        guild = ctx.guild
        
        embed = discord.Embed(
            title=f"📊 {guild.name} Server Information",
            color=0x0099ff
        )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
            
        embed.add_field(name="👑 Owner", value=guild.owner.mention if guild.owner else "Unknown", inline=True)
        embed.add_field(name="🆔 Server ID", value=guild.id, inline=True)
        embed.add_field(name="📅 Created", value=guild.created_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="👥 Members", value=guild.member_count, inline=True)
        embed.add_field(name="💬 Text Channels", value=len(guild.text_channels), inline=True)
        embed.add_field(name="🔊 Voice Channels", value=len(guild.voice_channels), inline=True)
        embed.add_field(name="😀 Emojis", value=len(guild.emojis), inline=True)
        embed.add_field(name="📋 Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="🚀 Boost Level", value=guild.premium_tier, inline=True)
        
        await ctx.send(embed=embed)

    @bot.command(name='userinfo', help='Get information about a user')
    async def userinfo(ctx, member: discord.Member = None):
        """Get user information"""
        if member is None:
            member = ctx.author
            
        embed = discord.Embed(
            title=f"👤 {member.display_name} Information",
            color=member.color if hasattr(member, 'color') and member.color != discord.Color.default() else 0x0099ff
        )
        
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        embed.add_field(name="👤 Username", value=f"{member.name}#{member.discriminator}", inline=True)
        embed.add_field(name="🆔 User ID", value=member.id, inline=True)
        embed.add_field(name="📅 Account Created", value=member.created_at.strftime("%B %d, %Y"), inline=True)
        
        # Only show guild-specific info if member is in the guild
        if ctx.guild and hasattr(member, 'joined_at') and hasattr(member, 'roles'):
            embed.add_field(name="📥 Joined Server", value=member.joined_at.strftime("%B %d, %Y") if member.joined_at else "Unknown", inline=True)
            embed.add_field(name="📋 Roles", value=len(member.roles) - 1, inline=True)  # -1 to exclude @everyone
            embed.add_field(name="🎯 Top Role", value=member.top_role.mention, inline=True)
        
        await ctx.send(embed=embed)

    # ==================== SLASH COMMANDS ====================
    
    @bot.tree.command(name="hello", description="Get a friendly greeting from the bot")
    async def slash_hello(interaction: discord.Interaction):
        """Slash command version of hello"""
        greetings = [
            f"Hello there, {interaction.user.mention}! 👋",
            f"Hi {interaction.user.mention}! How are you doing? 😊",
            f"Greetings, {interaction.user.mention}! Nice to see you! 🎉",
            f"Hey {interaction.user.mention}! Hope you're having a great day! ✨"
        ]
        
        embed = discord.Embed(
            description=random.choice(greetings),
            color=0x00ff00
        )
        embed.set_footer(text=f"Requested by {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="ping", description="Check the bot's latency")
    async def slash_ping(interaction: discord.Interaction):
        """Slash command version of ping"""
        websocket_latency = round(bot.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 Pong!",
            color=0x00ff00
        )
        embed.add_field(name="WebSocket Latency", value=f"{websocket_latency}ms", inline=True)
        
        # Add status indicator based on latency
        if websocket_latency < 100:
            embed.add_field(name="Status", value="🟢 Excellent", inline=True)
        elif websocket_latency < 200:
            embed.add_field(name="Status", value="🟡 Good", inline=True)
        else:
            embed.add_field(name="Status", value="🔴 Poor", inline=True)
            
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="userinfo", description="Get information about a user")
    @app_commands.describe(member="The member to get information about (optional)")
    async def slash_userinfo(interaction: discord.Interaction, member: discord.Member = None):
        """Slash command version of userinfo"""
        if member is None:
            member = interaction.user
            
        embed = discord.Embed(
            title=f"👤 {member.display_name} Information",
            color=member.color if hasattr(member, 'color') and member.color != discord.Color.default() else 0x0099ff
        )
        
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        embed.add_field(name="👤 Username", value=f"{member.name}#{member.discriminator}", inline=True)
        embed.add_field(name="🆔 User ID", value=member.id, inline=True)
        embed.add_field(name="📅 Account Created", value=member.created_at.strftime("%B %d, %Y"), inline=True)
        
        # Only show guild-specific info if member is in the guild
        if interaction.guild and hasattr(member, 'joined_at') and hasattr(member, 'roles'):
            embed.add_field(name="📥 Joined Server", value=member.joined_at.strftime("%B %d, %Y") if member.joined_at else "Unknown", inline=True)
            embed.add_field(name="📋 Roles", value=len(member.roles) - 1, inline=True)  # -1 to exclude @everyone
            embed.add_field(name="🎯 Top Role", value=member.top_role.mention, inline=True)
        
        await interaction.response.send_message(embed=embed)

    # ==================== FUN COMMANDS ====================
    
    @bot.command(name='roll', help='Roll a dice (1-6) or specify sides')
    async def roll(ctx, sides: int = 6):
        """Roll a dice command"""
        if sides < 1:
            await ctx.send("❌ Dice must have at least 1 side!")
            return
        if sides > 1000:
            await ctx.send("❌ Dice can't have more than 1000 sides!")
            return
            
        result = random.randint(1, sides)
        
        embed = discord.Embed(
            title="🎲 Dice Roll",
            description=f"You rolled a **{result}** on a {sides}-sided dice!",
            color=0x9932cc
        )
        embed.set_footer(text=f"Rolled by {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @bot.command(name='coinflip', help='Flip a coin')
    async def coinflip(ctx):
        """Coin flip command"""
        result = random.choice(['Heads', 'Tails'])
        emoji = '🪙' if result == 'Heads' else '🥈'
        
        embed = discord.Embed(
            title="🪙 Coin Flip",
            description=f"{emoji} It's **{result}**!",
            color=0xffd700
        )
        embed.set_footer(text=f"Flipped by {ctx.author.display_name}")
        await ctx.send(embed=embed)

    logger.info("Commands setup complete")
