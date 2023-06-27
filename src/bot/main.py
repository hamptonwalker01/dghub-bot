import discord
from datetime import datetime
from os import getenv
from discord.ext import commands
from dotenv import load_dotenv
from data.bot_data import TEST_SERVERS


class MyBot(commands.Bot):
    def __init__(self, command_prefix, intents, testing_servers, cogs):
        super().__init__(command_prefix, intents=intents)
        self._testing_servers = testing_servers
        self._cogs = cogs
        self.global_commands()
        self.load_extensions()

    @property
    def cogs(self):
        return self._cogs

    @cogs.setter
    def cogs(self, cogs):
        self._cogs = cogs

    @property
    def testing_servers(self):
        return self._testing_servers

    @testing_servers.setter
    def testing_servers(self, testing_servers):
        self._testing_servers = testing_servers

    async def on_ready(self):
        print(f"We have logged in as {self.user}")

    def global_commands(self):
        @self.slash_command(name="guide", description="Provides you with a link to DGHub's Dungoneering guide.")
        async def guide(ctx):
            embed = discord.Embed(
                title="DGHub Guide",
                description=f"Want to improve at DG?\nTry reading through the [DGHub guide](http://tinyurl.com/dghubguide)",
                timestamp=datetime.now()
            )
            embed.set_thumbnail(url="https://i.imgur.com/yeHsUDY.png")
            await ctx.respond(embed=embed)
            return

    def load_extensions(self):
        for ext in self.cogs:
            self.load_extension(ext)


def main():
    load_dotenv()
    cogs = ["src.cogs.prices", "src.cogs.about", "src.cogs.help"]
    token = getenv('TOKEN')
    intents = discord.Intents(
        messages=True, guilds=True, presences=True, reactions=True, members=True)
    intents.message_content = True
    bot = MyBot('/',  intents, TEST_SERVERS, cogs)
    bot.run(token)
