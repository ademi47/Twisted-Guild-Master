import discord
from discord.ext import commands
from discord import app_commands
import random
import time
import logging
from database import DatabaseManager
from ai_service import get_ai_service
from typing import List

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

    # ==================== CONTRIBUTION COMMANDS ====================
    
    # Create material choices for the dropdown
    async def get_material_choices() -> List[app_commands.Choice[str]]:
        """Get material choices for the dropdown"""
        try:
            materials = DatabaseManager.get_all_materials()
            choices = []
            for material in materials[:25]:  # Discord limit is 25 choices
                choices.append(app_commands.Choice(
                    name=material['display_name'], 
                    value=material['name']
                ))
            return choices
        except Exception as e:
            logger.error(f"Error getting material choices: {e}")
            return []

    @bot.tree.command(name="testdb", description="Test database connection")
    async def testdb(interaction: discord.Interaction):
        """Test database connection"""
        try:
            materials = DatabaseManager.get_all_materials()
            embed = discord.Embed(
                title="✅ Database Test",
                description=f"Database is working! Found {len(materials)} materials.",
                color=0x00ff00
            )
            material_list = ", ".join([m['display_name'] for m in materials[:5]])
            embed.add_field(name="Sample Materials", value=material_list, inline=False)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Database Error",
                description=f"Database connection failed: {str(e)}",
                color=0xff0000
            )
            await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="contribute", description="Log your contribution to the guild")
    @app_commands.describe(
        material="The material you're contributing",
        amount="The amount you're contributing (must be positive)"
    )
    async def contribute(interaction: discord.Interaction, material: str, amount: int):
        """Log a member's contribution"""
        # Ensure this is used in a guild
        if not interaction.guild:
            embed = discord.Embed(
                title="❌ Error",
                description="This command can only be used in a server!",
                color=0xff0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Validate amount
        if amount <= 0:
            embed = discord.Embed(
                title="❌ Invalid Amount",
                description="Amount must be a positive number!",
                color=0xff0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            # Ensure guild and member exist in database
            DatabaseManager.ensure_guild_exists(interaction.guild.id, interaction.guild.name)
            DatabaseManager.ensure_member_exists(
                interaction.user.id,
                interaction.user.name,
                interaction.user.display_name
            )
            
            # Verify material exists
            material_info = DatabaseManager.get_material_by_name(material)
            if not material_info:
                embed = discord.Embed(
                    title="❌ Invalid Material",
                    description="The specified material is not valid. Please use the dropdown to select a material.",
                    color=0xff0000
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            # Add contribution
            success = DatabaseManager.add_contribution(
                interaction.guild.id,
                interaction.user.id,
                material,
                amount
            )
            
            if success:
                embed = discord.Embed(
                    title="✅ Contribution Recorded",
                    description=f"{interaction.user.mention} contributed **{amount:,}** {material_info['display_name']}!",
                    color=0x00ff00
                )
                embed.add_field(name="Material", value=material_info['display_name'], inline=True)
                embed.add_field(name="Amount", value=f"{amount:,}", inline=True)
                embed.add_field(name="Contributor", value=interaction.user.display_name, inline=True)
                embed.set_footer(text=f"Guild: {interaction.guild.name}")
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(
                    title="❌ Error",
                    description="Failed to record contribution. Please try again.",
                    color=0xff0000
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                
        except Exception as e:
            logger.error(f"Error in contribute command: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description="An unexpected error occurred. Please try again later.",
                color=0xff0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    # Set up the material autocomplete
    @contribute.autocomplete('material')
    async def material_autocomplete(
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        """Autocomplete for material selection"""
        try:
            materials = DatabaseManager.get_all_materials()
            choices = []
            
            # Filter materials based on current input
            for material in materials:
                if current.lower() in material['display_name'].lower() or current.lower() in material['name'].lower():
                    choices.append(app_commands.Choice(
                        name=material['display_name'], 
                        value=material['name']
                    ))
                    if len(choices) >= 25:  # Discord limit
                        break
            
            # If no matches, show all materials
            if not choices:
                for material in materials[:25]:
                    choices.append(app_commands.Choice(
                        name=material['display_name'], 
                        value=material['name']
                    ))
            
            return choices
        except Exception as e:
            logger.error(f"Error in material autocomplete: {e}")
            return []

    @bot.tree.command(name="contributions", description="View your contributions or another member's contributions")
    @app_commands.describe(member="The member to view contributions for (optional)")
    async def view_contributions(interaction: discord.Interaction, member: discord.Member = None):
        """View contributions for a member"""
        if not interaction.guild:
            embed = discord.Embed(
                title="❌ Error",
                description="This command can only be used in a server!",
                color=0xff0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        target_member = member or interaction.user
        
        try:
            # Ensure member exists in database
            DatabaseManager.ensure_member_exists(
                target_member.id,
                target_member.name,
                target_member.display_name
            )
            
            contributions = DatabaseManager.get_member_contributions(
                interaction.guild.id,
                target_member.id
            )
            
            if not contributions:
                embed = discord.Embed(
                    title="📊 No Contributions",
                    description=f"{target_member.display_name} hasn't made any contributions yet.",
                    color=0x0099ff
                )
                await interaction.response.send_message(embed=embed)
                return
            
            # Group contributions by material
            material_totals = {}
            for contrib in contributions:
                material = contrib['material_name']
                if material in material_totals:
                    material_totals[material] += contrib['amount']
                else:
                    material_totals[material] = contrib['amount']
            
            embed = discord.Embed(
                title=f"📊 {target_member.display_name}'s Contributions",
                color=0x0099ff
            )
            embed.set_thumbnail(url=target_member.avatar.url if target_member.avatar else target_member.default_avatar.url)
            
            # Add fields for each material
            total_contributions = 0
            for material, amount in sorted(material_totals.items(), key=lambda x: x[1], reverse=True):
                embed.add_field(
                    name=material,
                    value=f"{amount:,}",
                    inline=True
                )
                total_contributions += amount
            
            embed.add_field(
                name="🏆 Total Contributions",
                value=f"{total_contributions:,}",
                inline=False
            )
            
            embed.set_footer(text=f"Guild: {interaction.guild.name} • Total entries: {len(contributions)}")
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            logger.error(f"Error in view_contributions command: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description="An unexpected error occurred. Please try again later.",
                color=0xff0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="leaderboard", description="View the top contributors in this guild")
    async def leaderboard(interaction: discord.Interaction):
        """View top contributors leaderboard"""
        if not interaction.guild:
            embed = discord.Embed(
                title="❌ Error",
                description="This command can only be used in a server!",
                color=0xff0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            top_contributors = DatabaseManager.get_top_contributors(interaction.guild.id, 10)
            
            if not top_contributors:
                embed = discord.Embed(
                    title="🏆 Contribution Leaderboard",
                    description="No contributions have been recorded yet!",
                    color=0x0099ff
                )
                await interaction.response.send_message(embed=embed)
                return
            
            embed = discord.Embed(
                title="🏆 Top Contributors",
                description=f"Leaderboard for {interaction.guild.name}",
                color=0xffd700
            )
            
            # Add leaderboard entries
            for i, contributor in enumerate(top_contributors, 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                embed.add_field(
                    name=f"{medal} {contributor['display_name']}",
                    value=f"{contributor['total_contributions']:,} total contributions",
                    inline=False
                )
            
            embed.set_footer(text=f"Use /contributions to view detailed breakdown")
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            logger.error(f"Error in leaderboard command: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description="An unexpected error occurred. Please try again later.",
                color=0xff0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    # ==================== AI CONVERSATION COMMANDS ====================
    
    @bot.tree.command(name="ask", description="Ask AI a question (Daily limits: 25 per user, 500 per server)")
    @app_commands.describe(question="Your question for the AI (max 4000 characters)")
    async def ask_ai(interaction: discord.Interaction, question: str):
        """AI conversation command with cost controls"""
        if not interaction.guild:
            embed = discord.Embed(
                title="❌ Error",
                description="This command can only be used in a server!",
                color=0xff0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # Get AI service
        ai_service = get_ai_service()
        if not ai_service:
            embed = discord.Embed(
                title="❌ AI Service Unavailable",
                description="AI service is not configured. Please check the OpenAI API key.",
                color=0xff0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # Defer response since AI calls can take time
        await interaction.response.defer()

        try:
            # Process AI request with safety checks
            success, response = await ai_service.ask_ai(
                guild_id=interaction.guild.id,
                user_id=interaction.user.id,
                prompt=question
            )

            if success:
                # Successful AI response
                embed = discord.Embed(
                    title="🤖 AI Response",
                    description=response,
                    color=0x00ff00
                )
                embed.set_footer(text=f"Asked by {interaction.user.display_name}")
                
                # Split long responses if needed (Discord has 4096 char limit for embeds)
                if len(response) > 4000:
                    embed.description = response[:4000] + "... [Response truncated]"
                
                await interaction.followup.send(embed=embed)
            else:
                # Error response (quota exceeded, API issues, etc.)
                embed = discord.Embed(
                    title="❌ AI Request Failed",
                    description=response,
                    color=0xff0000
                )
                await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            logger.error(f"Error in ask command: {e}")
            embed = discord.Embed(
                title="❌ Unexpected Error",
                description="An unexpected error occurred while processing your AI request. Please try again later.",
                color=0xff0000
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

    logger.info("Commands setup complete")
