
import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    guild = member.guild
    role = discord.utils.get(guild.roles, name="Member")
    if role:
        await member.add_roles(role)
    channel = discord.utils.get(guild.text_channels, name="welcome")
    if channel:
        await channel.send(f"👋 Welcome {member.mention} to **{guild.name}**!")

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

@bot.command()
async def welcome(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(f"👋 Welcome {member.mention}!")

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title="👤 User Info", color=discord.Color.blue())
    embed.add_field(name="Username", value=member.name, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Joined", value=member.joined_at.strftime("%d-%m-%Y"), inline=True)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else discord.Embed.Empty)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 Kicked {member.mention} for: {reason}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 Banned {member.mention} for: {reason}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"🧹 Cleared {amount} messages", delete_after=3)

bot.run(os.getenv("TOKEN"))
