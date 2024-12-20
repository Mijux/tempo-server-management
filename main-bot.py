#!/usr/bin/env python3
import os;
from dotenv import load_dotenv
from bot.discord_bot import DiscordBot

load_dotenv()
TOKEN_BOT = os.getenv("TOKEN_BOT")
print(TOKEN_BOT)
bot = DiscordBot(TOKEN_BOT)
bot.run()

