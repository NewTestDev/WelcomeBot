import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from flask import Flask
import threading

# Charger le fichier .env pour obtenir le token en toute sécurité
load_dotenv()

# Lire le token à partir du fichier .env
TOKEN = os.getenv("DISCORD_TOKEN")

# Vérifier si le token a été correctement chargé
if not TOKEN:
    print("❌ Token non trouvé. Assurez-vous que le fichier .env est présent et correctement configuré.")
    exit(1)  # Arrêter l'exécution du bot si le token est manquant

# Configuration du bot Discord
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# IDs à jour
ROLE_MEMBRE_ID = 1348599259276247061
ROLE_ARRIVANT_ID = 1350223364249227275

@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")

@bot.event
async def on_member_update(before, after):
    """Quand un membre reçoit le rôle Membre, supprimer le rôle Arrivant"""
    role_membre = after.guild.get_role(ROLE_MEMBRE_ID)
    role_arrivant = after.guild.get_role(ROLE_ARRIVANT_ID)

    if role_membre in after.roles and role_arrivant in after.roles:
        await after.remove_roles(role_arrivant)
        print(f"Rôle 'Arrivant' retiré pour {after.name}")

# Créer un serveur Flask pour maintenir le bot en ligne
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!"  # Une réponse simple pour prouver que ton bot est en vie

def run_flask():
    app.run(host="0.0.0.0", port=8080)  # Le port 8080 est utilisé par Render

# Lancer Flask dans un thread séparé pour ne pas bloquer ton bot
threading.Thread(target=run_flask, daemon=True).start()

# Utiliser le token depuis .env
bot.run(TOKEN)