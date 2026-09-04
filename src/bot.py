import os
from datetime import datetime

from dotenv import load_dotenv

import discord
from discord.ext import commands, tasks
from src.progression_roles import get_next_role, VALID_ROLES
from src.progression_view import ask_for_progression
from src.progression_db import initialize_database, has_user_been_prompted, record_user_prompt

# Load environment variables from .env file
load_dotenv()

token = os.getenv("BOT_TOKEN")
guild_id = int(os.getenv("GUILD_ID"))

if token is None:
    raise ValueError("Bot token not found in environment variables. Please set BOT_TOKEN in the .env file.")

# Default set of Gateway intents, which includes all non-privileged events
intents = discord.Intents.default()
intents.members = True  # Enable the members intent to access member information

# Define the months the bot should prompt users for progression.
# In this case, it prompts in August (8) and September (9) and October (10).
PROMPT_MONTHS = [8, 9, 10]

# Create a new instance of the Bot class with the specified command prefix and intents
bot = commands.Bot(
  command_prefix="!", 
  intents=intents
)

def get_school_year(now):
    """
    Get the current school year based on the current date.
    The new school year starts in August.
    """
    if now.month >= 8:
        return now.year
    return now.year - 1

# Event handler for when the bot is ready and connected to Discord
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

    if not yearly_progression_check.is_running():
        print("Starting yearly progression check task...")
        yearly_progression_check.start()

# Task to check for yearly progression, which runs every 24 hours
@tasks.loop(hours=24)
async def yearly_progression_check():
    """
    This task runs every 24 hours to check for users eligible for progression.
    It checks each member of the guild for their current role and determines if they can progress to the next role.
    """
    now = datetime.now()

    if now.month not in PROMPT_MONTHS:
        return  # Not the right month to prompt users

    school_year = get_school_year(now)

    guild = bot.get_guild(guild_id)  # Replace with guild ID
    if guild is None:
        print("Guild not found.")
        return

    for member in guild.members:
        if member.bot:
            continue  # Skip bots

        current_role = None
        for role in member.roles:
            if role.name in VALID_ROLES: # Skip roles that are not valid progression roles
                current_role = role.name
                break

        if current_role is None:
            continue  # Member has no valid role

        next_role = get_next_role(current_role)
        if next_role is None:
            continue  # No next role available

        # Query database if user has already been asked this year
        if has_user_been_prompted(guild.id, member.id, school_year):
            continue  # Already asked this year

        # Wait for view to prompt the user for progression
        await ask_for_progression(member)

        # Update state to indicate that the user has been asked this year
        record_user_prompt(guild.id, member.id, school_year)

# Initialize the database when the bot starts
initialize_database()

# Start the bot
bot.run(token)