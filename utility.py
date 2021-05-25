import discord, aiohttp
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        embed = discord.Embed(title="Privacy Policy", description=f"By using {self.bot.user.name}, you agree to the following Privacy Policy.", color=discord.Color.blue())
        embed.add_field(name='What information is stored?', value='Currently, no information is stored.', inline=False)
        embed.add_field(name='Questions and Concerns.', value='If you are concerned about the data stored, please [email us.](https://quacky.xyz/email?email=duck@bduck.xyz)', inline=False)
        embed.set_footer(text='Last updated on 05/24/2021')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Utility(bot))
