import discord
from discord import Embed, Colour, Status, Game, Activity, ActivityType
from discord.ext import tasks
from discord.ext.commands import Cog, command, BucketType, cooldown
from discord.ext.commands.errors import CommandNotFound, CommandOnCooldown
import random
from aiohttp import request
import datetime


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        self.bot_status.start()
        print("Bot is online")
        print(f"Logged in as: {self.bot.user}")

    @tasks.loop(seconds=60)
    async def bot_status(self):
        statuses = ["I'm Busy",
                    "PYTHON BOT Server",
                    "Compiling the code",
                    "Fortnite",
                    "!"]
        status = random.choice(statuses)
        if status in "I'm Busy":
            await self.bot.change_presence(status=Status.dnd, activity=discord.Game(name=status))

        elif status in ("PYTHON BOT Server", "Not_Thareesh's Stream"):
            await self.bot.change_presence(activity=Activity(type=ActivityType.watching,
                                                             name=status))

        elif status in "!":
            await self.bot.change_presence(activity=Activity(type=ActivityType.listening,
                                                             name=status))

        else:
            await self.bot.change_presence(activity=Game(name=status))

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            await ctx.send("Command not found.")

        elif isinstance(error, CommandOnCooldown):
            await ctx.send(f"Command is on cool down. Please retry after {round(error.retry_after)} seconds")

    @Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(773736558259994624)
        await channel.send(f"Welcome {member.mention}! Hope you have a great time in this server!")
        role = discord.utils.get(member.guild.roles, name="Testers")
        await member.add_roles(role)

    @Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(773736558259994624)
        await channel.send(f"{member.mention} left the server!")

    @command(description="Displays the version of the bot")
    @cooldown(1, 5, BucketType.user)
    async def version(self, ctx):
        await ctx.send("I am PyBot 2.0")

    @command()
    @cooldown(1, 5, BucketType.user)
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @command(aliases=['lachy'])
    @cooldown(1, 5, BucketType.user)
    async def pog(self, ctx):
        await ctx.send("POGGIES!")

    @command(aliases=['8ball'])
    @cooldown(1, 5, BucketType.user)
    async def _8ball(self, ctx, *, question):
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]

        await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

    @command(aliases=['link'])
    @cooldown(1, 5, BucketType.user)
    async def invite(self, ctx):
        link = await ctx.channel.create_invite(max_age=300)
        await ctx.send(f"Here is an instant invite to this server:\n{link}")

    @command(description="Duplicates your message")
    @cooldown(1, 5, BucketType.user)
    async def echo(self, ctx, *, message):
        await ctx.send(message)

    @command(description="Sends a meme")
    @cooldown(1, 5, BucketType.user)
    async def meme(self, ctx):
        url = "https://meme-api.herokuapp.com/gimme"
        async with request("GET", url) as response:
            if response.status == 200:
                data = await response.json()
                embed = Embed(title=data["title"], colour=Colour(0x27E4FF))
                embed.set_image(url=data["url"])
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"API returned a {response.status} status.")

    @command(description="Sends a joke")
    @cooldown(1, 5, BucketType.user)
    async def joke(self, ctx):
        url = "https://sv443.net/jokeapi/v2/joke/Miscellaneous,Dark,Pun?blacklistFlags=nsfw,religious,political,racist,sexist&type=twopart"
        async with request("GET", url) as response:
            if response.status == 200:
                data = await response.json()
                embed = Embed(title=data["setup"], colour=Colour(0x27E4FF))
                embed.add_field(name="\u200b", value=data["delivery"])
                await ctx.send(embed=embed)

            else:
                await ctx.send(f"API returned a {response.status} status.")

    @command(description="Wishes the member 'Happy Birthday'")
    @cooldown(1, 5, BucketType.user)
    async def bday(self, ctx, member: discord.Member):
        await ctx.send(f"Hey {member.mention}, Happy Birthday")

    @command(description="Sends 'member1' slapped 'member2' for 'reason'. (Reason isn't compulsory)")
    @cooldown(1, 5, BucketType.user)
    async def slap(self, ctx, member: discord.Member, *, reason=None):
        bot_users_id = []

        for bot_users in ctx.guild.members:
            if bot_users.bot:
                bot_users_id.append(bot_users.id)

        if member.id in bot_users_id:
            await ctx.send("Hey, you can't slap bots!")

        elif reason is None:
            await ctx.send(f"{ctx.author.display_name} slapped {member.mention}")

        elif member.id == ctx.message.author.id:
            await ctx.send("Really? I don't think its a good idea.")

        else:
            await ctx.send(f"{ctx.author.display_name} slapped {member.mention} for {reason}!")

    @command(description="Sends a gif/png of Pikachu")
    @cooldown(1, 5, BucketType.user)
    async def pikachu(self, ctx):
        url = "https://some-random-api.ml/img/pikachu"

        async with request("GET", url) as response:
            if response.status == 200:
                data = await response.json()

                if data["link"][-3:] == "gif":
                    embed = Embed(title="Here's a gif of Pikachu",
                                  colour=Colour(0x27E4FF))
                    embed.set_image(url=data["link"])
                    await ctx.send(embed=embed)

                else:
                    embed = Embed(
                        title=f"Here's a picture of Pikachu", colour=Colour(0x27E4FF))
                    embed.set_image(url=data["link"])
                    await ctx.send(embed=embed)

            else:
                await ctx.send(f"API returned a {response.status} status.")

    @command(description="Posts a picture of your Fortnite stats")
    @cooldown(1, 5, BucketType.user)
    async def fn(self, ctx, *, name):
        url = "https://fortnite-api.com/v1/stats/br/v2"

        async with request("GET", url, params={"name": name, "image": "all"}) as response:
            if response.status == 200:
                data = await response.json()
                await ctx.send(data["data"]["image"])

            elif response.status == 403:
                await ctx.send("The given user's account stats is private.")

            elif response.status == 404:
                await ctx.send("User not found")

            else:
                print(url)
                await ctx.send(f"API returned {response.status} status.")

    @command(name="server_info", aliases=["info", "server"])
    @cooldown(1, 5, BucketType.user)
    async def server_info(self, ctx):
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

        embed = discord.Embed(
            title=name + " Server Information", color=discord.Color.red())

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

    @command(name="covid", aliases=["covid19"])
    @cooldown(1, 5, BucketType.user)
    async def covid(self, ctx, country=None):

        if country:
            url = f"https://corona.lmao.ninja/v2/countries/{country}?yesterday&strict&query"

            async with request("GET", url) as response:
                if response.status == 200:
                    data = await response.json()

                    embed = Embed(
                        title=f"{country} Covid-19 Cases", colour=Colour(0x27E4FF), timestamp=datetime.datetime.utcnow())
                    embed.set_image(
                        url="https://assets.wam.ae/uploads/2020/07/3265571968478696090.jpg")

                    embed.add_field(name="Total Population", value="{:,}".format(
                        data['population']))
                    embed.add_field(name="Today Covid Cases",
                                    value="{:,}".format(data['todayCases']))
                    embed.add_field(name="Today Covid Deaths",
                                    value="{:,}".format(data['todayDeaths']))
                    embed.add_field(name="Total Covid Cases",
                                    value="{:,}".format(data['cases']))
                    embed.add_field(name="Total Covid Deaths",
                                    value="{:,}".format(data['deaths']))
                    embed.set_footer(text="Stay Safe Everybody ✌️")

                    await ctx.send(embed=embed)

                else:
                    await ctx.send(f"API responded with {response.status} status")

        else:
            url = "https://corona.lmao.ninja/v2/all?yesterday"

            async with request("GET", url) as response:
                if response.status == 200:
                    data = await response.json()

                    embed = Embed(
                        title="Global Covid-19 Cases", colour=Colour(0x27E4FF), timestamp=datetime.datetime.utcnow())
                    embed.set_image(
                        url="https://assets.wam.ae/uploads/2020/07/3265571968478696090.jpg")

                    embed.add_field(name="Today Covid Cases",
                                    value="{:,}".format(data['todayCases']))
                    embed.add_field(name="Today Covid Deaths",
                                    value="{:,}".format(data['todayDeaths']))
                    embed.add_field(
                        name="\u200b", value="\u200b")
                    embed.add_field(name="Total Covid Cases",
                                    value="{:,}".format(data['cases']))
                    embed.add_field(name="Total Covid Deaths",
                                    value="{:,}".format(data['deaths']))
                    embed.add_field(name="Total Active Cases",
                                    value="{:,}".format(data['active']))
                    embed.add_field(name="Total Recovered",
                                    value="{:,}".format(data['recovered']))
                    embed.set_footer(text="Stay Safe Everybody ✌️")

                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"API responded with {response.status} status")


def setup(bot):
    bot.add_cog(Fun(bot))
