#!/usr/bin/env python3
import discord

from bot.discord_job import DiscordJob

class DiscordBot:
    def __init__(self, TOKEN_BOT):
        self.TOKEN_BOT = TOKEN_BOT
        self.client = discord.Client(intents=self.configure_bot()) 
        self.setup_events()
        self.worker = DiscordJob()

    def configure_bot(self):
        intents = discord.Intents.default()
        intents.message_content = True 
        return intents 

    def setup_events(self):
        """
        Configure les événements du bot (par exemple, `on_ready`, `on_message`).
        """
        @self.client.event
        async def on_ready():
            print("Le bot est prêt !")

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return
            if message.content == "Ping":
                await message.channel.send("Pong")
                self.worker.add_user(message.author.id, message.author.name, message.author.avatar)

    def run(self):
        """
        Lance le bot avec le token.
        """
        self.client.run(self.TOKEN_BOT)
