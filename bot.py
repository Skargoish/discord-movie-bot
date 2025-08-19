import os
import discord
import random
import aiohttp
import asyncio
from discord.ext import commands
from datetime import datetime, timedelta

TOKEN = os.getenv("DISCORD_TOKEN")
OMDB_KEY = os.getenv("OMDB_API_KEY")

CHANNEL_ID = 1406165038741323796  
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

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            response = await resp.json()

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

async def send_daily_movie():
    """Send a movie recommendation in the announcements channel."""
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        channel = await bot.fetch_channel(CHANNEL_ID)

    if channel:
        embed = await fetch_movie()
        await channel.send(embed=embed)
        print("📢 Sent daily movie recommendation")

async def schedule_daily_task(target_hour=12, target_minute=0):
    """Schedules the first run at the next target time, then repeats every 24h."""
    now = datetime.utcnow()
    target_time = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)

    if now >= target_time:
        target_time += timedelta(days=1)

    wait_seconds = (target_time - now).total_seconds()
    print(f"⏰ Waiting {int(wait_seconds)}s until first daily run at {target_time} UTC")

    await asyncio.sleep(wait_seconds)

    while True:
        await send_daily_movie()
        await asyncio.sleep(24 * 60 * 60)  # 24h

# --- Manual command ---
@bot.command(name="movie")
async def movie_command(ctx):
    """Manually trigger a movie recommendation (only in announcements channel)."""
    if ctx.channel.id != CHANNEL_ID:
        await ctx.message.delete()
        return

    embed = await fetch_movie()
    await ctx.send(embed=embed)
    print(f"🎬 Sent manual movie recommendation in #{ctx.channel.name}")

    # delete the user's command message after execution
    await ctx.message.delete()

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

    if TEST_MODE:
        await send_daily_movie()
        await bot.close()
    else:
        bot.loop.create_task(schedule_daily_task(12, 0))  # daily at 12:00 UTC
        print("📅 Daily movie scheduler started")

bot.run(TOKEN)
