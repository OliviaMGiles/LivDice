import os
import random
import discord
from dotenv import load_dotenv
from discord.ext    import commands

class Savage_Worlds(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['i'])
    async def initiative(self, ctx, *characters):
        """ Generates initiative order using cards.
        Input: ;initiative Alice Bob Charlie Eve
        Output: Charlie: :black_joker: Joker! Act whenever you want in the round!
                Eve: Q :diamonds:
                Bob: 10 :hearts:
                Alice: 10 :clubs:
        """
        deck = {1:':black_joker: Joker! Act whenever you want in the round! Also add +2 to all Trait and damage rolls this round!',
        2:':black_joker: Joker! Act whenever you want in the round! Also add +2 to all Trait and damage rolls this round!', 
        3:'Ace :spades:', 4:'Ace :hearts:', 5:'Ace :diamonds:', 6:'Ace :clubs:',
        7:'King :spades:',8:'King :hearts:',9:'King :diamonds:',10:'King :clubs:',
        11:'Queen :spades:',12:'Queen :hearts:',13:'Queen :diamonds:',14:'Queen :clubs:',
        15:'Jack :spades:',16:'Jack :hearts:',17:'Jack :diamonds:',18:'Jack :clubs:',
        19:'10 :spades:',20:'10 :hearts:',21:'10 :diamonds:',22:'10 :clubs:',23:'9 :spades:',24:'9 :hearts:',25:'9 :diamonds:',26:'9 :clubs:',
        27:'8 :spades:',28:'8 :hearts:',29:'8 :diamonds:',30:'8 :clubs:',31:'7 :spades:',32:'7 :hearts:',33:'7 :diamonds:',34:'7 :clubs:',
        35:'6 :spades:',36:'6 :hearts:',37:'6 :diamonds:',38:'6 :clubs:',39:'5 :spades:',40:'5 :hearts:',41:'5 :diamonds:',42:'5 :clubs:',
        43:'4 :spades:',44:'4 :hearts:',45:'4 :diamonds:',46:'4 :clubs:',47:'3 :spades:',48:'3 :hearts:',49:'3 :diamonds:',50:'3 :clubs:',
        51:'2 :spades:',52:'2 :hearts:',53:'2 :diamonds:',54:'2 :clubs:'}
        cards_drawn = random.sample(range(1,54), len(characters))
        result_map = {}
        for character in characters:
            card_number_for_character = cards_drawn[characters.index(character)]
            result_map[card_number_for_character] = f'**{character}:** {deck[card_number_for_character]}'
        
        sorted_results = sorted(result_map.items())
        result = '__Initiative Order:__\n'
        for _, value in sorted_results:
            result += f'{value}\n'
        await ctx.send(result)
        
    @initiative.error
    async def initiative_error(ctx: commands.Context, error: commands.CommandError):
        return await ctx.send('Something went wrong')

async def setup(bot):
    await bot.add_cog(Savage_Worlds(bot)) 
