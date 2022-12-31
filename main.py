import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import logging

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
APPLICATION_ID = os.getenv('APPLICATION_ID')

class LivDice(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix=';', 
            intents=intents, 
            application_id=APPLICATION_ID)

    async def startup(self):
        await bot.wait_until_ready()
        logging.info(f'{bot.user.name} is connected to Discord!')

    async def setup_hook(self):
        for file in os.listdir('./cogs'):
            if file.endswith('py'):
                try:
                    await bot.load_extension(f'cogs.{file[:-3]}')
                    logging.info(f'Loaded {file}')
                except Exception as e:
                    logging.warn(f'Failed to load {file}')
                    logging.warn(f'[ERROR] {e}')
        self.loop.create_task(self.startup()) 

bot = LivDice()
bot.run(TOKEN)