#!/usr/bin/env python3
from re import match
from datetime import datetime
from bot.command import CommandHandler
from discord import Interaction
from functools import wraps
from utils.logger import get_logger

def admin_command(func):
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


def check_mention_cmd(positions: list):
    def decorator(func):
        @wraps(func)
        async def wrapper(interaction: Interaction, *args, **kwargs):
            words = interaction.message.content.split()
            for position in positions:
                if len(words) >= position + 1:
                    mention = words[position]
                    match = match(r'<@(\d+)>', mention)
                    if match:
                        member_id = int(match.group(1))
                        member = interaction.guild.get_member(member_id)
                        if member:
                            continue
                    await interaction.channel.send(f"Mention invalide ou manquante à la position {position + 1}.")
                    return
            return await func(interaction, *args, **kwargs)
        return wrapper
    return decorator



def check_date_cmd(positions: list):
    def decorator(func):
        @wraps(func)
        async def wrapper(interaction: Interaction, *args, **kwargs):
            words = interaction.message.content.split()
            for position in positions:
                if len(words) >= position + 1:
                    try:
                        datetime.strptime(words[position], "%Y-%m-%d")
                        continue
                    except ValueError:
                        await interaction.channel.send(f"Date invalide à la position {position + 1}. Veuillez utiliser le format YYYY-MM-DD.")
                        return
            return await func(interaction, *args, **kwargs)
        return wrapper
    return decorator



def check_length_cmd(min: int = None, max: int = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(interaction: Interaction, *args, **kwargs):
            message_length = len(interaction.message.content.split())
            if min is not None and message_length < min:
                await interaction.channel.send(f"Le message doit contenir au moins {min} mots.")
                return
            if max is not None and message_length > max:
                await interaction.channel.send(f"Le message ne doit pas contenir plus de {max} mots.")
                return
            return await func(interaction, *args, **kwargs)
        return wrapper
    return decorator


            