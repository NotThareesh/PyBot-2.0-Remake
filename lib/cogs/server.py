from discord import Embed, Status, Game, Activity, ActivityType, Colour
from discord.ext import tasks
from discord.ext.commands import Cog, command, BucketType, cooldown
import random


class Discord(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Server Cog Loaded")
        self.bot_status.start()

    async def cog_before_invoke(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            return ctx.command.reset_cooldown(ctx)

    @tasks.loop(hours=1)
    async def bot_status(self):
        statuses = ["I'm Busy",
                    f"{len(self.bot.guilds)} Servers",
                    "Compiling the code",
                    "Fortnite",
                    "help", ]

        status = random.choice(statuses)

        if status in "I'm Busy":
            await self.bot.change_presence(status=Status.dnd, activity=Game(name=status))

        elif status in ("Fortnite", "Compiling the code"):
            await self.bot.change_presence(activity=Game(name=status))

        elif status in "help":
            await self.bot.change_presence(activity=Activity(type=ActivityType.listening,
                                                             name=status))
        else:
            await self.bot.change_presence(activity=Activity(type=ActivityType.watching,
                                                             name=status))

    @command(description="Sends a server invitation", aliases=['link'])
    @cooldown(1, 5, BucketType.user)
    async def invite(self, ctx):
        link = await ctx.channel.create_invite(max_age=86400)
        await ctx.send(f"Here is an instant invite to this server:\n{link}")

    @command(description="Sends info about the server", aliases=["info"])
    @cooldown(1, 5, BucketType.user)
    async def server(self, ctx):
        embed = Embed(
            title=ctx.guild.name + " Server Information", color=Colour(0x27E4FF))

        embed.add_field(name="Owner", value=ctx.guild.owner.name, inline=False)
        embed.add_field(name="Server ID", value=ctx.guild.id)
        embed.add_field(name="Region", value=str(
            ctx.guild.region).capitalize())
        embed.add_field(name="\u200b", value="\u200b")
        embed.add_field(name="Humans Count", value=len(
            list(filter(lambda user: not user.bot, ctx.guild.members))))
        embed.add_field(name="Bots", value=len(
            list(filter(lambda user: user.bot, ctx.guild.members))))
        embed.add_field(name="\u200b", value="\u200b")
        embed.add_field(name="Text Channels",
                        value=len(ctx.guild.text_channels))
        embed.add_field(name="Voice Channels",
                        value=len(ctx.guild.voice_channels))

        embed.set_thumbnail(url=ctx.guild.icon_url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Discord(bot))
