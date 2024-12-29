import random
import discord
from discord.ext import commands
from discord import app_commands
from typing import Literal, List


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

global_characters = {}

class Character():
    def __init__(self, name:str, current_points:int, log:str) -> None:
        self.name = name
        self.current_points = current_points
        self.log = log
    def add_point(self, comment) -> None:
        self.current_points += 1
        self.log += comment
    def sub_point(self, comment) -> None:
        self.current_points 

def character_embed(character:Character) -> discord.Embed:
    embed = discord.Embed(title = character.name)
    embed.add_field(name='Points', value=character.current_points)
    embed.add_field(name="Log", value=character.log)
    return embed

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

    @fate_group.command(name="points", description="Manage and view Fate Points for a given character")
    @app_commands.describe(
        character_name = 'Name of the character',
        action = 'Show = show the current points the character has \nAdd = add a Fate Point \nSubtract = subtract a Fate Point',
        message = 'When adding or subtracting a fate point, record why',
        ephemeral = 'Whether to hide the message so only you can see it. Only used for "Show" messages.'
    )
    async def fate_points(self, interaction: discord.Interaction, character_name:str, action:Literal['Show', 'Add', 'Subtract']='Show', message:str='', ephemeral:bool=True):
        if character_name not in global_characters.keys():
            global_characters[character_name] = Character(character_name, 3, "Initial 3 points")
        thisCharacter = global_characters[character_name] 
        match action:
            case 'Add':
                thisCharacter.current_points += 1
                thisCharacter.log += f'\n `+ 1` \t{message}'
                ephemeral = False
            case 'Subtract':
                thisCharacter.current_points -= 1
                thisCharacter.log += f'\n `- 1` \t{message}'
                ephemeral = False
        await interaction.response.send_message(embed=character_embed(thisCharacter), ephemeral=ephemeral)

    @fate_group.command(name="clear", description="Clear a character from the list for tracking Fate points.")
    @app_commands.describe(
        character_name="Name of the character to remove from the list. If this is blank, it will clear the whole list."
    )
    async def fate_reset_points(self, interaction:discord.Integration, character_name:str=''):
        if character_name in global_characters.keys():
            global_characters.pop(character_name)
            await interaction.response.send_message(f'`Cleared {character_name} from character list`')
        elif character_name == '':
            global_characters.clear()
            await interaction.response.send_message('`Cleared character list`')
        else:
            await interaction.response.send_message('`Failed to clear anyone from the list`')

    @fate_points.autocomplete('character_name')
    @fate_reset_points.autocomplete('character_name')
    async def character_list_autocomplete(self, interaction: discord.Integration, current:str) -> List[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=character_name, value=character_name)
            for character_name in list(global_characters.keys()) if current.lower() in character_name.lower()
        ]
    


async def setup(bot):
    await bot.add_cog(Fate(bot)) 