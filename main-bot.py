#!/usr/bin/env python3
import os;
from dotenv import load_dotenv
from bot.discord import DiscordBot

load_dotenv()
TOKEN_BOT = os.getenv("TOKEN_BOT")
GUILD_ID = os.getenv("GUILD_ID")
bot = DiscordBot(TOKEN_BOT, GUILD_ID)
bot.run()


