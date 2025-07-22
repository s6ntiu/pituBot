import discord
import os
from discord.ext import commands
import logging
from dotenv import load_dotenv
import requests

# This bot function was initially made to search for anime via discord chat, although it may change in the future.

load_dotenv()
mal = os.getenv("MAL_CLIENT_ID")

def buscar_anime(nombre):
    url = 'https://api.myanimelist.net/v2/anime'
    headers = {
        'X-MAL-CLIENT-ID': mal
    }
    params = {
        'q': nombre,
        'limit': 1,
        'fields': 'id,title,main_picture,synopsis,mean,rank,genres,start_date,num_list_users'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return None
    data = response.json()
    if 'data' not in data or len(data['data']) == 0:
        return None
    return data['data'][0]['node']

async def setup(bot):
    @bot.command()
    async def anime(ctx, *, nombre):
        await ctx.typing()
        anime = buscar_anime(nombre)
        generos = ', '.join([g['name'] for g in anime.get('genres', [])])
        if not anime:
            await ctx.send("No encontré ningún anime con ese nombre.")
            return

        embed = discord.Embed(
            title=anime['title'],
            description=anime.get('synopsis', 'Sin sinopsis.')[:500] + '...',
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=anime['main_picture']['medium'])
        embed.add_field(name='Score', value=str(anime.get('mean', 'N/A')), inline=True)
        embed.add_field(name='Rank', value=str(anime.get('rank', 'N/A')), inline=True)
        embed.add_field(name='Genres', value=generos if generos else 'N/A', inline=True)
        embed.add_field(name='Start Date', value=str(anime.get('start_date', 'N/A')), inline=True)
        embed.add_field(name='Members', value=str(anime.get('num_list_users', 'N/A')), inline=True)
        embed.set_footer(text="Información de myanimelist.net")

        await ctx.send(embed=embed)