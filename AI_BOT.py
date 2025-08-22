# https://github.com/Psvita538/discord.py-projects
# Made by Batboy4K!!!🧸🧸🧸🧸

import discord
from discord.ext import commands
import google.generativeai as genai
import requests
from PIL import Image
from io import BytesIO

# Configure Gemini AI (Make sure to keep your API key secret!)
genai.configure(api_key="GET_YOUR_OWN_API_CODE")
model = genai.GenerativeModel("gemini-2.0-flash")

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True  # Allows the bot to read message content
intents.messages = True
intents.guilds = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Store auto-reply channel (default: disabled)
auto_reply_channel_id = None  

# --- Image Processing Function ---
async def process_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.show()  # Opens the image for inspection

# --- Error Handling ---
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You are missing permissions to use this command.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I am missing permissions to execute this command.")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send(f"An error occurred: {error}")
    else:
        await ctx.send(f"An unknown error occurred: {error}")

# --- Unified Message Handling (Mentions + Auto-reply + Image Detection) ---
@bot.event
async def on_message(message):
    if message.author.bot:
        return  # Ignore bot messages

    # Handle bot mentions
    if bot.user in message.mentions:
        await handle_ai_response(message)

    # Handle auto-reply in specific channel
    if auto_reply_channel_id and message.channel.id == auto_reply_channel_id:
        await handle_ai_response(message)

    # Handle image attachments
    if message.attachments:
        for attachment in message.attachments:
            if any(attachment.filename.endswith(ext) for ext in ["png", "jpg", "jpeg", "gif"]):
                await message.channel.send(f"Image received: {attachment.url}")
                await process_image(attachment.url)  # Process the image

    await bot.process_commands(message)  # Ensure commands still work

# --- AI Response Handling ---
async def handle_ai_response(message):
    async with message.channel.typing():
        response = model.generate_content(message.content)
        response_text = response.text

        if len(response_text) > 2000:
            chunks = [response_text[i:i+2000] for i in range(0, len(response_text), 2000)]
            for chunk in chunks:
                await message.channel.send(chunk)
        else:
            await message.channel.send(response_text)

# --- Enable Auto-reply ---
@bot.command(name="set_autoreply")
async def set_autoreply(ctx, channel: discord.TextChannel):
    global auto_reply_channel_id
    auto_reply_channel_id = channel.id
    await ctx.send(f"Auto-reply enabled in {channel.mention}")

# --- Disable Auto-reply ---
@bot.command(name="disable_autoreply")
async def disable_autoreply(ctx):
    global auto_reply_channel_id
    auto_reply_channel_id = None  # Reset the auto-reply setting
    await ctx.send("Auto-reply has been disabled.")

# --- Start the Bot ---
bot.run("token here lol")
