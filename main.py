import discord
from discord.ext import commands
from discord import app_commands
from webservice import webservice
import os

# ✅ Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# ✅ Bot Setup
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree  # For slash commands

# ✅ When bot starts
@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ Logged in as {bot.user}")
    print("🔁 Slash commands synced.")

# ✅ Auto Welcome & Auto Role
@bot.event
async def on_member_join(member):
    # Welcome Message
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if channel:
        await channel.send(f"👋 Welcome {member.mention} to **{member.guild.name}**!")

    # Auto Role
    role = discord.utils.get(member.guild.roles, name="Member")  # Change "Member" to your role name
    if role:
        try:
            await member.add_roles(role)
        except discord.Forbidden:
            print("❌ Bot lacks permission to add role.")

# ✅ /ping
@tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!", ephemeral=True)

# ✅ /userinfo
@tree.command(name="userinfo", description="Show info about a user")
@app_commands.describe(user="The user to inspect")
async def userinfo(interaction: discord.Interaction, user: discord.User = None):
    user = user or interaction.user
    embed = discord.Embed(title="👤 User Info", color=discord.Color.blue())
    embed.add_field(name="Username", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.set_thumbnail(url=user.avatar.url if user.avatar else "")
    await interaction.response.send_message(embed=embed)

# ✅ /kick
@tree.command(name="kick", description="Kick a member")
@app_commands.describe(member="User to kick", reason="Reason for kick")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason"):
    if interaction.user.guild_permissions.kick_members:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"👢 Kicked {member.mention}")
    else:
        await interaction.response.send_message("❌ No permission", ephemeral=True)

# ✅ /ban
@tree.command(name="ban", description="Ban a member")
@app_commands.describe(member="User to ban", reason="Reason for ban")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason"):
    if interaction.user.guild_permissions.ban_members:
        await member.ban(reason=reason)
        await interaction.response.send_message(f"🔨 Banned {member.mention}")
    else:
        await interaction.response.send_message("❌ No permission", ephemeral=True)

# ✅ /clear
@tree.command(name="clear", description="Delete messages")
@app_commands.describe(amount="Number of messages to delete")
async def clear(interaction: discord.Interaction, amount: int = 5):
    if interaction.user.guild_permissions.manage_messages:
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"🧹 Deleted {len(deleted)} messages", ephemeral=True)
    else:
        await interaction.response.send_message("❌ No permission", ephemeral=True)

webservice()
bot.run(os.getenv("TOKEN"))
