import os
import json

from dotenv import load_dotenv

import discord
from discord.ext import commands, tasks

# Load environment variables from .env file
load_dotenv()

token = os.getenv("BOT_TOKEN")

if token is None:
    raise ValueError("Bot token not found in environment variables. Please set BOT_TOKEN in the .env file.")

# Default set of Gateway intents, which includes all non-privileged events
intents = discord.Intents.default()

# Path to state file for saving and loading bot state
STATE_FILE_PATH = "progression_state.json"

# Create a new instance of the Bot class with the specified command prefix and intents
bot = commands.Bot(
  command_prefix="!", 
  intents=intents
)

def load_state():
    """
    Load the bot's state from a file or database.
    This function should be implemented to restore any necessary state when the bot starts.
    """
    if not os.path.exists(STATE_FILE_PATH):
        return {}
    try:
        return json.loads(STATE_FILE_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Error loading state: {e}")
        return {}

def save_state(data):
    """
    Save the bot's state to a file or database.
    This function should be implemented to persist any necessary state when the bot shuts down.
    """
    try:
        with open(STATE_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Error saving state: {e}")

# Event handler for when the bot is ready and connected to Discord
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@tasks.loop(hours=24)
async def yearly_progression_check():
    """
    This task runs every 24 hours to check for users eligible for progression.
    It should be implemented to iterate through members and prompt them for role progression.
    """
    # Placeholder for yearly progression check logic
    pass

# Start the bot
bot.run(token)