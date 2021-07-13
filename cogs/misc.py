import discord, time
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def privacy(self, ctx):
        """ View the Privacy Policy """
        embed = discord.Embed(title="Privacy Policy", description=f"By using {self.bot.user.name}, you agree to the following Privacy Policy.\nYou understand that this policy may update at any time, and you continue to agree to it even if you\'re not notified about the changes.", color=discord.Color.blue())
        embed.add_field(name='What information is stored?', value='We store all server invite codes and their use count.\nWe also store all emoji ids sent in the chat and their use count.', inline=False)
        embed.add_field(name='Why we store the information and how we use it.', value='We store this information for invite logging and emoji statistics.', inline=False)
        embed.add_field(name='Who gets this data?', value='Only bot developers get access to this data.', inline=False)
        embed.add_field(name='Questions and Concerns.', value='If you are concerned about the data stored, please [email us.](https://quacky.xyz/email?email=duck@bduck.xyz)', inline=False)
        embed.add_field(name='How to Remove your data.', value='If you would like us to remove your data, please [email us.](https://quacky.xyz/email?email=duck@bduck.xyz)', inline=False)
        embed.set_footer(text='Last updated on 07/04/2021')
        await ctx.send(embed=embed)

    @commands.command()
    async def source(self, ctx):
        """ View the Source Code o_O """
        await ctx.send("You can view the source code here: https://github.com/DuckMasterAl/cuties-utilities")

    @commands.command()
    async def ping(self, ctx):
        """ Ping...? or pong... """
        start = time.perf_counter()
        message = await ctx.send(f":ping_pong: Pong!\n:heart: Heartbeat • {round(self.bot.latency * 1000)}ms")
        end = time.perf_counter()
        await message.edit(content=f"{message.content}\n:pencil2: Edit • {round((end - start) * 1000)}ms")

    @commands.command(hidden=True)
    @commands.is_owner()
    @commands.guild_only()
    async def recache(self, ctx):
        """ Just a dev command! You can ignore this :p """
        await ctx.trigger_typing()
        await self.bot.db.invites.delete_many({})
        guild = self.bot.get_guild(ctx.guild.id)
        invites = await guild.invites()
        insert_to_db = []
        for x in invites:
            insert_to_db.append({"code": x.code, "uses": 0})
        await self.bot.db.invites.insert_many(insert_to_db)
        await ctx.send("Recached all the invite codes <a:bcaCheerleader:844296747497160736>")

def setup(bot):
    bot.add_cog(Misc(bot))
