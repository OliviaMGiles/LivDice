import os
import random
import discord
from discord import app_commands
from discord.ext    import commands

class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def sync(self, ctx, *sync_global: bool):
        """Syncs slash commands
            When to sync: https://gist.github.com/AbstractUmbra/a9c188797ae194e592efe05fa129c57f#file-4-when_to_sync-md
        """
        if sync_global == True:
            synced = await ctx.bot.tree.sync()
            await ctx.send(f'Synced {len(synced)} commands to global')
        else:
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
            await ctx.send(f'Synced {len(synced)} commands to current guild')

    @commands.command(aliases=['r','roll'])
    async def roll_dice(self, ctx, dice: str):
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
    await bot.add_cog(general(bot), guilds=[discord.Object(id=os.getenv('DISCORD_GUILD_ID'))]) 