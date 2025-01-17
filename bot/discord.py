#!/usr/bin/env python3
import discord
from discord.ext import commands
from discord import app_commands
from bot.command import CommandHandler

from datetime import datetime
from utils.cmd_validators import admin_command, check_date_cmd, check_length_cmd, check_mention_cmd
from utils.enums.role import RoleE
from utils.exceptions import DBError, DBUserAlreadyExistsError, DBUserDoesNotExistError, DBUserNotPresent, DBUserPresenceOngoingdError
from utils.logger import get_logger



class DiscordBot:
    def __init__(self, TOKEN_BOT, GUILD_ID):
        self.TOKEN_BOT = TOKEN_BOT
        self.GUILD_ID = discord.Object(id=GUILD_ID)       
        self.client = commands.Bot(command_prefix="!", intents=self.configure_bot()) 
        self.setup_events()  
        self.setup_cmds()   
    
    def configure_bot(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True  # Nécessaire pour pouvoir lire le contenu des messages
        return intents

    def setup_events(self):
 
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
        
        @self.client.command(name="hello", description="Description à venir", guild=self.GUILD_ID)
        @check_length_cmd(min=2, max=3)  
        @check_mention_cmd(positions=[1]) 
        @check_date_cmd(positions=[2]) 
        @admin_command
        async def hello(interaction: discord.Interaction):
            user_mention = interaction.message.mentions[0]
            username = user_mention.name
            id = user_mention.id
            avatar = user_mention.avatar
            if len(interaction.message.content.split()) == 3:
                date = interaction.message.content.split()[2]
                date = datetime.strptime(date, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)
            else:
                date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            try:
                if CommandHandler.add_user(id,username, avatar, date):
                    await interaction.channel.send(f"L'utilisateur {username} a été rajouté avec une date d'arrivée {date.strftime('%Y-%m-%d')}")
                else:
                    await interaction.channel.send(f"L'utilisateur {username} n'a pas put être créé.")
            except DBUserPresenceOngoingdError:
                await interaction.channel.send(f"L'utilisateur {username} est déjà en cours de présence.")
            return False
        
        @self.client.command(name="op", description="Description à venir", guild=self.GUILD_ID)
        @check_length_cmd(min=2, max=2)  
        @check_mention_cmd(positions=[1]) 
        @admin_command
        async def op(interaction: discord.Interaction):
            user_mention = interaction.message.mentions[0]
            username = user_mention.name
            user_id = user_mention.id
            try:
                if CommandHandler.change_role_user(user_id,RoleE.ADMIN):
                    await interaction.channel.send(f"L'utilisateur {username} a été ajouté aux administrateurs.")
            except DBUserDoesNotExistError:
                await interaction.channel.send(f"L'utilisateur {username} n'existe pas.")
            except DBError:
                await interaction.channel.send(f"Une erreur est survenue.")
            
            return False
        
        @self.client.command(name="deop", description="Description à venir", guild=self.GUILD_ID)
        @check_length_cmd(min=2, max=2)  
        @check_mention_cmd(positions=[1]) 
        @admin_command
        async def deop(interaction: discord.Interaction):
            user_mention = interaction.message.mentions[0]
            username = user_mention.name
            user_id = user_mention.id
            try:
                if CommandHandler.change_role_user(user_id,RoleE.DEFAULT):
                    await interaction.channel.send(f"L'utilisateur {username} est retiré des administrateurs.")
            except DBUserDoesNotExistError:
                await interaction.channel.send(f"L'utilisateur {username} n'existe pas.")
            except DBError:
                await interaction.channel.send(f"Une erreur est survenue.")
            
            return False
        
        @self.client.command(name="bye", description="Description à venir", guild=self.GUILD_ID)
        @check_length_cmd(min=2, max=2)  
        async def bye(interaction: discord.Interaction):
            word = interaction.message.content.split()[1]
            try:
                username = ''
                if word == 'yes':
                    username = interaction.message.author.name
                    await bye_myself(interaction.message.author.id)
                else:
                    username = interaction.message.mentions[0].name
                    await bye_admin(interaction)
                await interaction.channel.send(f"L'utilisateur {username} a bien été retiré.")
            except DBUserNotPresent as e: 
                await interaction.channel.send(f"L'utilisateur {username} n'est plus présent.")
            except DBUserDoesNotExistError as e: 
                await interaction.channel.send(f"L'utilisateur {username} n'existe pas.")
            except DBError as e: 
                await interaction.channel.send(f"Une erreur est survenue.")

           

            return False
        
        @check_mention_cmd(positions=[1]) 
        @admin_command
        async def bye_admin(interaction: discord.Interaction):
            user_mention = interaction.message.mentions[0]
            user_id = user_mention.id
            return CommandHandler.leave_user(user_id)

        

        async def bye_myself(user_id: str):
            return CommandHandler.leave_user(user_id)
            

        
        
    def run(self):
        self.client.run(self.TOKEN_BOT)
