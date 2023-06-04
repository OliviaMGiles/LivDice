import random
import re
from typing import Literal, Optional
import discord
from discord import app_commands
from discord.ext    import commands
from discord.ext.commands import Context
import logging

logging.basicConfig(level=logging.DEBUG)

def exploding_roll(sides:int, explode:bool):
    """Rolls a 1d{sides} and if the value is {sides} and explode is true, it rolls again \n
    first return value contains the sum\n
    second return value contains a string that shows the explosions :boom:
    """
    roll = random.randint(1, sides)
    fancy_log = f'{roll}'
    sum = roll
    explostion_happened = False
    while explode and roll == sides:
        roll = random.randint(1, sides)
        fancy_log += f' :boom: {roll}'
        sum += roll
        explostion_happened = True
    # Check to see if explosions happened, if yes, put the sum on the log
    if explostion_happened:
        fancy_log += f" = {sum}"
    return sum, fancy_log

class general(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self, ctx: Context, sync_options: Optional[Literal["global", "clear", "clear_global"]] = None):
        """Syncs slash commands
            When to sync: https://gist.github.com/AbstractUmbra/a9c188797ae194e592efe05fa129c57f#file-4-when_to_sync-md
            If you want to push changes to global, run the ';sync global' command. Then run the ';sync clear' command
        """
        if sync_options == 'global':
            logging.debug('Syncing globaly')
            synced = await ctx.bot.tree.sync()
            await ctx.send(f'Synced {len(synced)} commands to global. This can take up to an hour to update.')
        elif sync_options == 'clear':
            logging.debug(f'Clearing guild commands')
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            await ctx.send('Cleared guild commands')
        elif sync_options == 'clear_global':
            logging.debug('Clearing global commands')
            ctx.bot.tree.clear_commands(guild=None)
            await ctx.bot.tree.sync()
            await ctx.send('Cleared global commands. This can take up to an hour to update.')
        else:
            logging.debug('Syncing to current guild')
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
            await ctx.send(f'Synced {len(synced)} commands to current guild')

    @app_commands.command(name='roll', description='Roll [-+]?\d*d\d+!?|[-+]?\d+ dice')
    @app_commands.describe(
        dice='Comma separated, each term should match: [-+]?<quantity>*d<sides>+!?|[-+]?<constant modifier>',
        comment='Whatcha rolling for?'
    )
    async def roll_dice(self, interaction: discord.Interaction, dice: str, comment:str=''):
        dice = dice.lower()
        pools = dice.split(',')
        result = []
        for pool in pools:
            terms = re.findall("[-+]?\d*d\d+!?|[-+]?\d+", pool)
            summation = 0
            for term in terms:
                explode = False
                # Resolve if explostion
                if re.search("!", term):
                    explode = True
                    term = term.strip('!')
                # Resolve die rolls
                if re.search("\d*d\d+", term):
                    quantity, sides = term.split('d')
                    if quantity == '': # If the quantity is left out, assume 1
                        quantity = 1
                    quantity = int(quantity)
                    sides = int(sides)
                    if quantity <= 0: # If the quantity is negative, the rolls should be subtracted from the total
                        quantity = 1-quantity
                        for _ in range(quantity):
                            summation -= exploding_roll(sides, explode)[0]
                    else:
                        for _ in range(quantity):
                            summation += exploding_roll(sides, explode)[0]
                # else it is a constant modifier
                else:
                    summation += int(term)
            result.append(summation)

        await interaction.response.send_message(f'{"**"+comment+":** " if comment != "" else ""}{dice} ➔ {result}')

async def setup(bot):
    await bot.add_cog(general(bot)) 