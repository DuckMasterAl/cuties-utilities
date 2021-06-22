import discord, datetime
from discord.ext import commands, tasks

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logchannel = 846837457189208145
        self.guild_id = 767344022980132884
        self.seriouschat = 848215416702631977
        self.clear_serious_chat.start()

    def cog_unload(self):
        self.clear_serious_chat.cancel()

    @tasks.loop(hours=1)
    async def clear_serious_chat(self):
        channel = self.bot.get_channel(self.seriouschat)
        def is_pinned(m):
            if not m.pinned:
                return True
            return False
        await channel.purge(limit=None, before=(datetime.datetime.now() - datetime.timedelta(days=7)), check=is_pinned)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.db.invites.delete_many({})
        guild = self.bot.get_guild(self.guild_id)
        invites = await guild.invites()
        insert_to_db = []
        for x in invites:
            insert_to_db.append({"code": x.code, "uses": 0})
        await self.bot.db.invites.insert_many(insert_to_db)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot is True or member.guild.id != self.guild_id:
            return
        binvites = await self.bot.db.invites.find().to_list(None)
        ainvites = await member.guild.invites()
        invite = None
        for b in binvites:
            for a in ainvites:
                if b['code'] == a.code and b['uses'] < a.uses:
                    invite = a
                    break
        await self.bot.db.invites.find_one_and_update({"code": invite.code}, {"$inc": {"uses": 1}})
        channel = self.bot.get_channel(self.logchannel)
        if invite is None:
            await channel.send(f'{member} ({member.mention}) joined through a temporary or vanity invite link.')
        else:
            await channel.send(f'{member} ({member.mention}) joined through **{invite.code}** made by {invite.inviter} ({invite.inviter.mention})!')

    @commands.Cog.listener()
    async def on_member_leave(self, member):
        if member.bot is True or member.guild.id != self.guild_id:
            return
        binvites = await self.bot.db.invites.find().to_list(None)
        ainvites = await member.guild.invites()
        invite = None
        for b in binvites:
            for a in ainvites:
                if b['code'] == a.code and b['uses'] > a.uses:
                    invite = a
                    break
        await self.bot.db.invites.find_one_and_update({"code": invite.code}, {"$inc": {"uses": -1}})

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles == after.roles:
            return
        boost_role = after.guild.get_role(773123881284272141)
        if boost_role in before.roles and boost_role not in after.roles:
            color_roles = [855494471592312882, 855494453787361302, 856284563474874379, 856284568931008562, 855494506055729192, 855494521651724330, 847169928707571782, 856284567320002580, 856285250459402261, 856284565580808252, 856285998644461570, 856285997494697994, 856284555232149514]
            for x in [x.id for x in before.roles]:
                if x in color_roles:
                    await after.remove_roles(after.guild.get_role(x), reason='Unboosted the server :(')

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        await self.bot.db.invites.insert_one({"code": invite.code, "uses": 0})
        channel = self.bot.get_channel(self.logchannel)
        await channel.send(f'{invite.inviter} ({invite.inviter.mention}) created a new invite: **{invite.code}**')

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        await self.bot.db.invites.find_one_and_delete({"code": invite.code})
        channel = self.bot.get_channel(self.logchannel)
        await channel.send(f'The invite **{invite.code}** has been removed or has expired.')

def setup(bot):
    bot.add_cog(Events(bot))
