import discord
from data.bot_data import TEST_SERVERS, COLOURS, EMOJIS
from discord.ext import commands
from datetime import datetime


class About(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # subject to change in the future -> update as needed
        self.admins = ['<@143174781561339904>', '<@472479347299581975>', '<@154622682078380032>', '<@377971066913423360>',  # Feery, Hunter, James, Vex
                       '<@208938795582750721>', '<@143380940490670080>', '<@286257540268949504>', '<@389923609268715541>']  # Gate, QP, Kup, Mage
        self.link = "https://discord.com/invite/FfPxUhN"
        self.logo = "https://cdn.discordapp.com/icons/679134698059989003/a_a220830225d485901d6877854f532970.gif?size=1024"

    @commands.slash_command(guild_ids=TEST_SERVERS, name="about", description="Provides basic information about the DGHub server.")
    async def about(self, ctx):
        dgh: discord.Guild = self.bot.get_guild(
            679134698059989003)  # get dg hub guild
        total = dgh.member_count  # get raw member count
        online = sum([m.raw_status == "offline" for m in dgh.members])
        offline = total - online
        bots = sum([m.bot for m in dgh.members])
        emojis = EMOJIS["about"]
        embed = discord.Embed(
            title=dgh.name,
            description="A bot written for the DGHub Discord server.\nIf you have any feedback, requests, or suggestions, feel free to pm <@522537136361046016> or <@154622682078380032> ",
            colour=COLOURS["default"],
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=self.logo)
        ad, ad2 = f'\n'.join(self.admins[::2]), f'\n'.join(self.admins[1::2])
        embed.add_field(
            name=":mage: Member count:",
            value=(
                f"{total} members\n{emojis['online']} {online}\n"
                f"{emojis['offline']} {offline}\n{emojis['bot']} {bots}\n"
                f"\n**Admins**:\n"
                f"{ad}"
            )
        )
        embed.add_field(
            name=":envelope_with_arrow: Permanent Invite link:",
            value=(f"**[Invite]({self.link})** your friends!\n\n\n\n\n\n"
                   f"{ad2}"),
            inline=True
        )
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(About(bot))
