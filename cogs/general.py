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
    explosion_log = f'{roll}'
    sum = roll
    while explode and roll == sides:
        roll = random.randint(1, sides)
        explosion_log += f' :boom: {roll}'
        sum += roll
    return sum, explosion_log

# Each term is a number of equal-sized dice, or it is a modifier
# This function returns the log of individual dice results, the sign of the term, and the sum
def resolve_dice_term(term):
    explode = False
    results = ''
    sum = 0
    sign = "+"
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
        result_set = []
        sides = int(sides)
        if quantity <= 0: # If the quantity is negative, the rolls should be subtracted from the total
            sign = "-"
            quantity = 0-quantity
            for _ in range(quantity):
                die_sum, explosion_log = exploding_roll(sides, explode)
                sum -= die_sum
                result_set.append(explosion_log)
        else:
            for _ in range(quantity):
                die_sum, explosion_log = exploding_roll(sides, explode)
                sum += die_sum
                result_set.append(explosion_log)
        results = f'[{", ".join(result_set)}]'
    # else it is a constant modifier
    else:
        term = int(term)
        if term <= 0: # If the constant modifier is negative, set the sign to negative
            sign = "-"
        sum += term
        results = abs(term)
    return str(results), sign, sum

# Each pool can be made of multiple dice and modifiers, called "terms"
# This function retruns the log of the dice pool, and the sum of the terms
def resolve_dice_pool(pool):
    terms = re.findall("[-+]?\d*d\d+!?|[-+]?\d+", pool)
    results = ''
    sum = 0
    first = True
    for term in terms:
        term_result, term_sign, term_sum = resolve_dice_term(term)
        if first and term_sign == "+":
            results += term_result
        else:
            results += term_sign + term_result
        sum += term_sum
        first = False
    return results, str(sum)

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
        dice='Comma separated, each term should match: [-+]?<quantity>*d<sides>+!?|[-+]?<constant modifier>\nUse "!" to indicate the dice should explode.',
        comment='Whatcha rolling for?'
    )
    async def roll_dice(self, interaction: discord.Interaction, dice: str, comment:str=''):
        dice = dice.lower()
        pools = dice.split(',')
        results = []
        result_sum = []
        results, result_sum = zip(*(resolve_dice_pool(pool) for pool in pools))
        formatted_response = f'{"**"+comment+":** " if comment != "" else ""}{dice}'
        formatted_response += f'\nResults: {", ".join(results)}'
        formatted_response += f'\nSum: {", ".join(result_sum)}'
        await interaction.response.send_message(formatted_response)

async def setup(bot):
    await bot.add_cog(general(bot)) 