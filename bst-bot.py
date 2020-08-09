import os

from discord.ext import commands
from discord.channel import DMChannel
from dotenv import load_dotenv

from db_utils import save_search, get_recent
from gsearch import g_search

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


bot = commands.Bot(command_prefix='!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == 'hi' and isinstance(message.channel, DMChannel):
        response = 'hey'
        await message.channel.send(response)
    else:
        await bot.process_commands(message)


@bot.command(name='google')
async def google(ctx, query):
    response = g_search(query)
    save_search(query)
    await ctx.send(response)


@bot.command(name='recent')
async def recent(ctx, query):
    response = get_recent(query)
    await ctx.send(response)

bot.run(TOKEN)
