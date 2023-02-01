import random
import discord
from discord.ext    import commands
from discord import app_commands
from enum import Enum

dice = Enum('dice', ['ability','proficiency','difficulty','challenge','boost', 'setback'])

class Roll_result():
    def __init__(self, successes:int=0, advantages:int=0, triumphs:int=0, failures:int=0, threats:int=0, despairs:int=0) -> None:
        self.successes = successes
        self.advantages = advantages
        self.triumphs = triumphs
        self.failures = failures
        self.threats = threats
        self.despairs = despairs
    def __str__(self) -> str:
        return f'Successes: {self.successes}, Advantages: {self.advantages}, Triumphs: {self.triumphs}, Failures: {self.failures}, Threats: {self.threats}, Despairs: {self.despairs}'
    def __add__(self, other):
        return Roll_result(self.successes + other.successes, self.advantages + other.advantages, self.triumphs + other.triumphs, 
        self.failures + other.failures, self.threats + other.threats, self.despairs + other.despairs)

def roll_genesys(die: dice) -> Roll_result:
    if die == dice.ability:
        return random.choice([
            Roll_result(), 
            Roll_result(successes=1), 
            Roll_result(successes=1), 
            Roll_result(successes=2), 
            Roll_result(advantages=1),
            Roll_result(advantages=1),
            Roll_result(advantages=2),
            Roll_result(successes=1, advantages=1)])
    elif die == dice.proficiency:
        return random.choice([
            Roll_result(), 
            Roll_result(successes=1), 
            Roll_result(successes=1), 
            Roll_result(successes=2), 
            Roll_result(successes=2),
            Roll_result(advantages=1),
            Roll_result(advantages=2),
            Roll_result(advantages=2),
            Roll_result(successes=1, advantages=1),
            Roll_result(successes=1, advantages=1),
            Roll_result(successes=1, advantages=1),
            Roll_result(triumphs=1)])
    elif die == dice.difficulty:
        return random.choice([
            Roll_result(), 
            Roll_result(failures=1), 
            Roll_result(failures=2), 
            Roll_result(threats=1), 
            Roll_result(threats=1),
            Roll_result(threats=1),
            Roll_result(threats=2),
            Roll_result(failures=1, threats=1)])
    elif die == dice.challenge:
        return random.choice([
            Roll_result(),
            Roll_result(failures=1),
            Roll_result(failures=1),
            Roll_result(failures=2),
            Roll_result(failures=2),
            Roll_result(threats=1), 
            Roll_result(threats=1),
            Roll_result(threats=2),
            Roll_result(threats=2),
            Roll_result(failures=1, threats=1),
            Roll_result(failures=1, threats=1),
            Roll_result(despairs=1)])
    elif die == dice.boost:
        return random.choice([
            Roll_result(),
            Roll_result(), 
            Roll_result(successes=1),
            Roll_result(advantages=1),
            Roll_result(advantages=2),
            Roll_result(successes=1, advantages=1)])
    elif die == dice.setback:
        return random.choice([
            Roll_result(),
            Roll_result(),
            Roll_result(failures=1),
            Roll_result(failures=1),
            Roll_result(threats=1),
            Roll_result(threats=1)])

class Genesys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    genesys_group = app_commands.Group(name="genesys", description="Genesys commands")

    @genesys_group.command(name='roll', description='Roll Genesys dice')
    @app_commands.describe(
        ability='d8 Positive',
        proficiency='d12 Positive',
        difficulty='d8 Negative',
        challenge='d12 Negative',
        boost='d6 Positive',
        setback='d6 Negative',
        comment='Whatcha rolling for?'
    )
    async def roll(self, interaction: discord.Interaction, ability: int=0, proficiency: int=0, difficulty: int=0, challenge:int=0, boost: int=0, setback:int=0, comment:str=''):
        totals = Roll_result()
        for _ in range(ability):
            result = roll_genesys(dice.ability)
            totals += result
        for _ in range(proficiency):
            result = roll_genesys(dice.proficiency)
            totals += result
        for _ in range(difficulty):
            result = roll_genesys(dice.difficulty)
            totals += result
        for _ in range(challenge):
            result = roll_genesys(dice.challenge)
            totals += result
        for _ in range(boost):
            result = roll_genesys(dice.boost)
            totals += result
        for _ in range(setback):
            result = roll_genesys(dice.setback)
            totals += result
        # Calculate the end results.
        net_suceess = (totals.successes + totals.triumphs) - (totals.failures + totals.despairs)
        net_advantages = totals.advantages - totals.threats
        end_result = ""
        if net_suceess > 0:
            end_result += f'{net_suceess} Success{"es" if net_suceess > 1 else ""} :dart:'
        elif net_suceess <= 0:
            end_result += f'Failure :x:'
        if net_advantages > 0:
            end_result += f', {net_advantages} Advantage{"s" if net_advantages > 1 else ""} :arrow_up_small: '
        elif net_advantages < 0:
            end_result += f', {0 - net_advantages} Threat{"s" if net_advantages < -1 else ""} :anger: '
        if totals.triumphs != 0:
            end_result += f'\n\t{totals.triumphs} Triumph{"s" if totals.triumphs > 1 else ""}! :tada: '
        if totals.despairs != 0:
            end_result += f'\n\t{totals.despairs} Despair{"s" if totals.despairs > 1 else ""}! :skull: '
        await interaction.response.send_message(f'{"**"+comment+":**\n" if comment != "" else ""}Raw results: `{totals}`\n**End result:** \n\t{end_result}')

async def setup(bot):
    await bot.add_cog(Genesys(bot)) 