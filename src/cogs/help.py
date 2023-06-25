import discord
from discord.ext import commands
from data.bot_data import TEST_SERVERS, COLOURS, BUFF_MAP, EMOJIS
# manually building this because walk_commands() only returns help
cmds = ["pc", "tokens", "guide"]


class CustomHelp(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    def default_help(self):
        embed = discord.Embed(
            title="**/help**",
            description="Learn more about the commands offered",
            colour=COLOURS["default"]
        )
        for cmd in cmds:
            test = self.bot.get_application_command(cmd).to_dict()
            title = f"**Command: /{test['name']}**"
            value = f"*{test['description']}*\n\n__Parameters__:"
            value += "\n" if test["options"] else " None\n"
            for option in test["options"]:
                value += f'**{option["name"]}**: {option["description"]}\n'
            embed.add_field(name=title, value=value, inline=False)
        return embed

    @commands.slash_command(guild_ids=TEST_SERVERS,
                            name="help",
                            description="Display list of commands or get more info about a specific command.")
    async def help(self,
                   ctx: discord.AutocompleteContext,
                   command: discord.Option(str, description="Choose a command to learn more about", choices=cmds, default=None)):
        if not command:
            embed = self.default_help()
            await ctx.respond(embed=embed)
        elif command == "guide":
            cmd = self.bot.get_application_command(command).to_dict()
            embed = discord.Embed(
                title=f"**/help {cmd['name']}**",
                description=f"**About /{cmd['name']}**: *{cmd['description']}\n\n...what else do you expect*?",
                colour=COLOURS["default"]
            )
            await ctx.respond(embed=embed)
        elif command == "tokens":
            cmd = self.bot.get_application_command(command).to_dict()
            option = cmd['options'][0]
            embed = discord.Embed(
                title=f"**/help {cmd['name']}**",
                description=f"**About /{cmd['name']}**: *{cmd['description']}.\nDisplays Regular and Premium price for received amount of tokens*.",
                colour=COLOURS["default"]
            )
            embed.add_field(
                name="**Parameters**:",
                value=(
                    f"**{option['name']}**: {option['description']}\n\n"
                    "If the received amount is not divisible by 5,000, then we round up to\n"
                    "the nearest 5,000 as tokens drop 5,000 at a time."
                ),
                inline=False
            )
            await ctx.respond(embed=embed)
        else:
            cmd = self.bot.get_application_command(command).to_dict()
            embed = discord.Embed(
                title=f"**/help {cmd['name']}**",
                description=f"**About /{cmd['name']}**: *{cmd['description']}.\nDisplays Price, XP, and Tokens gained based on\nparameters and user-applied buffs*.",
                colour=COLOURS["default"]
            )
            title = "**__Parameters__**:"
            value = ""
            for option in cmd["options"]:
                value += f'**{option["name"]}**: {option["description"]}\n'
            embed.add_field(name=title, value=value, inline=False)
            embed.add_field(name="Invalid Parameters",
                            value=(f'`type =="Premium" and acccount_type == "Ironman"`\n'
                                   f'`start >= 200m or goal >= 200m`\n\n'
                                   f'**NOTE**: if `goal` > `start`, then `goal` is treated as *amount of\n'
                                   f'xp to be gained*. If `start + goal > 200m`, then `goal = 200m`.'),
                            inline=False)
            cards, iron, prem = [EMOJIS["pc"][k] for k in EMOJIS["pc"]]
            emojis = cards | (iron | prem)
            title = "**Boosts**"
            value = f"*React to the specific emoji to receive said boost\n"
            value += "some are incompatible, such as dxp + bomb or yak*.\n\n"
            for k, v in BUFF_MAP.items():
                emoji = emojis[k]
                value += f"{emoji} {v['name']}: {v['value']}\n"
            embed.add_field(name=title, value=value, inline=False)
            await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(CustomHelp(bot))
