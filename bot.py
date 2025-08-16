import os
import discord
import requests
import random
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
OMDB_KEY = os.getenv("OMDB_API_KEY")  # make sure the secret name matches exactly!
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))  # add this as a secret too

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

movies = ["Inception", "The Matrix", "Interstellar", "The Dark Knight", "Parasite", "Get Out", "A Quiet Place"]

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)

    if channel:
        movie = random.choice(movies)
        url = f"http://www.omdbapi.com/?t={movie}&apikey={OMDB_KEY}"
        response = requests.get(url).json()

        if response.get("Response") == "True":
            embed = discord.Embed(
                title=f"🎬 {response['Title']} ({response['Year']})",
                description=response.get("Plot", "No plot available."),
                color=discord.Color.red()
            )
            embed.add_field(name="⭐ IMDB", value=response.get("imdbRating", "N/A"))
            embed.add_field(name="🎭 Genre", value=response.get("Genre", "N/A"))
            embed.add_field(name="🎬 Director", value=response.get("Director", "N/A"))
            embed.set_image(url=response.get("Poster"))

            await channel.send(embed=embed)
        else:
            await channel.send(f"🎬 Movie of the Day: {movie}")

    await bot.close()  # stop after posting

bot.run(TOKEN)
