import logging
import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
import mysql.connector

load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(name)s: %(message)s",
    handlers=[
        logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w'),
        logging.StreamHandler()  # Esto también imprime en consola (opcional)
    ]
)






token = os.getenv('DISCORD_TOKEN')


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='s', intents=intents)


@bot.event
async def on_ready():
    print(f"toy listo, {bot.user.name} \n ------------")

async def main():
    await bot.load_extension("gpt_chat")
    await bot.load_extension("mudae_a_pitusas")
    await bot.start(token)

asyncio.run(main())



