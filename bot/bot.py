#!/usr/bin/env python3
import discord
from discord.ext import commands
from discord import app_commands
from command import CommandHandler


class BotDiscord:
    def __init__(self, TOKEN_BOT, GUILD_ID):
        self.TOKEN_BOT = TOKEN_BOT
        self.GUILD_ID = discord.Object(id=GUILD_ID)       
        self.client = commands.Bot(command_prefix="!", intents=self.configure_bot()) 
        self.setup_events()  
        self.setup_cmds()   
    
    def configure_bot(self):
        """
        Configure les intents pour permettre au bot de lire les messages.
        """
        intents = discord.Intents.default()
        intents.message_content = True  # Nécessaire pour pouvoir lire le contenu des messages
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
            # Ignore les messages envoyés par le bot lui-même
            if message.author == self.client.user:
                return
            
            # Gère les messages Ping
            if message.content == "Ping":
                await message.channel.send("Pong")
                self.worker.add_user(message.author.id, message.author.name, message.author.avatar)

            # Traite aussi les commandes
            await self.client.process_commands(message)

    def setup_cmds(self):
        @self.client.command(name="hello", description="Hello me", guild=self.GUILD_ID)
        async def hello(interaction: discord.Interaction):
            await interaction.channel.send("coucou")
        
    def run(self):
        self.client.run(self.TOKEN_BOT)
