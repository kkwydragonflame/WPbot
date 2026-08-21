import os

from dotenv import load_dotenv

import discord
from discord.ext import commands

# Load environment variables from .env file
load_dotenv()

token = os.getenv("BOT_TOKEN")

if token is None:
    raise ValueError("Bot token not found in environment variables. Please set BOT_TOKEN in the .env file.")

# Default set of Gateway intents, which includes all non-privileged events
intents = discord.Intents.default()

# Create a new instance of the Bot class with the specified command prefix and intents
bot = commands.Bot(
  command_prefix="!", 
  intents=intents
)

# Event handler for when the bot is ready and connected to Discord
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

# Start the bot
bot.run(token)