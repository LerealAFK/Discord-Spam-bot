import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import random

# Configuration du bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Variables pour gérer le spam de messages et de GIFs
is_spamming = False
spam_task = None
is_spamming_gif = False
gif_spam_task = None

# Liste des GIFs à utiliser
gif_urls = [
    "https://tenor.com/view/zarbi-dance-tv-stupid-fun-gif-19517995",
    "https://media.giphy.com/media/3oriO0OEd9QIDdllqo/giphy.gif",
    "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
    "https://media.giphy.com/media/5ntdy5Ban1dIY/giphy.gif",
    "https://media.giphy.com/media/26ufdipQqU2lhNA4g/giphy.gif"
]

@bot.event
async def on_ready():
    await bot.tree.sync()  # Synchronise les slash commands
    print(f"Bot connecté en tant que {bot.user} et commandes synchronisées.")

# Commande /spamm
@bot.tree.command(name="spamm", description="Commence à spammer un message.")
async def spamm(interaction: discord.Interaction, message: str):
    global is_spamming, spam_task

    if is_spamming:
        await interaction.response.send_message("Le spam est déjà en cours !", ephemeral=True)
        return

    is_spamming = True
    await interaction.response.send_message(f"Début du spam : `{message}`")

    # Tâche de spam
    async def spam():
        while is_spamming:
            await interaction.channel.send(message)
            await asyncio.sleep(1)  # Temps entre chaque message (modifiable)

    spam_task = asyncio.create_task(spam())

# Commande /stop pour arrêter le spam
@bot.tree.command(name="stop", description="Arrête le spam.")
async def stop(interaction: discord.Interaction):
    global is_spamming, spam_task

    if not is_spamming:
        await interaction.response.send_message("Aucun spam en cours.", ephemeral=True)
        return

    is_spamming = False
    if spam_task:
        spam_task.cancel()  # Arrête la tâche
        spam_task = None

    await interaction.response.send_message("Spam arrêté.")

# Commande /mdr pour envoyer un GIF
@bot.tree.command(name="mdr", description="Envoie un GIF drôle avec option de boucle.")
async def mdr(interaction: discord.Interaction, loop: bool):
    global is_spamming_gif, gif_spam_task

    if is_spamming_gif:
        await interaction.response.send_message("Le spam du GIF est déjà en cours !", ephemeral=True)
        return

    await interaction.response.send_message("Début de l'envoi de GIFs.")
    is_spamming_gif = True

    # Fonction pour spammer des GIFs aléatoires
    async def spam_gif():
        while is_spamming_gif:
            random_gif = random.choice(gif_urls)  # Choisit un GIF aléatoire
            await interaction.channel.send(random_gif)
            await asyncio.sleep(2)  # Intervalle entre chaque envoi

    if loop:
        gif_spam_task = asyncio.create_task(spam_gif())
    else:
        # Envoie un GIF aléatoire une seule fois
        random_gif = random.choice(gif_urls)
        await interaction.channel.send(random_gif)
        is_spamming_gif = False

# Commande /mdrstop pour arrêter le spam du GIF
@bot.tree.command(name="mdrstop", description="Arrête le spam du GIF.")
async def mdrstop(interaction: discord.Interaction):
    global is_spamming_gif, gif_spam_task

    if not is_spamming_gif:
        await interaction.response.send_message("Aucun spam de GIF en cours.", ephemeral=True)
        return

    is_spamming_gif = False
    if gif_spam_task:
        gif_spam_task.cancel()  # Arrête la tâche de spam
        gif_spam_task = None

    await interaction.response.send_message("Spam des GIFs arrêté.")

# Démarrer le bot
TOKEN = "MTMwNTc4NDk5NzgwNTgyMjAwMg.GK3ZBC.wZm3KqeQZNlsVW2V8qa-mC-SjY_pzAlLUQ3rLY"
print(TOKEN) # Remplace par le token de ton bot
bot.run(TOKEN)
