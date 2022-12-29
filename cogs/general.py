import random
from typing import Literal, Optional
import discord
from discord import app_commands
from discord.ext    import commands
from discord.ext.commands import Context
import logging

logging.basicConfig(level=logging.DEBUG)

class general(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self, ctx: Context, sync_options: Optional[Literal["global", "clear", "clear_global"]] = None):
        """Syncs slash commands
            When to sync: https://gist.github.com/AbstractUmbra/a9c188797ae194e592efe05fa129c57f#file-4-when_to_sync-md
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

    @commands.command(aliases=['r','roll'])
    async def roll_dice(self, ctx: Context, dice: str):
        """Alieses = r, roll. Use NdN or format. Simulates rolling dice.
        """
        try:
            rolls, sides = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Bad format! Use NdN format', reference=ctx.message)
            return
        result = ', '.join(str(random.randint(1,sides)) for r in range(rolls))
        await ctx.send(result, reference=ctx.message)

    @app_commands.command(name="test", description="Testing slash commands")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message('Testing!')

async def setup(bot):
    await bot.add_cog(general(bot)) 