# LivDice
A discord dice bot made to support Savage Worlds TTRPG and Genesys TTRPG

# Features
- General purpose dice rolling: `/roll`

    Comma separated, each term should match the regex `[-+]?<quantity>*d<sides>+!?|[-+]?<constant modifier>`
    | Example | Returns|  |
    |---------|--------|---|
    | 1d4     | ➔ [3] |  Result of a four-sided die roll |
    | 3d6   |  ➔ [7] | Sum of 3 six-sided dice |
    | 1d4, 1d4, 1D4 | ➔ [3, 1, 4]| Commas separate dice pools|
    | 1d6+1d10+1 | ➔ [15] | Can add die sizes together along with modifiers |
    | 1d6! | ➔ [10] | Explodes! Returns the sum |

- Genesys dice pool: `/genesys roll`

- Trait Rolls for Savage World with optional Wild Dice:  `/sw trait`
    - Shows explosions :boom: and counts successes and raises :dart:

- Savage Worlds initiative tracking: `/sw initiative`

- Fate dice roll: `/fate roll`

# Permissions needed
- Read Messages/View Channels
- Send Messages
- Send Messages in Threads
- Use Slash Commands

# Development

## Environment
This project requires a `.env` file with the following variables:
```
DISCORD_TOKEN=<Found on Bot page for your Application in Discord Developer portal>
APPLICATION_ID=<Found on General Information for your Application in Discord Developer portal>
```

## Running the program
```
python main.py
```

## Syncing commands
When to sync: https://gist.github.com/AbstractUmbra/a9c188797ae194e592efe05fa129c57f#file-4-when_to_sync-md

(Only app owners can sync)

To sync commands, use `;sync` to sync to the local guild for development.

When you are done developing use `;sync global` to sync the commands globally, then `;sync clear` to clear the guild context commands so that you don't have duplicate commands on your guild.