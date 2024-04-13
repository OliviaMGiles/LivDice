import random
import math
import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
from typing import Literal, List
from .general import exploding_roll

class Savage_Worlds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    sw_group = app_commands.Group(name="sw", description="Savage Worlds commands")

    @sw_group.command(name="initiative") 
    @app_commands.describe(
        characters='List of characters for the initiative round. White space delimited.'
    )
    async def initiative(self, interaction: discord.Interaction, characters: str):
        """Generates initiative order using cards."""
        # Parse characters: str into a list of characters
        character_list = characters.split(' ')

        # Define the deck and draw chards for each character
        deck = {1:':black_joker: Joker! Act whenever you want in the round! Also add +2 to all Trait and damage rolls this round!',
        2:':black_joker: Joker! Act whenever you want in the round! Also add +2 to all Trait and damage rolls this round!', 
        3:'Ace ♠︎', 4:'Ace ♥︎', 5:'Ace ♦︎', 6:'Ace ♣︎',
        7:'King ♠︎',8:'King ♥︎',9:'King ♦︎',10:'King ♣︎',
        11:'Queen ♠︎',12:'Queen ♥︎',13:'Queen ♦︎',14:'Queen ♣︎',
        15:'Jack ♠︎',16:'Jack ♥︎',17:'Jack ♦︎',18:'Jack ♣︎',
        19:'10 ♠︎',20:'10 ♥︎',21:'10 ♦︎',22:'10 ♣︎',23:'9 ♠︎',24:'9 ♥︎',25:'9 ♦︎',26:'9 ♣︎',
        27:'8 ♠︎',28:'8 ♥︎',29:'8 ♦︎',30:'8 ♣︎',31:'7 ♠︎',32:'7 ♥︎',33:'7 ♦︎',34:'7 ♣︎',
        35:'6 ♠︎',36:'6 ♥︎',37:'6 ♦︎',38:'6 ♣︎',39:'5 ♠︎',40:'5 ♥︎',41:'5 ♦︎',42:'5 ♣︎',
        43:'4 ♠︎',44:'4 ♥︎',45:'4 ♦︎',46:'4 ♣︎',47:'3 ♠︎',48:'3 ♥︎',49:'3 ♦︎',50:'3 ♣︎',
        51:'2 ♠︎',52:'2 ♥︎',53:'2 ♦︎',54:'2 ♣︎'}
        cards_drawn = random.sample(range(1,54), len(character_list))
        result_map = {}
        for character in character_list:
            card_number_for_character = cards_drawn[character_list.index(character)]
            result_map[card_number_for_character] = f'**{character}:** {deck[card_number_for_character]}'
        
        sorted_results = sorted(result_map.items())
        result = '__Initiative Order:__\n'
        for _, value in sorted_results:
            result += f'{value}\n'
        await interaction.response.send_message(result)

    @sw_group.command(name="trait", description="Roll Savage World dice")
    @app_commands.describe(
        trait='Die size for the trait roll',
        wild_die='Yes if using a wild dice. Defaults to Yes.',
        modifier='The modifier to the roll. Defaults to 0.',
        comment='Whatcha rolling for?'
    )
    @app_commands.choices(trait=[
        Choice(name='Unskilled (d4-2)', value=2),
        Choice(name='d4', value=4),
        Choice(name='d6', value=6),
        Choice(name='d8', value=8),
        Choice(name='d10', value=10),
        Choice(name='d12', value=12)
    ])
    async def trait(self, interaction: discord.Interaction, trait:Choice[int], wild_die: Literal['Yes', 'No']='Yes', modifier: int=0, comment:str=''):
        """Trait Roll for Savage worlds
        Unskilled rolls: roll a d4 for skill die (+ a wild die if present) and subtract 2 from the total.
        Raises happen every 4 points over the Target Number. Raises are calculated after adjusting for modifiers.
        Critical failures occur when a Wild Card rolls a 1 on both skill die and Wild Die.
        """
        if trait.value == 2:
            # roll a d4 and subtract 2
            trait_roll, trait_roll_log = exploding_roll(4, True)
            modifier += -2
        else:
            trait_roll, trait_roll_log = exploding_roll(trait.value, True)
        
        if wild_die == 'Yes':
            wild_roll, wild_roll_log = exploding_roll(6, True)
        else:
            wild_roll = 0
        
        roll_total = max(trait_roll, wild_roll) + modifier
        # Evaluate for failures or successes
        if trait_roll==1 and wild_roll ==1:
            result = 'Critical Failure! :skull:'
        elif roll_total < 4:
            result = 'Failure :x:'
        elif roll_total >= 4:
            result = 'Success! :dart:'
            #Check for raises every 4 points
            raises = math.floor((roll_total-4)/4)
            if raises >= 1:
                result = f'Success with {raises} raise{"s" if raises > 1 else ""}! :dart:'
                for _ in range(raises):
                    result += ":dart:"
        formatted_response = f'{"**"+comment+":** " if comment != "" else "Rolled: "}'
        formatted_response += f'[{trait_roll_log}{ ", " + wild_roll_log if wild_roll != 0 else ""}]'
        if modifier != 0:
            formatted_response += f'{" + " if (modifier >= 0) else ""}{modifier} = {roll_total}'
        formatted_response += f'\nResult: {result}'
        await interaction.response.send_message(formatted_response)


async def setup(bot):
    await bot.add_cog(Savage_Worlds(bot)) 
