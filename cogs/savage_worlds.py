import random
import discord
from dotenv import load_dotenv
from discord.ext    import commands
from discord import app_commands

class Savage_Worlds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command(aliases=['r','roll'])
    # async def roll_dice(self, ctx, dice: str):
    #     """Alieses = r, roll. Use _d_ format. Simulates rolling dice.
    #     """
    #     try:
    #         rolls, limit = map(int, dice.split('d'))
    #     except Exception:
    #         await ctx.send('Bad format! Use _d_ format', ephemeral=True)
    #         return
    #     result = ', '.join(str(random.randint(1,limit)) for r in range(rolls))
    #     await ctx.send(result)

    @commands.command(aliases=['i'])
    async def initiative(self, ctx, *characters):
        """Generates initiative order using cards.
        Input: ;initiative Alice Bob Charlie Eve
        Output: Charlie: :black_joker: Joker! Act whenever you want in the round!
                Eve: Q ♦︎
                Bob: 10 ♥︎
                Alice: 10 ♣︎
        """
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
        return await ctx.send('Something went wrong',ephemeral=True)

    @app_commands.command(name="savage", description="Roll Savage World dice")
    async def savage(self, interaction: discord.Interaction, dice_size, wild_die):
        die1 = random.randint(1,dice_size)
        if wild_die == 'y':
            die2 = random.randint(1,6)
        result = max(die1, die2)
        await interaction.response.send_message(f'Rolled {result}')

async def setup(bot):
    await bot.add_cog(Savage_Worlds(bot)) 
