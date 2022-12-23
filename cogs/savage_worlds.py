import random
import math
import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
from typing import Literal, List
import logging

global_parties = {}
global_characters = {}
statuses = {
    'Shaken': 'Shaken characters may only move and take free actions. At the start of their turn, characters automatically make a Spirit roll to recover from being Shaken as afree action.',
    'Distracted': 'The character suffers -2 to all Trait rolls until the end of his next turn.',
    'Vulnerable': 'Actions and attacks against the target are made at +2 until the end of his next turn.',
    'Entangled': 'The victim can’t move and is Distracted as long as he remains Entangled.',
    'Bound': 'The victim may not move, is Distracted and Vulnerable as long as he remains Bound, and cannot make physical actions other than trying to break free.',
    'Fatigued': '-1 to all Trait rolls. If he takes another level of Fatigue, he’s Exhausted.',
    'Exhausted': '-2 to all Trait rolls. If he takes another level of Fatigue, he’s Incapacitated.',
    'Stunned': 'A Stunned character is Distracted (removed at the end of his next turn as usual), Vulnerable (until he recovers), falls prone, can’t take actions, or move. At the start of each turn thereafter, he automatically makes a Vigor roll as a free action. Success means he’s no longer Stunned but remains Vulnerable until the end of his turn. With a raise, his Vulnerable state goes away at the end of this turn.',
    'Wounded': '-1 to Pace, -1 to all Trait rolls.',
    'Wounded x2': '-2 to Pace, -2 to all Trait rolls.',
    'Wounded x3': '-3 to Pace, -3 to all Trait rolls.',
    'Incapacitated': 'Characters may not perform actions but are still dealt Action Cards to track power effects or in case they recover.',
    'Bleeding out': 'Failure -> death, Success -> survive until next turn, Raise -> stabilizes',
    'Dead': ':skull:'
}

def character_embed(character) -> discord.Embed:
    """Makes an embed for a charcter that lists their statuses"""
    embed = discord.Embed(title = character)
    if character not in global_characters.keys():
        global_characters[character] = []
    if global_characters[character] == []:
        embed.add_field(name='Healthy', value=':green_heart:')
    for status in global_characters[character]:
        embed.add_field(name=status, value=statuses[status])
    return embed

def party_embed(party) -> discord.Embed:
    """Formats a party list of characters into an embed."""
    embed = discord.Embed(title=party)
    for party_member in global_parties[party]:
        pretty_status = ''
        if global_characters[party_member] == []:
            pretty_status = "`Healthy`"
        else:
            for status in global_characters[party_member]:
                pretty_status += f"`{status}` "
        embed.add_field(name=party_member, value=(f'*Status:* {pretty_status}'))
    return embed

def exploding_roll(max:int):
    """Rolls a 1d{max} and if the value is {max} it rolls again \n
    first return value contains the sum\n
    second return value contains a string that shows the explosions :boom:
    """
    roll = random.randint(1, max)
    fancy_log = f'{roll}'
    sum = roll
    explostion_happened = False
    while roll == max:
        roll = random.randint(1, max)
        fancy_log += f' :boom: {roll}'
        sum += roll
        explostion_happened = True
    # Check to see if explosions happened, if yes, put the sum on the log
    if explostion_happened:
            fancy_log += f" = {sum}"
    return sum, fancy_log

########################################################################################################################

class Savage_Worlds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    sw_group = app_commands.Group(name="sw", description="Savage Worlds commands")

    @sw_group.command(name='status', description='Show and edit the statuses on a character.')
    @app_commands.describe(
        character='Who to apply the statuses to.',
        add_status='Status to add. Options from autocomplete will have descriptions too.',
        remove_status='Status to remove. Options from autocomplete are statuses the character has.'
    )
    async def status(self, interaction: discord.Interaction, character: str, add_status: str="", remove_status: str="", ephemeral:bool = True):
        if character in global_characters.keys():
            current_status = global_characters[character]
            if add_status != "":
                current_status.append(add_status)
            if remove_status in current_status:
                current_status.remove(remove_status)
            global_characters[character] = current_status
        else:
            current_status = add_status
            global_characters[character] = [current_status]
        logging.debug(f'global_characters: {global_characters}')
        await interaction.response.send_message(embed=character_embed(character), ephemeral=ephemeral)

    @status.autocomplete('character')
    async def characters_autocomplete(self, interaction: discord.Interaction, current:str) -> List[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=character, value=character)
            for character in list(global_characters.keys()) if current.lower() in character.lower()
        ]

    @status.autocomplete('add_status')
    async def statuses_autocomplete(self, interaction: discord.Interaction, current:str) -> List[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=status, value=status)
            for status in list(statuses.keys()) if current.lower() in status.lower()
        ]

    @status.autocomplete('remove_status')
    async def remove_statuses_autocomplete(self, interaction: discord.Interaction, current:str) -> List[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=status, value=status)
            for status in list(global_characters[interaction.namespace.character]) if current.lower() in status.lower()
        ]

    @sw_group.command(name='add_status', description='Add a new custom status along with a description.')
    @app_commands.describe(
        status_name='Name of the status',
        status_description='Describe what the status does mechanically.'
    )
    async def add_status(self, interaction: discord.Interaction, status_name: str, status_description:str):
        global statuses
        statuses.update({status_name: status_description})
        await interaction.response.send_message(f'Added {status_name}', ephemeral=True)

    @sw_group.command(name='party', description='Show the state of the party and add characters.')
    @app_commands.describe(
        characters='Characters to add to the party.',
        party_name='Name of the party.',
        ephemeral='Whether to send as an ephemeral message or not. Default is True.'
    )
    async def party(self, interaction: discord.Interaction, characters: str="", party_name: str="", ephemeral:bool=True):
        global global_parties
        global global_characters
        if characters == "":
            if global_parties == {}:
                await interaction.response.send_message(f'There is no party.', ephemeral=ephemeral)
            elif party_name in global_parties.keys():
                await interaction.response.send_message(embed=party_embed(party_name), ephemeral=ephemeral)
            else:
                embeds = []
                for party in global_parties:
                    embeds.append(party_embed(party))
                await interaction.response.send_message(f'These are all the parties:', embeds=embeds, ephemeral=ephemeral)
        roster = []
        if characters != "":
            list_of_names = characters.split(' ')
            for name in list_of_names:
                roster.append((name))
                if name not in global_characters.keys():
                    global_characters[name] = []
            if party_name == "":
                party_name = "Party"
            if party_name in global_parties.keys():
                # prevent duplicates
                roster = list(set(global_parties[party_name] + roster))
            global_parties[party_name] = roster
            await interaction.response.send_message(embed=party_embed(party_name),ephemeral=ephemeral)

    @sw_group.command(name='disolve_party', description='Party’s over!')
    @app_commands.describe(
        party = 'The party you want to end. Default is to end all parties.',
        ephemeral='Whether to send as an ephemeral message or not. Default is True.'
    )
    async def disolve_party(self, interaction: discord.Interaction, party: str="", ephemeral: bool=True):
        if party == "":
            global_parties.clear()
            await interaction.response.send_message('*All* Parties are over!', ephemeral=ephemeral)
        elif party in global_parties.keys():
            del global_parties[party]
            await interaction.response.send_message('Party’s over!', ephemeral=ephemeral)
        else:
            await interaction.response.send_message(f'There isn’t a party named {party}. (The party *might* go on...)', ephemeral=ephemeral)

    @sw_group.command(name='kick_partymemeber', description='For when someone is being a pooper.')
    @app_commands.describe(
        party_member='The party member to remove from the party.',
        party='The party from which to remove the offender. Default is all parties.',
        ephemeral='Whether to send as an ephemeral message or not. Default is True.'
    )
    async def kick_partymemeber(self, interaction: discord.Interaction, party_member: str, party: str='', ephemeral: bool=True):
        response = f'{party_member} is a loner. They were never even in a party.'
        if party in global_parties.keys():
            response = f'{party_member} was never even in {party}. They are uninvited anyway!'
            if party_member in global_parties[party]:
                global_parties[party].remove(party_member)
                response = f'{party_member} has left {party}.'
        else:
            for existing_party in global_parties.keys():
                if party_member in global_parties[existing_party]:
                    global_parties[existing_party].remove(party_member)
                    response = f'{party_member} has left all parties they were in.'
        await interaction.response.send_message(response, ephemeral=ephemeral)

    @kick_partymemeber.autocomplete('party_member')
    async def characters_autocomplete(self, interaction: discord.Interaction, current:str) -> List[app_commands.Choice[str]]:
        # If 'party' is filled in, give options for characters in that party
        if interaction.namespace.party != None:
            autofill = [
                app_commands.Choice(name=character, value=character)
                for character in list(global_parties[interaction.namespace.party]) if current.lower() in character.lower()
            ]
        else: # Else, give a list of all charcters
            autofill = [
                app_commands.Choice(name=character, value=character)
                for character in list(global_characters.keys()) if current.lower() in character.lower()
            ]
        return autofill

    @party.autocomplete('party_name')
    @disolve_party.autocomplete('party')
    @kick_partymemeber.autocomplete('party')
    async def parties_autocomplete(self, interaction: discord.Interaction, current:str) -> List[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=character, value=character)
            for character in list(global_parties.keys()) if current.lower() in character.lower()
        ]

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
        modifier='The modifier to the roll. Defaults to 0.'
    )
    @app_commands.choices(trait=[
        Choice(name='Unskilled', value=2),
        Choice(name='d4', value=4),
        Choice(name='d6', value=6),
        Choice(name='d8', value=8),
        Choice(name='d10', value=10),
        Choice(name='d12', value=12)
    ])
    async def trait(self, interaction: discord.Interaction, trait:Choice[int], wild_die: Literal['Yes', 'No']='Yes', modifier: int=0):
        """Trait Roll for Savage worlds
        Unskilled rolls: roll a d4 for skill die (+ a wild die if present) and subtract 2 from the total.
        Raises happen every 4 points over the Target Number. Raises are calculated after adjusting for modifiers.
        Critical failures occure when a Wild Card rolls a 1 on both skill die and Wild Die.
        """
        if trait.value == 2:
            # roll a d4 and subtract 2
            trait_roll, trait_roll_log = exploding_roll(4)
            modifier += -2
        else:
            trait_roll, trait_roll_log = exploding_roll(trait.value)
        
        if wild_die == 'Yes':
            wild_roll, wild_roll_log = exploding_roll(6)
        else:
            wild_roll = 0
        
        roll_total = max(trait_roll, wild_roll) + modifier
        # Evaluate for failures or successes
        if trait_roll==1 and wild_roll ==1:
            result = 'Critical Failure!'
        elif roll_total < 4:
            result = 'Failure'
        elif roll_total >= 4:
            result = 'Success!'
            #Check for raises every 4 points
            raises = math.floor((roll_total-4)/4)
            if raises >= 1:
                result = f'Success with {raises} raises!'
        await interaction.response.send_message(f'Rolled: [{trait_roll_log}{ ", " + wild_roll_log if wild_roll != 0 else ""}] {"+" if (modifier >= 0) else ""} {modifier} \nResult: {result}')


async def setup(bot):
    await bot.add_cog(Savage_Worlds(bot)) 
