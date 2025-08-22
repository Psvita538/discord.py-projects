# https://github.com/Psvita538/discord.py-projects
# Made by Batboy4K!!!🧸🧸🧸🧸


import discord
from discord.ext import commands
from discord import app_commands

# Define intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()  # Sync slash commands with Discord
    print(f"Logged in as {bot.user}")

# Create a slash command directly within bot.tree
@bot.tree.command(name="say", description="Make the bot say something")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)  # Bot repeats the message

bot.run("add bot token here!")
