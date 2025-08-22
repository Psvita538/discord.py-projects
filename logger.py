# https://github.com/Psvita538/discord.py-projects
# Made by Batboy4K!!!🧸🧸🧸🧸

import discord
from discord.ext import commands
from datetime import datetime

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

CHANNEL_ID = 0 # Channel to log EVERYTHING in!
WELCOME_CHANNEL_ID = 0 # Channel to welcome people in!
WELCOME_IMAGE_URL = "https://github.com/Psvita538/Pii-Public-Radio/blob/main/16.png?raw=true"

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You are missing permissions to use this command.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I am missing permissions to execute this command.")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send(f"An error occurred: {error}") #Careful with this one!
    else:
        await ctx.send(f"An unknown error occurred: {error}")


# Log voice state changes (join/leave voice channels)
@bot.event
async def on_voice_state_update(member, before, after):
    channel = bot.get_channel(CHANNEL_ID)
    if before.channel is None and after.channel is not None:  # Joined a voice channel
        embed = discord.Embed(title="User Joined Voice Chat", color=discord.Color.green())
        embed.add_field(name="User", value=f"{member.name}#{member.discriminator}")
        embed.add_field(name="Channel", value=f"{after.channel.name}")
        embed.add_field(name="Time", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        await channel.send(embed=embed)
    elif before.channel is not None and after.channel is None:  # Left a voice channel
        embed = discord.Embed(title="User Left Voice Chat", color=discord.Color.red())
        embed.add_field(name="User", value=f"{member.name}#{member.discriminator}")
        embed.add_field(name="Channel", value=f"{before.channel.name}")
        embed.add_field(name="Time", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        await channel.send(embed=embed)

# Log reactions added or removed
@bot.event
async def on_reaction_add(reaction, user):
    channel = bot.get_channel(CHANNEL_ID)
    if user.bot:
        return
    embed = discord.Embed(title="Reaction Added", color=discord.Color.blue())
    embed.add_field(name="User", value=f"{user.name}#{user.discriminator}")
    embed.add_field(name="Emoji", value=str(reaction.emoji))
    embed.add_field(name="Message", value=f"[Jump to message]({reaction.message.jump_url})")
    embed.set_footer(text=f"User ID: {user.id}")
    await channel.send(embed=embed)

@bot.event
async def on_reaction_remove(reaction, user):
    channel = bot.get_channel(CHANNEL_ID)
    if user.bot:
        return
    embed = discord.Embed(title="Reaction Removed", color=discord.Color.orange())
    embed.add_field(name="User", value=f"{user.name}#{user.discriminator}")
    embed.add_field(name="Emoji", value=str(reaction.emoji))
    embed.add_field(name="Message", value=f"[Jump to message]({reaction.message.jump_url})")
    embed.set_footer(text=f"User ID: {user.id}")
    await channel.send(embed=embed)

# Enhanced logging for member joins
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(CHANNEL_ID)
    invites = await member.guild.invites()
    vanity = member.guild.vanity_url
    join_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    embed = discord.Embed(title="Member Joined", color=discord.Color.green())
    embed.add_field(name="User", value=f"{member.name}#{member.discriminator}")
    embed.add_field(name="Time Joined", value=join_time)
    embed.add_field(name="Joined From", value="Vanity URL" if vanity else "Invite Link")
    embed.set_footer(text=f"User ID: {member.id}")
    await channel.send(embed=embed)


async def fetch_audit_logs():
    channel = bot.get_channel(CHANNEL_ID)
    guild = channel.guild

    try:
        async for entry in guild.audit_logs(limit=10):  # Fetch latest 10 entries
            embed = discord.Embed(title="Audit Log Entry", color=discord.Color.purple())
            embed.add_field(name="Action Type", value=str(entry.action), inline=False)
            embed.add_field(name="Target", value=str(entry.target), inline=False)
            embed.add_field(name="Responsible User", value=f"{entry.user.name}#{entry.user.discriminator}", inline=False)
            embed.add_field(name="Extra Details", value=str(entry.extra), inline=False)
            embed.add_field(name="Time", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), inline=False)
            await channel.send(embed=embed)
    except Exception as e:
        print(f"Error fetching audit logs: {e}")

@bot.event
async def on_member_update(before, after):
    # Fetch audit logs on member update (example trigger)
    await fetch_audit_logs()

@bot.event
async def on_guild_update(before, after):
    # Fetch audit logs on guild update (example trigger)
    await fetch_audit_logs()

@bot.event
async def on_message_delete(message):
    channel = bot.get_channel(CHANNEL_ID)
    if message.author.bot:
        return

    embed = discord.Embed(title="Message Deleted", color=discord.Color.red())
    embed.add_field(name="User", value=f"{message.author.name}#{message.author.discriminator}")
    embed.add_field(name="Content", value=message.content, inline=False)
    embed.add_field(name="Channel", value=f"{message.channel.name}")
    embed.set_footer(text=f"Message ID: {message.id} | Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    await channel.send(embed=embed)

# Log edited messages
@bot.event
async def on_message_edit(before, after):
    channel = bot.get_channel(CHANNEL_ID)
    if before.author.bot:
        return

    embed = discord.Embed(title="Message Edited", color=discord.Color.orange())
    embed.add_field(name="User", value=f"{before.author.name}#{before.author.discriminator}")
    embed.add_field(name="Before", value=before.content, inline=False)
    embed.add_field(name="After", value=after.content, inline=False)
    embed.add_field(name="Channel", value=f"{before.channel.name}")
    embed.set_footer(text=f"Message ID: {before.id} | Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    """
    Event listener that triggers when a member leaves the server.
    Sends an embed message to a specified channel with information about the departing member.
    """
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"Error: Could not find channel with ID {CHANNEL_ID}")  # Add error handling in case the channel doesn't exist
        return  # Exit the function if the channel isn't found

    embed = discord.Embed(
        title="Member Left",
        description=f"{member.name}#{member.discriminator} has left the server.",
        color=discord.Color.red()
    )
    embed.set_footer(text=f"User ID: {member.id}")
    await channel.send(embed=embed)

#@bot.event
# async def on_member_join(member):
#    role_id = 1244081892429529159  # Your role ID
#    role = member.guild.get_role(role_id)
#    if role:
#        await member.add_roles(role)
#        print(f"Assigned {role.name} to {member.name}")

@bot.event
async def on_member_join(member):
    # Create the welcome embed
    embed = discord.Embed(
    title="Welcome to ReTrance! 🎉",
    description=(
        f"{member.mention}, please read the rules if you haven't, and meet some small businesses, "
        "content creators, IT pros, gamers, and others."
    ),
    color=discord.Color.blue()
)

    embed.set_thumbnail(url=WELCOME_IMAGE_URL)

    # Send DM
    try:
        await member.send(embed=embed)
    except discord.Forbidden:
        print(f"Could not send DM to {member}.")
    embed.set_thumbnail(url=WELCOME_IMAGE_URL)

    # Send DM
    try:
        await member.send(embed=embed)
    except discord.Forbidden:
        print(f"Could not send DM to {member}.")

    # Post in server welcome channel
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(embed=embed)


bot.run('add your bot token here!')
