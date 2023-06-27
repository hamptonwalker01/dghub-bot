import discord
import asyncio
from data.bot_data import COLOURS, TEST_SERVERS
from discord.ext import commands
from datetime import datetime 

class Feedback(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.feedback_id = 1123094123746963596

    @commands.slash_command(guild_ids = TEST_SERVERS, name="feedback", description="Give feedback on your experience with our services.")
    async def feedback(self, ctx: discord.AutocompleteContext):
        author = ctx.interaction.user
        feedback_channel = self.bot.get_channel(self.feedback_id)
        ids = []
        service_view = Choose_Service()
        msg = await ctx.respond(
                f"Thank you for taking the time to give us feedback {author.mention}."
                f"Which of our services is your feedback for?",
                view=service_view
            )
        ids.append(msg)
        timeout_check = await service_view.wait()
        if timeout_check:
            await ids[0].edit_original_response(content=f'{author.mention} the command timed out. Please try again',view=None, ephemeral=True)
            return
        
        footer, thumb = None, None
        match service_view.value:
            case "fc":
                footer = "Floor Selling Services"
                thumb = "https://i.imgur.com/Z7U81Rl.png"
            case "ed":
                footer = "Elite Dungeon Services"
                thumb = "https://i.imgur.com/rTM6Ft5.png"
            case "subs":
                footer = "Premium DG XP Services"
                thumb = "https://i.imgur.com/WaEdzy4.png"
            
        colour = COLOURS[service_view.value]
        cancel_flag = False
        while True:
            res = await ctx.send("What would you like to say?")
            ids.append(res)
            
            response = await self.bot.wait_for(
                    "message", check=lambda message: message.author == author, timeout = 120
            )
            
            ids.append(response)
            embed = discord.Embed(
                    description=response.content,
                    colour=colour,
                    timestamp=datetime.now(),
            )
            embed.set_author(
                    name=author.display_name, icon_url=author.avatar.url
            )
            embed.set_footer(text=footer)
            embed.set_thumbnail(url=thumb)
            
            confirm_view = Confirm_Feedback()
            res = await response.reply(
                content="Would you like to edit this message?",
                embed=embed,
                view=confirm_view
            )
            
            ids.append(res)
            await confirm_view.wait()

            match confirm_view.value:
                case "cancel":
                    cancel_flag = True
                    break
                case "edit":
                    continue
                case "complete":
                        await feedback_channel.send(embed=embed)
                        break
                    
        
        for id in ids[1:]:
            await id.delete()
        
        if not cancel_flag:
            await ids[0].edit_original_response(content=f'Thank you for the feedback, {author.mention}!',view=None)
        else:
            await ids[0].delete_original_response()


class Choose_Service(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    def disable(self):
        for item in self.children:
            item.disabled = True
        return self
    

    @discord.ui.button(label="Elite Dungeons", style=discord.ButtonStyle.red, emoji="<:DGH_EliteDungeons:689266008321818718>", custom_id="select_service:ed")
    async def elite_dungeons(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.value = "ed"
        await interaction.response.edit_message(view=self.disable())
        self.stop()

    @discord.ui.button(label="Floor Selling", style=discord.ButtonStyle.blurple, emoji="<:DGH_Floors:689266019919069204>", custom_id="select_service:fc")
    async def friends_chat(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.value = "fc"
        await interaction.response.edit_message(view=self.disable())
        self.stop()

    @discord.ui.button(label="Premium DG XP", style=discord.ButtonStyle.green, emoji="<:DGH_DXPW:698433263617966140>", custom_id="confirm_service:subs")
    async def premium_dg(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.value = "subs"
        await interaction.response.edit_message(view=self.disable())
        self.stop()


class Confirm_Feedback(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None
    
    def disable(self):
        for item in self.children:
            item.disabled = True
        return self
    
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, custom_id="confirm_feedback:cancel")
    async def confirm(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.value = "cancel"
        await interaction.response.edit_message(view=self.disable())
        self.stop()
    
    @discord.ui.button(label="Edit", style=discord.ButtonStyle.grey, custom_id="confirm_feedback:edit")
    async def edit(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.value = "edit"
        await interaction.response.edit_message(view=self.disable())
        self.stop()
    
    @discord.ui.button(label="Finished", style=discord.ButtonStyle.green, custom_id="confirm_feedback:finished")
    async def finish(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.value = "complete"
        await interaction.response.edit_message(view=self.disable())
        self.stop()


def setup(bot):
    bot.add_cog(Feedback(bot))