# Tutorial: https://realpython.com/how-to-make-a-discord-bot-python/
import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=';', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} is connected to Discord!')


@bot.command(aliases=['r','roll'], help='Alieses = r, roll. Simulates rolling dice.')
async def roll_dice(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Bad format! Use NdN format')
        return
    result = ', '.join(str(random.randint(1,limit)) for r in range(rolls))
    await ctx.send(result)

bot.run(TOKEN)