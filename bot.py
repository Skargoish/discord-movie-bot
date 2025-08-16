import os
import discord
import requests
import random
from discord.ext import commands, tasks
from datetime import datetime

# === CONFIG ===
TOKEN = os.getenv("DISCORD_TOKEN")   # keep token as a GitHub secret
OMDB_KEY = os.getenv("OMDB_API_KEY") # keep API key as a GitHub secret
CHANNEL_ID = 1406165038741323796     # put your channel ID here directly

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# List of movies you want it to pick from
movies = ["Inception", "The Matrix", "Interstellar", "The Dark Knight", "Parasite", "Get Out", "A Quiet Place"]

# Helper: fetch movie details from OMDB
def get_movie_info(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_KEY}"
    response = requests.get(url).json()
    return response if response.get("Response") == "True" else None

# Task: send a movie recommendation daily
@tasks.loop(minutes=1)
async def daily_movie_post():
    now = datetime.utcnow().strftime("%H:%M")  # server time in UTC
    target_time = "12:00"  # <-- change this if you want another posting time (UTC)
    if now == target_time:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            movie = random.choice(movies)
            data = get_movie_info(movie)
            
            if data:
                embed = discord.Embed(
                    title=f"🎬 {data['Title']} ({data['Year']})",
                    description=data['Plot'],
                    color=discord.Color.red()
                )
                embed.add_field(name="⭐ IMDB", value=data.get("imdbRating", "N/A"))
                embed.add_field(name="⏱ Runtime", value=data.get("Runtime", "N/A"))
                embed.add_field(name="🎭 Genre", value=data.get("Genre", "N/A"))
                embed.set_thumbnail(url=data.get("Poster"))
                await channel.send(embed=embed)
            else:
                await channel.send(f"🎬 Movie of the Day: {movie}")

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    daily_movie_post.start()

bot.run(TOKEN)
