import os
import random
import discord
import requests
from discord.ext import commands

# Load secrets from GitHub repository
TOKEN = os.getenv("DISCORD_TOKEN")
OMDB_KEY = os.getenv("OMDB_API_KEY")

# Intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Movies to pick from
MOVIES = [
    "Inception",
    "The Matrix",
    "Interstellar",
    "The Dark Knight",
    "Parasite",
    "Hereditary",
    "The Conjuring",
    "Get Out",
    "A Quiet Place",
    "Midsommar"
]

# 👇 Replace with your announcement/text channel ID
CHANNEL_ID = 1406165038741323796  

def fetch_movie(movie_name: str) -> str:
    """Fetch movie info from OMDB API and format the message."""
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_KEY}"
    response = requests.get(url).json()

    if response.get("Response") == "True":
        return (
            f"🎬 **Movie of the Day:** {response['Title']} ({response['Year']})\n"
            f"⭐ IMDB: {response['imdbRating']}\n"
            f"📖 {response['Plot']}"
        )
    return f"🎬 Movie of the Day: {movie_name}"

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("⚠️ Channel not found. Double-check CHANNEL_ID.")
        await bot.close()
        return

    # Check if bot has permission
    perms = channel.permissions_for(channel.guild.me)
    if not perms.send_messages:
        print("🚫 Bot does not have permission to send messages in this channel.")
        await bot.close()
        return

    # Pick a random movie and fetch info
    movie = random.choice(MOVIES)
    message = fetch_movie(movie)

    try:
        if isinstance(channel, discord.TextChannel):
            # Normal text channel
            await channel.send(message)

        elif isinstance(channel, discord.NewsChannel):
            # Announcement channel → send inside a thread
            sent_message = await channel.send("📢 New Movie Recommendation!")
            await sent_message.create_thread(name="Daily Movie", auto_archive_duration=60)
            thread = sent_message.thread
            if thread:
                await thread.send(message)

        print(f"📢 Sent movie recommendation to #{channel.name}")

    except discord.Forbidden:
        print("❌ Missing permissions: could not send the message.")

    await bot.close()  # Exit after sending

bot.run(TOKEN)
