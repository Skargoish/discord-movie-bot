import os
import discord
import requests
import random
from discord.ext import commands, tasks

TOKEN = os.getenv("DISCORD_TOKEN")
OMDB_KEY = os.getenv("OMDB_KEY")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

movies = ["Inception", "The Matrix", "Interstellar", "The Dark Knight", "Parasite"]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    channel = discord.utils.get(bot.get_all_channels(), name="general")  # change if needed
    if channel:
        movie = random.choice(movies)
        url = f"http://www.omdbapi.com/?t={movie}&apikey={OMDB_KEY}"
        response = requests.get(url).json()
        if response["Response"] == "True":
            msg = f"🎬 **Movie of the Day:** {response['Title']} ({response['Year']})\n⭐ IMDB: {response['imdbRating']}\n📖 {response['Plot']}"
        else:
            msg = f"🎬 Movie of the Day: {movie}"
        await channel.send(msg)
    await bot.close()  # stop after sending

bot.run(TOKEN)
