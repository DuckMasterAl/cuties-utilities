import discord, aiohttp, io, emoji, math, asyncio
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx: SlashContext, error):
        embed = discord.Embed(title='You broke it <:foxREE:826881122445033549>', description=str(error), color=discord.Color.red())
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        embed = discord.Embed(title='You broke it <:foxREE:826881122445033549>', description=str(error), color=discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command()
    async def emojilist(self, ctx):
        emojis = await self.bot.db.emojis.find().to_list(None)
        emojis = sorted(emojis, key=lambda k: k['uses'], reverse=True)
        msg = []
        num = 0
        total_uses = 0
        for x in emojis:
            num += 1
            total_uses += int(x['uses'])
            if x['id'] in emoji.UNICODE_EMOJI['en']:
                emoji_name = x['id']
            else:
                e = self.bot.get_emoji(int(x['id']))
                if e is None:
                    emoji_name = f'[Unknown](https://cdn.discordapp.com/emojis/{x["id"]}.{"gif" if x["animated"] else "png"})'
                else:
                    emoji_name = str(e)
            msg.append(f"**{num}.** {emoji_name} | {x['uses']} Use{'' if x['uses'] == 1 else 's'}")

        list_page = 0
        page = 1
        page_total = math.ceil(len(msg) / 10)
        embed_description = []
        for a in range(page_total):
            if msg != []:
                embed_description.append('\n'.join(msg[:10]))
                msg = msg[10:]
        embed = discord.Embed(title=f'Emoji Leaderboard ({total_uses} Total)', description=embed_description[0], color=discord.Colour.blue())
        embed.set_footer(text=f'Page {page}/{page_total} • Change Pages via Reactions')
        loading_embed = discord.Embed(title='Loading Menu...', color=discord.Color.dark_yellow())
        m = await ctx.send(embed=loading_embed)
        await m.add_reaction('\U00002b05')# left
        await m.add_reaction('\U000023f9')# stop
        await m.add_reaction('\U000027a1')# right
        await m.edit(embed=embed)
        while True:
            def reaction_check(reaction, user):
                if ctx.author == user and reaction.emoji in ['\U00002b05', '\U000023f9', '\U000027a1'] and reaction.message.id == m.id:
                    return True
                return False
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=90.0, check=reaction_check)
            except asyncio.TimeoutError:
                embed.set_footer(text=f'Page {page}/{page_total} • Menu Timed out')
                embed.color = discord.Color.greyple()
                await m.edit(embed=embed)
                try:
                    await m.clear_reactions()
                except:
                    pass
            else:
                if reaction.emoji == '\U00002b05':# left
                    if list_page - 1 != -1:
                        list_page -= 1
                        page -= 1
                        embed.description = embed_description[list_page]
                        embed.set_footer(text=f'Page {page}/{page_total} • Change Pages via Reactions')
                        await m.edit(embed=embed)
                    try:
                        await m.remove_reaction('\U00002b05', user)
                    except:
                        pass
                elif reaction.emoji == '\U000027a1':# right
                    if list_page + 1 <= page_total - 1:
                        list_page += 1
                        page += 1
                        embed.description = embed_description[list_page]
                        embed.set_footer(text=f'Page {page}/{page_total} • Change Pages via Reactions')
                        await m.edit(embed=embed)
                    try:
                        await m.remove_reaction('\U000027a1', user)
                    except:
                        pass
                elif reaction.emoji == '\U000023f9':# stop
                    embed.set_footer(text=f'Page {page}/{page_total} • Menu Closed')
                    embed.color = discord.Color.greyple()
                    await m.edit(embed=embed)
                    try:
                        await m.clear_reactions()
                    except:
                        pass

    @commands.command()
    @commands.bot_has_permissions(manage_emojis=True)
    @commands.has_permissions(manage_emojis=True)
    async def steal(self, ctx, *, emojis):
        role_list = [ctx.guild.get_role(804036444502753331), ctx.guild.get_role(773123881284272141)]
        emoji_list = {}
        animated = []
        for x in emojis.split(' '):
            emoji_list[x.split(':')[1]] = x.split(':')[2][:-1]
            animated.append('y' if x[1] == 'a' else 'n')
        async with aiohttp.ClientSession() as session:
            for x in emoji_list:
                async with session.get(f'https://cdn.discordapp.com/emojis/{emoji_list[x]}.{"gif" if animated.pop(0) == "y" else "png"}') as r:
                    img = await r.read()
                    emoji = await ctx.guild.create_custom_emoji(name=x, image=img, roles=role_list, reason=f'#DuckLivesMatter | {ctx.author.name}')

    @commands.command()
    @commands.bot_has_permissions(manage_emojis=True)
    @commands.has_permissions(manage_emojis=True)
    async def emote(self, ctx, name, *, role: discord.Role):
        """ Create an emoji with limited role access.
        Make sure to attach the image of the emoji you want to create! """
        if ctx.message.attachments == []:
            return await ctx.reply('You didn\'t attach an image for me to upload!')
        image = await ctx.message.attachments[0].read()
        emoji = await ctx.guild.create_custom_emoji(name=name, image=image, roles=[role], reason=f'{ctx.author.name} told me to do the thing, so I did the thing!')
        await ctx.send(f"Created the emoji ({emoji}) and limited it to users with the {role.mention} role.\n*Note: You may not see the emoji because I don\'t have permission to use it myself!*")

    @cog_ext.cog_slash(
        description='Bean a user!',
        options=[
                {
                    "name": "user",
                    "description": "The user you want to bean.",
                    "type": 6,
                    "required": True
                },
                {
                    "name": "reason",
                    "description": "The reason you're beaning the user.",
                    "type": 3,
                    "required": False
                }
            ]
        )
    @commands.guild_only()
    async def bean(self, ctx, user, reason=None):
        role = ctx.guild.get_role(773123881284272141)# boost
        role2 = ctx.guild.get_role(804036444502753331)# staff
        member = ctx.guild.get_member(ctx.author.id)
        if role2 not in member.roles and role not in member.roles and ctx.author.id != self.bot.owner_id:
            return await ctx.send(f'<:foxban:826881101951402044> You must be a **Server Booster** to be able to hold the bean hammer!')
        if user.id == self.bot.user.id:
            embed = discord.Embed(description=f'I\'ve beaned **{ctx.author.display_name}** for trying to bean me <:catgun:805686505631907890>', color=discord.Color.red())
            embed.set_thumbnail(url='https://duck-is-super-cool.elixi.re/i/s8si.png?raw=true')
            return await ctx.send(embed=embed)
        embed = discord.Embed(description=f'**{user.display_name}** has been beaned by **{ctx.author.display_name}**', color=discord.Color.red())
        embed.set_thumbnail(url='https://duck-is-super-cool.elixi.re/i/zn9z.gif?raw=true')
        if reason is not None:
            embed.description += f'\n**Reason:** {reason}'
        m = await ctx.send(embed=embed)
        await m.add_reaction(self.bot.get_emoji(826881101951402044))# fox ban

    @cog_ext.cog_slash(
        description='Get a role!',
        options=[{
                "name": "role",
                "description": "The role you want.",
                "type": 3,
                "required": True,
                "choices": [
                            {"name": "he/him", "value": "812781933691797535"},
                            {"name": "she/her", "value": "812781931913281567"},
                            {"name": "they/them", "value": "812781931400790016"},
                            {"name": "Ask My Pronoun", "value": "836591936617840641"},
                            {"name": "Any Pronouns", "value": "836592005836439622"},
                            {"name": "gay", "value": "812781930768105533"},
                            {"name": "bisexual", "value": "812781929237708820"},
                            {"name": "straight", "value": "812781927454212106"},
                            {"name": "pansexual", "value": "812781925139087361"},
                            {"name": "asexual", "value": "812781919791611905"},
                            {"name": "transgender", "value": "812782543195602976"},
                            {"name": "Blues", "value": "819633319775567883"},
                            {"name": "Rock", "value": "819632617162145792"},
                            {"name": "Alternative", "value": "819632532379140186"},
                            {"name": "Pop", "value": "819632681662546002"},
                            {"name": "Hip-Hop", "value": "819632736766787604"},
                            {"name": "EDM", "value": "819632815460581456"},
                            {"name": "Lofi", "value": "819632913435197501"}
                    ]
                }
            ]
        )
    async def selfroles(self, ctx, role):
        role = ctx.guild.get_role(int(role))
        member = await ctx.guild.fetch_member(ctx.author.id)
        if role in member.roles:
            await member.remove_roles(role, reason='Selfrole magic')
            await ctx.send(f'Removed the {role.mention} role from you!', hidden=True)
        else:
            await member.add_roles(role, reason='Selfrole magic')
            await ctx.send(f'Added you {role.mention} the role you!', hidden=True)

    @cog_ext.cog_slash(
        description='Visualizes a color!',
        options=[
                {
                    "name": "hex",
                    "description": "The hex code you\'re trying to visualize.",
                    "type": 3,
                    "required": True
                }
            ]
        )
    async def color(self, ctx, hex):
        if hex.startswith('#'):
            hex = hex[1:]
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.thecolorapi.com/id', params={"hex": hex}) as r:
                if r.status == 200:
                    js = await r.json()
                    if (js['hex']['clean'] == '000000' and str(hex).lower() != '000000') or (js['name']['exact_match_name'] is False and js['name']['distance'] is None):
                        return await ctx.send('That\'s not a valid hex code!')
                    embed = discord.Embed(title=f"Information about {js['name']['value'].lower()}", description=f"**HEX:** {js['hex']['value']}\n**RGB:** {js['rgb']['value']}\n**HSV:** {js['hsv']['value']}\n**HSL:** {js['hsl']['value']}\n**CMYK:** {js['cmyk']['value']}\n**XYZ:** {js['XYZ']['value']}\nContrasts with {'black' if js['contrast']['value'] == '#000000' else 'white'}.")
                    try:
                        embed.color = discord.Color(int(f"0x{js['hex']['clean']}", 16))
                    except:# sometimes discord is mean >:(
                        pass
                    embed.set_image(url=f"https://colorhexa.com/{js['hex']['clean']}.png")
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f'Something went wrong when trying to get the data! Status code: {r.status}')

    @commands.command()
    async def privacy(self, ctx):
        """ View the Privacy Policy """
        embed = discord.Embed(title="Privacy Policy", description=f"By using {self.bot.user.name}, you agree to the following Privacy Policy.\nYou understand that this policy may update at any time, and you continue to agree to it even if you\'re not notified about the changes.", color=discord.Color.blue())
        embed.add_field(name='What information is stored?', value='We store all server invite codes and their use count.\nWe also store all emoji ids sent in the chat and their use count.', inline=False)
        embed.add_field(name='Why we store the information and how we use it.', value='We store this information for invite logging and emoji statistics.', inline=False)
        embed.add_field(name='Who gets this data?', value='Only bot developers get access to this data.', inline=False)
        embed.add_field(name='Questions and Concerns.', value='If you are concerned about the data stored, please [email us.](https://quacky.xyz/email?email=duck@bduck.xyz)', inline=False)
        embed.add_field(name='How to Remove your data.', value='If you would like us to remove your data, please [email us.](https://quacky.xyz/email?email=duck@bduck.xyz)', inline=False)
        embed.set_footer(text='Last updated on 05/24/2021')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Utility(bot))
