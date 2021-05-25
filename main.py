import discord, tokens
from discord.ext import commands
from discord_slash import SlashCommand

client = commands.Bot(
                    command_prefix=commands.when_mentioned,
                    status=discord.Status.online,
                    activity=discord.Activity(type=discord.ActivityType.watching, name='cuties be cute!'),
                    case_insensitive=True,
                    allowed_mentions=discord.AllowedMentions.none(),
                    reconnect=True,
                    intents=discord.Intents.default(),
                    max_messages=30
                    )
slash = SlashCommand(client=client, sync_commands=True, override_type=True, sync_on_cog_reload=True, delete_from_unused_guilds=True)

client.load_extension('jishaku')
client.load_extension('utility')

if __name__ == '__main__':
    client.run(tokens.bot)
