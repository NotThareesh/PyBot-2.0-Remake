import discord
from discord import Embed, Colour
from discord.ext.commands import Cog, command, BucketType, cooldown
from discord.utils import get
import random
from aiohttp import request
from datetime import datetime
from typing import Optional


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Fun Cog Loaded")

    @command(description="Displays the version of the bot")
    @cooldown(1, 5, BucketType.user)
    async def version(self, ctx):
        await ctx.send("I am PyBot 2.0")

    @command(description="Returns bot latency")
    @cooldown(1, 5, BucketType.user)
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @command(description="Returns Poggies!", aliases=['lachy'])
    @cooldown(1, 5, BucketType.user)
    async def pog(self, ctx):
        await ctx.send("POGGIES!")

    @command(name="8ball", description="Returns a random message from a 8-Ball")
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

    @command(description="Duplicates your message")
    @cooldown(1, 5, BucketType.user)
    async def echo(self, ctx, *, message: Optional[str]):
        await ctx.send(message)

    @command(description="Returns a meme")
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

    @command(description="Returns a joke")
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

    @command(description="Wishes the member 'Happy Birthday'", aliases=["bday", "hbd"])
    @cooldown(1, 5, BucketType.user)
    async def birthday(self, ctx, member: discord.Member):
        await ctx.send(f"Hey {member.mention}, Happy Birthday")

    @command(description="Returns that you slapped 'mentioned member' for 'reason'")
    @cooldown(1, 5, BucketType.user)
    async def slap(self, ctx, member: discord.Member, *, reason: Optional[str]):
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

    @command(description="Posts a gif/png of Pikachu")
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
    async def fn(self, ctx, *, name: str):
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

    @command(description="Posts Covid19 Stats", aliases=["covid19"])
    @cooldown(1, 5, BucketType.user)
    async def covid(self, ctx, country: Optional[str]):

        if country:
            url = f"https://corona.lmao.ninja/v2/countries/{country}?strict=true"

            async with request("GET", url) as response:
                if response.status == 200:
                    data = await response.json()

                    embed = Embed(
                        title=f"{country.capitalize()} Covid-19 Cases", colour=Colour(0x27E4FF), timestamp=datetime.utcfromtimestamp(data['updated']/1000))
                    embed.set_image(
                        url="https://assets.wam.ae/uploads/2020/07/3265571968478696090.jpg")
                    embed.set_thumbnail(url=f"{data['countryInfo']['flag']}")
                    embed.add_field(name="Total Population", value="{:,}".format(
                        data['population']))
                    embed.add_field(
                        name="\u200b", value="\u200b")
                    embed.add_field(
                        name="\u200b", value="\u200b")
                    embed.add_field(
                        name="Today Covid Cases", value="None/Not Updated" if data['todayCases'] == 0 else f"{data['todayCases']:,}")
                    embed.add_field(
                        name="Today Covid Deaths", value="None/Not Updated" if data['todayDeaths'] == 0 else f"{data['todayDeaths']:,}")
                    embed.add_field(
                        name="\u200b", value="\u200b")
                    embed.add_field(name="Total Covid Cases",
                                    value=f"{data['cases']:,}")
                    embed.add_field(name="Total Covid Deaths",
                                    value=f"{data['deaths']:,}")
                    embed.add_field(name="Total Recovered",
                                    value=f"{data['recovered']:,}")
                    embed.set_footer(
                        text="Stay Safe Everybody ✌️")

                    await ctx.send(embed=embed)

                else:
                    await ctx.send(f"API responded with {response.status} status")

        else:
            url = "https://corona.lmao.ninja/v2/all"

            async with request("GET", url) as response:
                if response.status == 200:
                    data = await response.json()

                    embed = Embed(
                        title="Global Covid-19 Cases", colour=Colour(0x27E4FF), timestamp=datetime.utcfromtimestamp(data['updated']/1000))
                    embed.set_image(
                        url="https://assets.wam.ae/uploads/2020/07/3265571968478696090.jpg")

                    embed.add_field(name="Today Covid Cases",
                                    value=f"{data['todayCases']:,}")
                    embed.add_field(name="Today Covid Deaths",
                                    value=f"{data['todayDeaths']:,}")
                    embed.add_field(
                        name="\u200b", value="\u200b")
                    embed.add_field(name="Total Covid Cases",
                                    value=f"{data['cases']:,}")
                    embed.add_field(name="Total Covid Deaths",
                                    value=f"{data['deaths']:,}")
                    embed.add_field(name="Total Recovered",
                                    value=f"{data['recovered']:,}")
                    embed.set_footer(
                        text=f"Stay Safe Everybody ✌️")

                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"API responded with {response.status} status")

    @command(description="Changes Nickname of Member", aliases=["nick"])
    @cooldown(1, 5, BucketType.user)
    async def nickname(self, ctx, member: discord.Member, *, nick: Optional[str]):
        role = get(ctx.guild.roles, name="Co-ordinators")

        if nick:
            if ctx.author.guild_permissions.administrator or role in ctx.author.roles or member == ctx.author:
                await member.edit(nick=nick)
                await ctx.send(f"Nickname has been successfully changed to **{nick}**")

            else:
                await ctx.send(f"You do not have the required permissions")

        else:
            await member.edit(nick=nick)
            await ctx.send("Successfully removed nickname")


def setup(bot):
    bot.add_cog(Fun(bot))
