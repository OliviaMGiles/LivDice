# LivDice
A discord dice bot made to support Savage Worlds TTRPG and Genesys TTRPG

# Features
- General purpose dice rolling: `/roll`

- Genesys dice pool: `/genesys roll`

- Trait Rolls for Savage World with optional Wild Dice:  `/sw trait`
- Savage Worlds initiative tracking: `/sw initiative`
- Track character statuses and add new statuses: `/sw status`
- Add custom status types: `/sw add_status`
- Track characters in a party, including tracking multiple parties for when the PC's decide to split: `/sw party`
- Party management: `/sw disolve_party`, `/sw kick_partymember`

# Permissions needed
- Read Messages/View Channels
- Send Messages
- Send Messages in Threads
- Use Slash Commands

# Development
This project requires a `.env` file with the following variables:
```
DISCORD_TOKEN=<Found on Bot page for your Application in Discord Developer portal>
APPLICATION_ID=<Found on General Information for your Application in Discord Developer portal>
```