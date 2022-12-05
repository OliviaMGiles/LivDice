import os
import random
import discord
from discord import app_commands
from discord.ext    import commands

class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f'Synced {len(fmt)} commands.')

    @commands.command(aliases=['r','roll'])
    async def roll_dice(self, ctx, dice: str):
        """Alieses = r, roll. Use _d_ format. Simulates rolling dice.
        """
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Bad format! Use _d_ format', ephemeral=True)
            return
        result = ', '.join(str(random.randint(1,limit)) for r in range(rolls))
        await ctx.send(result)

    @app_commands.command(name="test", description="Testing slash commands")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message('Testing!')

async def setup(bot):
    await bot.add_cog(general(bot), guilds=[discord.Object(id=os.getenv('DISCORD_GUILD_ID'))]) 