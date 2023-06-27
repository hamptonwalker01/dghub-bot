
import discord
import asyncio
from datetime import datetime
from itertools import zip_longest
from math import ceil
from discord.ext import commands
from data.bot_data import EMOJIS, BUFF_MAP, COLOURS, LINKS
from src.helpers import price_to_str, str_to_int, custom_error, level_to_xp, calculate
from src.resources import FloorSizeMap, FloorStats
from data.bot_data import TEST_SERVERS
from os import getenv
from dotenv import load_dotenv

load_dotenv()
DXPW = getenv("IS_DXPW") == "True"


class PriceChecker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.regular_price = (50_000_000, 2_500_000)
        self.premium_price = (75_000_000, 3_750_000)

    def conditional_join(self, arr):
        if not arr:
            return "None"
        elif len(arr) < 5:
            return ", ".join(arr)
        elif len(arr) < 9:
            return ",\n".join([", ".join(arr[:4]), ", ".join(arr[4:])])
        else:
            return ",\n".join([", ".join(arr[:4]), ", ".join(arr[4:8]), ", ".join(arr[8:])])

    def get_emojis(self, type, account_type):
        cards, iron, prem = [EMOJIS["pc"][k] for k in EMOJIS["pc"]]
        if account_type == "Ironman":
            return cards | iron
        elif type == "Premium":
            return prem | iron
        return cards | (prem | iron)

    def round_to_five(self, num) -> int:
        remainder = num % 5_000
        return num if not remainder else num - remainder + 5_000

    @commands.slash_command(guild_ids=TEST_SERVERS, name="tokens", description="Price Checker for Token Farming services")
    async def tokens(self, ctx, amount: discord.Option(str, description="Amount of tokens to be purchased (e.g. 40k, 250k, 1.5m)")):
        # parsing k/m / verifying correct input
        token_num = str_to_int(amount)
        # send error if invalid input
        if token_num is None:
            await ctx.respond(f"Please enter a valid amount of tokens you would like to buy. For example: `50000`, `100k`, or `1.5m`", ephemeral=True)
            return

        adjusted = self.round_to_five(token_num)
        embed = discord.Embed(
            title="Elite Dungeon Token Farming",
            description=(
                f"*Input `amount` is rounded up to the nearest 5k*\n"
                f"**/pc tokens {price_to_str(adjusted)}**"),
            colour=COLOURS["ed"],
            timestamp=datetime.utcnow()
        )
        adjusted /= 5_000
        embed.set_thumbnail(url=LINKS["Tokens"])
        embed.set_author(name="DGHub", icon_url=LINKS["Logo"])
        embed.add_field(
            name="More info",
            value=("<#689608713933291527>"), inline=False)
        embed.add_field(
            name="__Prices__",
            value=(
                f"**Regular Service** ({price_to_str(self.regular_price[0])} per 100k): {price_to_str(adjusted * self.regular_price[1])} GP Total\n"
                f"**Premium Service** ({price_to_str(self.premium_price[0])} per 100k): {price_to_str(adjusted * self.premium_price[1])} GP Total"
            ),
            inline=False
        )
        await ctx.respond(embed=embed)

    @commands.slash_command(guild_ids=TEST_SERVERS, name="pc", description="Price Checker for Dungeoneering services")
    async def pc(self, ctx: discord.AutocompleteContext,
                 type: discord.Option(str, choices=["Regular", "Premium"], description="Type of floor service, either Regular or Premium"),
                 account_type: discord.Option(str, choices=["Main", "Ironman"], description="Show prices for Mains or Irons"),
                 start: discord.Option(str, description="Your starting level/experience (e.g. 60, 99, 150m)"),
                 goal: discord.Option(str, description="Your desired level/experience (e.g. 75, 120, 200m) or amount of experience gained."),
                 bonus_xp: discord.Option(str, description="(Optional) amount of Bonus XP to be used", required=False)):
        # Parameter Error checking
        if type == "Premium" and account_type == "Ironman":
            await ctx.respond(embed=custom_error("Incompatible Parameters", "Ironmen currently do not have access to Premium Floors.\nWe apologize about the inconvenience."))
            return
        start_xp = level_to_xp(start) or str_to_int(start)
        if start_xp is None or start_xp >= 200_000_000:
            await ctx.respond(embed=custom_error("Invalid Parameter: `start`", "Please input a valid integer (e.g. `50`, `574k`, `120m`)."))
            return
        end_xp = level_to_xp(goal) or str_to_int(goal)
        if not end_xp or end_xp > 200_000_000:
            await ctx.respond(embed=custom_error("Invalid Parameter: `goal`", "Please input a valid integer (e.g. `75`, `120`, `200m`)."))
            return
        # instead of throwing an error, treat "goal" as amount of xp to be gained.
        if start_xp >= end_xp:
            end_xp += start_xp
            end_xp = 200_000_000 if end_xp > 200_000_000 else end_xp
        bonus = 0
        cmd = f"/pc {type} {account_type} {start} - {goal}"

        if bonus_xp:
            bonus = str_to_int(bonus_xp) or 0
            if bonus:
                cmd += f" with {bonus_xp}"
            elif bonus == None:
                await ctx.respond(embed=custom_error("Invalid Parameter: `bonus_xp`", "You did not input a valid number into the `bonus_xp` variable.\nTry a number in the range of `0 - 200,000,000` "))
                return

        emojis = self.get_emojis(type, account_type)
        values = {k: False for k in emojis}
        m = FloorSizeMap()

        subs = type == "Premium"
        is_iron = account_type == "Ironman"
        buffs = []
        warn = f"**{cmd}**\n_Never trade the full amount below to __anyone__.\nLarge floors are paid for individually._"
        buffs_warn = f"_Please wait for a previous buff to be applied\nbefore adding a new one._\n"
        embed = self.build_header(type, warn, subs)
        stats = calculate(m, start_xp, end_xp, bonus,
                          subs, False, False, is_iron, DXPW, buffs)
        embed.add_field(name="XP Gained", value=stats.get_total_xp())
        embed.add_field(name="Tokens Gained", value=stats.get_tokens())
        self.build_subs_response(
            embed, stats) if subs else self.build_regular_response(embed, stats)
        embed.add_field(
            name="Buffs", value=f"{buffs_warn}None" if not subs else "2.5x XP Cards, Double Tokens", inline=False)
        msg = await ctx.respond(embed=embed)
        res = await msg.original_response()
        msg_id, author_id = res.id, ctx.author.id

        # add reaction emojis to message
        async def reactions(msg=msg):
            for k in emojis:
                try:
                    await msg.add_reaction(emojis[k])
                except AttributeError:
                    msg = await ctx.channel.fetch_message(msg_id)
                    await msg.add_reaction(emojis[k])

        await self.bot.loop.create_task(reactions())

        # verify that reaction added was by appropriate user + valid emoji
        def check(payload):
            return (
                payload.message_id == msg_id and
                payload.user_id == author_id
                and str(payload.emoji) in [emojis[k] for k in emojis]
            )

        # stolen from previous bot + slightly refactored
        while True:
            tasks = [
                asyncio.create_task(self.bot.wait_for(
                    "raw_reaction_add", check=check, timeout=60)),
                asyncio.create_task(self.bot.wait_for(
                    "raw_reaction_remove", check=check, timeout=60))
            ]

            done, pending = await asyncio.wait(
                tasks,
                return_when=asyncio.FIRST_COMPLETED
            )
            try:
                msg = await ctx.channel.fetch_message(msg_id)
                payload = done.pop().result()
                for k in emojis:
                    if str(payload.emoji) == emojis[k]:
                        values[k] = "ADD" in payload.event_type

                buffs = [BUFF_MAP[k]["name"] for k in emojis if values[k]]
                dxpw = DXPW or "DXPW" in buffs
                if dxpw:
                    buffs = [buff for buff in buffs if buff not in [
                        "Knowledge Bomb", "Yak Track"]]

                token_cards = xp_cards = False
                if subs:
                    token_cards = xp_cards = True
                    buffs.extend(["2.5x XP Cards", "Double Tokens"])
                else:
                    xp_cards = "2.5x XP Cards" in buffs
                    if xp_cards:
                        token_cards = True
                        if "Double Tokens" not in buffs:
                            buffs.insert(0, "Double Tokens")
                    else:
                        token_cards = "Double Tokens" in buffs

                embed = self.build_header(type, warn, subs)
                stats = calculate(m, start_xp, end_xp, bonus,
                                  subs, token_cards, xp_cards, is_iron, dxpw, buffs)
                embed.add_field(name="XP Gained", value=stats.get_total_xp())
                embed.add_field(name="Tokens Gained", value=stats.get_tokens())
                self.build_subs_response(
                    embed, stats) if subs else self.build_regular_response(embed, stats)
                embed.add_field(
                    name="Buffs", value=(
                        f"{buffs_warn}{self.conditional_join(buffs)}"), inline=False)
                msg = await msg.edit(embed=embed)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                break
            except Exception as e:
                print(f"We caught a {e} exception, should we do something?")
                continue
            finally:
                for completed, future in zip_longest(done, pending):
                    completed is not None and completed.exception()
                    future is not None and future.cancel()

    def get_floors_required(self, stats: FloorStats):
        _s = "\u2007"
        ret = "*These can be done in any order*\n"
        meds, aba, occ, warp, hw = stats.get_num_floors()
        ret += f"{_s}{meds} Mediums\n{_s}{aba + occ + warp + hw} Larges\n {_s}({aba} Ab2, {occ} Occ, {warp} Warp, {hw} HWarp)"
        return ret

    def build_regular_response(self, embed: discord.Embed, stats: FloorStats):
        _s = "\u2007 ➢"
        no_rushes, with_rushes = stats.get_time_and_cost()
        embed.add_field(name="Estimated Prices",
                        value=(f"Buying Rushes:\n"
                               f"{_s} {with_rushes[0]} (~{with_rushes[1]})\n"
                               f"[Skipping](https://i.imgur.com/Pc9g0a5.png) rushes with tokens:\n"
                               f"{_s} {no_rushes[0]} (~{no_rushes[1]})"),
                        inline=False)
        embed.add_field(name="Floors Required",
                        value=self.get_floors_required(stats))

    def build_subs_response(self, embed: discord.Embed, stats: FloorStats):
        _s = "\u2007 ➢"
        prices = stats.get_subs_prices()
        affordable, premium = stats.get_time_and_cost()
        embed.add_field(
            name=f"Afforadble Option ({prices['Affordable'][DXPW]}/hr)",
            value=(f"*This option requires another customer*\n"
                   f"{_s} {affordable[0]} (~{affordable[1]})"),
            inline=False
        )
        embed.add_field(
            name=f"Fastest option ({prices['Premium'][DXPW]}/hr)",
            value=(
                f"*Best xp/hr with minimal wait time*\n"
                f"{_s} {premium[0]} (~{premium[1]})"
            ),
            inline=False
        )

    def build_header(self, type, msg, subs) -> discord.Embed:
        embed = discord.Embed(
            title="Regular Floor Service" if not subs else "Premium XP Service",
            description=msg,
            colour=COLOURS[f"{type}"],
            timestamp=datetime.now(),
        )
        embed.set_thumbnail(url=LINKS[f"{type}"])
        embed.set_author(name="DGHub", icon_url=LINKS["Logo"])
        embed.add_field(
            name="More info", value="<#690796425658761256>" if subs else "<#689256402803490918>", inline=False)
        return embed


def setup(bot):
    bot.add_cog(PriceChecker(bot))
