import discord
import os
import asyncio

TOKEN = os.getenv("DISCORD_TOKEN")  # from GitHub secret

intents = discord.Intents.default()
client = discord.Client(intents=intents)

CHANNEL_ID = 1406165038741323796  # 👈 replace with your actual channel ID

@client.event
async def on_ready():
    print(f'Bot connected as {client.user}')
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("🎬 Daily Movie Bot is now online!")
    else:
        print("⚠️ Channel not found! Check your channel ID.")

client.run(TOKEN)
