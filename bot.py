import os
import discord
import requests
import random
import asyncio
from discord.ext import tasks, commands
from datetime import datetime

TOKEN = os.getenv("DISCORD_TOKEN")
OMDB_KEY = os.getenv("OMDB_API_KEY")

# Hardcode your channel ID here:
CHANNEL_ID = 1406165038741323796  

# For manual workflow runs
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

movies = [
    "Inception", "The Matrix", "Interstellar", "The Dark Knight",
    "Parasite", "Get Out", "Hereditary", "The Conjuring",
    "A Quiet Place", "Midsommar", "The Shining"
]

async def fetch_movie():
    movie = random.choice(movies)
    url = f"http://www.omdbapi.com/?t={movie}&apikey={OMDB_KEY}"
    response = requests.get(url).json()

    if response.get("Response") == "True":
        embed = discord.Embed(
            title=f"🎬 {response['Title']} ({response['Year']})",
            description=response["Plot"],
            color=discord.Color.red()
        )
        embed.add_field(name="⭐ IMDB", value=response["imdbRating"], inline=True)
        embed.add_field(name="🎭 Genre", value=response["Genre"], inline=True)
        embed.add_field(name="🎬 Director", value=response["Director"], inline=True)
        embed.set_image(url=response["Poster"])
        return embed
    else:
        return discord.Embed(
            title="🎬 Movie Recommendation",
            description=movie,
            color=discord.Color.orange()
        )

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

    channel = bot.get_channel(CHANNEL_ID)

    # If manual run → send instantly
    if TEST_MODE and channel:
        embed = await fetch_movie()
        await channel.send(embed=embed)
        print("📢 Sent test movie recommendation instantly")
        await bot.close()
        return

    # Otherwise → start daily task
    daily_movie.start()
    print("⏰ Daily movie task scheduled")

@tasks.loop(minutes=1)
async def daily_movie():
    now = datetime.utcnow().strftime("%H:%M")
    if now == "12:00":  # set to your desired UTC time
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            embed = await fetch_movie()
            await channel.send(embed=embed)
            print("📢 Sent daily movie recommendation")

bot.run(TOKEN)
