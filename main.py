import discord, tokens
from discord.ext import commands
from discord_slash import SlashCommand
from motor.motor_asyncio import AsyncIOMotorClient

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(
                    command_prefix=commands.when_mentioned,
                    status=discord.Status.online,
                    activity=discord.Activity(type=discord.ActivityType.watching, name='cuties be cute!'),
                    case_insensitive=True,
                    allowed_mentions=discord.AllowedMentions.none(),
                    reconnect=True,
                    intents=intents,
                    max_messages=30
                    )
slash = SlashCommand(client=client, sync_commands=True, override_type=True, sync_on_cog_reload=True, delete_from_unused_guilds=True)

db_client = AsyncIOMotorClient(tokens.mongo)# Mongo
client.db = db_client.bot

cogs = ['jishaku', 'cogs.utility', 'cogs.events', 'cogs.misc']# Load Cogs (yes this is the simple way)
for x in cogs:
    try:
        client.load_extension(x)
    except Exception as e:
        print(f'{x[:-3]} could not be loaded!')
        print(f"{type(e).__name__}: {e}")

if __name__ == '__main__':
    client.run(tokens.bot)
