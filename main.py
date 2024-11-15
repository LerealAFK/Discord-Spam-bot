import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import random
from keep_alive import keep_alive

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Configuration du bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Liste des tâches de spam en cours, avec le format {ID: (task, user_id)}
active_spams = {}

@bot.event
async def on_ready():
    await bot.tree.sync()  # Synchronise les slash commands
    print(f"Bot connecté en tant que {bot.user} et commandes synchronisées.")

# Commande /spamm : Démarre un spam
@bot.tree.command(name="spamm", description="Commence à spammer un message.")
async def spamm(interaction: discord.Interaction, message: str):
    spam_id = len(active_spams) + 1
    user_id = interaction.user.id  # ID de l'utilisateur qui a initié le spam
    await interaction.response.send_message(f"Début du spam `{spam_id}` : `{message}`. Utilisez `/stop {spam_id}` pour l'arrêter. (Seulement vous pouvez le stopper.)")

    # Tâche de spam
    async def spam():
        try:
            while True:
                await interaction.channel.send(message)
                await asyncio.sleep(1)  # Intervalle entre chaque message
        except asyncio.CancelledError:
            # Arrêter proprement la tâche si elle est annulée
            await interaction.channel.send(f"Spam `{spam_id}` arrêté.")

    # Créer et enregistrer la tâche avec l'ID de l'utilisateur
    spam_task = asyncio.create_task(spam())
    active_spams[spam_id] = (spam_task, user_id)

# Commande /stop : Arrête un spam spécifique
@bot.tree.command(name="stop", description="Arrête un spam en cours.")
async def stop(interaction: discord.Interaction, spam_id: int):
    if spam_id not in active_spams:
        await interaction.response.send_message(f"❌ Aucun spam trouvé avec l'ID `{spam_id}`.", ephemeral=True)
        return

    spam_task, user_id = active_spams[spam_id]

    # Vérifie si l'utilisateur est autorisé à arrêter le spam
    if interaction.user.id != user_id:
        await interaction.response.send_message("❌ Vous n'êtes pas autorisé à arrêter ce spam.", ephemeral=True)
        return

    # Arrêter et supprimer la tâche de spam
    spam_task.cancel()
    del active_spams[spam_id]
    await interaction.response.send_message(f"✔️ Spam `{spam_id}` arrêté avec succès.")

# Commande /listspams : Affiche la liste des spams actifs
@bot.tree.command(name="listspams", description="Affiche la liste des spams en cours.")
async def listspams(interaction: discord.Interaction):
    if not active_spams:
        await interaction.response.send_message("Aucun spam actif.", ephemeral=True)
        return

    # Construire une liste des spams actifs
    spam_list = "\n".join([
        f"ID : `{spam_id}`, Démarré par : <@{user_id}>"
        for spam_id, (_, user_id) in active_spams.items()
    ])
    await interaction.response.send_message(f"📜 Liste des spams actifs :\n{spam_list}")

# Commande /mdr : Envoie un GIF avec une option de boucle
gif_urls = [
    "https://tenor.com/view/zarbi-dance-tv-stupid-fun-gif-19517995",
    "https://media.giphy.com/media/3oriO0OEd9QIDdllqo/giphy.gif",
    "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
    "https://media.giphy.com/media/5ntdy5Ban1dIY/giphy.gif",
    "https://media.giphy.com/media/26ufdipQqU2lhNA4g/giphy.gif"
]

@bot.tree.command(name="mdr", description="Envoie un GIF drôle avec option de boucle.")
async def mdr(interaction: discord.Interaction, loop: bool):
    if loop:
        # Envoie des GIFs en boucle
        await interaction.response.send_message("Début du spam de GIFs en boucle.")
        async def spam_gifs():
            try:
                while True:
                    random_gif = random.choice(gif_urls)
                    await interaction.channel.send(random_gif)
                    await asyncio.sleep(2)
            except asyncio.CancelledError:
                await interaction.channel.send("Spam de GIFs arrêté.")

        # Lancer le spam GIF
        gif_task = asyncio.create_task(spam_gifs())
        active_spams[len(active_spams) + 1] = (gif_task, interaction.user.id)
    else:
        # Envoie un seul GIF
        random_gif = random.choice(gif_urls)
        await interaction.response.send_message("Envoi d'un GIF unique.")
        await interaction.channel.send(random_gif)

# Commande /mdrstop : Arrête tous les spams de GIFs pour l'utilisateur
@bot.tree.command(name="mdrstop", description="Arrête tous vos spams de GIFs.")
async def mdrstop(interaction: discord.Interaction):
    user_id = interaction.user.id
    gif_spams = [
        spam_id for spam_id, (_, owner_id) in active_spams.items()
        if owner_id == user_id
    ]
    if not gif_spams:
        await interaction.response.send_message("Vous n'avez aucun spam de GIFs en cours.", ephemeral=True)
        return

    for spam_id in gif_spams:
        task, _ = active_spams.pop(spam_id)
        task.cancel()

    await interaction.response.send_message("✔️ Tous vos spams de GIFs ont été arrêtés.")

# Démarrer le bot
keep_alive()
bot.run(token)
