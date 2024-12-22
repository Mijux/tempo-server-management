#!/usr/bin/env python3
import re
from datetime import datetime
from bot.command import CommandHandler
from discord import Interaction
from functools import wraps
from utils.logger import get_logger

def is_admin_command(func):
    """Décorateur pour vérifier si l'utilisateur est administrateur."""
    @wraps(func)
    async def wrapper(interaction: Interaction, *args, **kwargs):
        # Vérifie si l'utilisateur est administrateur
        if not CommandHandler.is_admin_user(interaction.message.author.id):
            get_logger().error("Uniquement réservé à un administrateur")
            await interaction.channel.send("Seul un utilisateur administrateur peut exécuter cette commande")
            return
        return await func(interaction, *args, **kwargs)
    return wrapper


def check_length_cmd(interaction: Interaction, min:int = None, max:int= None):
    if min != None and len(interaction.message.content.split()) < min:
        return False
    if max != None and len(interaction.message.content.split()) > max:
        print(max)
        return False
    return True


def check_mention_cmd(interaction: Interaction, position: int):
    words = interaction.message.content.split()
    if len(words) >= position + 1:
        mention = words[position]
        print(mention)
        print(mention)
        match = re.match(r'<@(\d+)>', mention)

        if match:
            member_id = int(match.group(1))
            print(member_id)
            # Vérifie si un membre avec cet ID existe dans le serveur
            member = interaction.guild.get_member(member_id)
            for mem in interaction.guild.members:
                print(mem)
            if member:
                return True  # C'est une mention valide
    return False  # Ce n'est pas une mention valide

def check_date_cmd(interaction: Interaction, position:int):
    if len(interaction.message.content.split()) >= position + 1:
        try:
            datetime.strptime(interaction.message.content.split()[position], "%Y-%m-%d")
            return True
        except ValueError:
            return False
    return False
            