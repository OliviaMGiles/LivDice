import random
import discord
from discord.ext import commands
from discord import app_commands


ladder = {
    8: 	'Legendary :tada::exploding_head::tada:',
    7: 	'Epic :triumph:',
    6: 	'Fantastic :partying_face:',
    5: 	'Superb :star_struck:',
    4: 	'Great :grin:',
    3: 	'Good :grinning:',
    2: 	'Fair :slight_smile:',
    1: 	'Average :neutral_face:',
    0: 	'Mediocre :slight_frown:',
    -1: 'Poor :disappointed_relieved:',
    -2: 'Terrible :confounded:',
    -3: 'Abysmal :sob:',
    -4: 'Despair :skull:'
}

def fate_die_roll():
    return random.choice([
            -1,
            0,
            1
        ])

class Fate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    fate_group = app_commands.Group(name="fate", description="Fate commands")

    @fate_group.command(name="roll", description="Roll Fate Dice")
    @app_commands.describe(
        rating="The rating of the skill. This will be added to the result.",
        comment='Whatcha rolling for?'
    )
    async def fate_roll(self, interaction: discord.Interaction, rating: int=0, comment: str=''):
        """Dice Roll for Fate
        Roll 4 dice, each of wich can be a "-", " ", or "+" for -1, +0, and +1.
        Add the skill ranking to the raw dice result to get the final outcome.
        """
        dice_results = [fate_die_roll(), fate_die_roll(), fate_die_roll(), fate_die_roll()]
        result_sum = dice_results[0]+dice_results[1]+dice_results[2]+dice_results[3] + rating
        formatted_result = f'{comment}\n{dice_results}'
        if rating !=0:
            formatted_result += f'{" +" if rating > 0 else " "}{rating}'
        formatted_result += f'\nResult: **{result_sum}**'
        if result_sum in range(-4, 8):
            formatted_result+= f' = {ladder[result_sum]}'
        elif result_sum > 8:
            formatted_result+= f' = Infinite Celestial :fireworks::crown::fireworks:'
        await interaction.response.send_message(formatted_result)

async def setup(bot):
    await bot.add_cog(Fate(bot)) 