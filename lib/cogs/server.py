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

    @tasks.loop(minutes=5)
    async def bot_status(self):
        statuses = ["I'm Busy",
                    "PYTHON BOT Server",
                    "Compiling the code",
                    "Fortnite",
                    "!"]
        status = random.choice(statuses)
        if status in "I'm Busy":
            await self.bot.change_presence(status=Status.dnd, activity=Game(name=status))

        elif status in ("PYTHON BOT Server", "Not_Thareesh's Stream"):
            await self.bot.change_presence(activity=Activity(type=ActivityType.watching,
                                                             name=status))
        elif status in "!":
            await self.bot.change_presence(activity=Activity(type=ActivityType.listening,
                                                             name=status))
        else:
            await self.bot.change_presence(activity=Game(name=status))

    @command(description="Sends a server invitation", aliases=['link'])
    @cooldown(1, 5, BucketType.user)
    async def invite(self, ctx):
        link = await ctx.channel.create_invite(max_age=86400)
        await ctx.send(f"Here is an instant invite to this server:\n{link}")

    @command(description="Sends info about the server", aliases=["info"])
    @cooldown(1, 5, BucketType.user)
    async def server(self, ctx):
        name = str(ctx.guild.name)
        owner = str(ctx.guild.owner)
        server_id = str(ctx.guild.id)
        region = str(ctx.guild.region).capitalize()
        icon = str(ctx.guild.icon_url)
        member_count = str(ctx.guild.member_count)
        bot_users = 0
        for i in ctx.guild.members:
            if i.bot:
                bot_users += 1
        text_channels = str(len(ctx.guild.text_channels))
        voice_channels = str(len(ctx.guild.voice_channels))

        embed = Embed(
            title=name + " Server Information", color=Colour.red())
        embed.add_field(name="Owner", value=owner, inline=False)
        embed.add_field(name="Server ID", value=server_id)
        embed.add_field(name="Region", value=region, inline=False)
        embed.add_field(name="Member Count", value=member_count)
        embed.add_field(name="Bots", value=str(bot_users))
        embed.add_field(name="Text Channels",
                        value=text_channels, inline=False)
        embed.add_field(name="Voice Channels", value=voice_channels)
        embed.set_thumbnail(url=icon)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Discord(bot))
