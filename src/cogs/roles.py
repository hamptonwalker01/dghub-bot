# import discord
from discord.ext import commands

# test command to snipe roles from other guilds and add them to a destination guild


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=[597564088972869633], name="get_roles")
    @commands.is_owner()
    async def get_roles(self, ctx):
        source_guild = self.bot.get_guild(679134698059989003)
        dest_guild = ctx.guild
        print(dest_guild)
        await ctx.send("Yeah I got you")
        if source_guild:
            for role in source_guild.roles:
                r = await dest_guild.create_role(name=role.name, mentionable=role.mentionable, colour=role.colour, hoist=role.hoist)
                print(r)


def setup(bot):
    bot.add_cog(Roles(bot))
