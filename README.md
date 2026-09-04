# WPbot

WPbot is a small Discord bot that manages yearly progression between school-year roles.

During August, September, and October, it checks the configured guild once per day. Members with a progression role receive a direct message asking whether they have completed the school year. If they confirm, the bot changes their role:

```text
Åk1 -> Åk2 -> Åk3 -> Alumni
```

The bot uses the school year rather than the calendar year. August starts a new school year, so a member is asked at most once during each school year. SQLite stores the prompt history, including the member, guild, and school year.

## Use This Bot

1. Fork this repository on GitHub and clone your fork.
2. Install Python 3.10 or newer.
3. Install the dependencies:

	```powershell
	python -m pip install discord.py python-dotenv
	```

4. Create a Discord application and bot in the [Discord Developer Portal](https://discord.com/developers/applications).
5. Invite the bot to your server with these permissions:
	- View Channels
	- Send Messages
	- Manage Roles
6. Enable **Server Members Intent** under the bot's **Privileged Gateway Intents** in the Developer Portal.
7. Update [src/progression_roles.py](src/progression_roles.py) with the role names used in your server. The names must match Discord exactly.
8. Create a `.env` file in the project root:

	```env
	BOT_TOKEN=your_bot_token_here
	GUILD_ID=your_server_id_here
	```

	Keep the token private and never commit `.env`.

9. Start the bot from the project root:

	```powershell
	python -m src.bot
	```

The bot creates `progression.sqlite3` automatically the first time it starts. This file contains runtime data and should not be committed.

## Finding Your Guild ID

In Discord, enable **Developer Mode** under **User Settings -> Advanced**. Then right-click your server icon or server name and choose **Copy Server ID**. Put the copied number in `.env` as `GUILD_ID`.

## Configuration

The prompt period is configured in [src/bot.py](src/bot.py):

```python
PROMPT_MONTHS = [8, 9, 10]
```

The progression roles are configured in [src/progression_roles.py](src/progression_roles.py). The bot currently supports one configured guild. Each member must have one of the configured progression roles, and the bot's own role must be higher than those roles in the server role list.

## Project Files

- [src/bot.py](src/bot.py): starts the bot and runs the yearly progression check.
- [src/progression_roles.py](src/progression_roles.py): defines valid roles and allowed transitions.
- [src/progression_view.py](src/progression_view.py): sends the DM and handles the Yes/Not yet buttons.
- [src/progression_db.py](src/progression_db.py): creates and queries the SQLite database.
