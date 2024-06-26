import discord
from discord import Embed, Colour
from discord.ext.commands import Cog, command, BucketType, cooldown, hybrid_command
import random
from aiohttp import request
from typing import Optional


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Fun Cog Loaded")

    async def cog_before_invoke(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            return ctx.command.reset_cooldown(ctx)

    @hybrid_command(description="Displays the version of the bot")
    @cooldown(1, 5, BucketType.user)
    async def version(self, ctx):
        await ctx.reply("I am PyBot 2.0")

    @hybrid_command(description="Returns bot latency")
    @cooldown(1, 5, BucketType.user)
    async def ping(self, ctx):
        await ctx.reply(f"Pong! {round(self.bot.latency * 1000)}ms", ephemeral=True)

    @hybrid_command(description="Returns Poggies!", aliases=['lachy'])
    @cooldown(1, 5, BucketType.user)
    async def pog(self, ctx):
        await ctx.reply("POGGIES!")

    @hybrid_command(name="8ball", description="Returns a random message from a 8-Ball")
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

        await ctx.reply(f"Question: {question}\nAnswer: {random.choice(responses)}")

    @hybrid_command(description="Returns a meme")
    @cooldown(1, 5, BucketType.user)
    async def meme(self, ctx):
        url = "https://meme-api.herokuapp.com/gimme"
        async with request("GET", url) as response:
            if response.status == 200:
                data = await response.json()
                embed = Embed(title=data["title"], colour=Colour(0x27E4FF))
                embed.set_image(url=data["url"])
                await ctx.reply(embed=embed)
            else:
                await ctx.reply(f"API returned a {response.status} status.")

    @hybrid_command(description="Returns a joke")
    @cooldown(1, 5, BucketType.user)
    async def joke(self, ctx):
        url = "https://sv443.net/jokeapi/v2/joke/Miscellaneous,Dark,Pun?blacklistFlags=nsfw,religious,political,racist,sexist&type=twopart"
        async with request("GET", url) as response:
            if response.status == 200:
                data = await response.json()
                embed = Embed(title=data["setup"], colour=Colour(0x27E4FF))
                embed.add_field(name="\u200b", value=data["delivery"])
                await ctx.reply(embed=embed)

            else:
                await ctx.reply(f"API returned a {response.status} status.")

    @hybrid_command(description="Wishes the member 'Happy Birthday'", aliases=["bday", "hbd"])
    @cooldown(1, 5, BucketType.user)
    async def birthday(self, ctx, member: discord.Member):
        await ctx.reply(f"Hey {member.mention}, Happy Birthday")

    @hybrid_command(description="Returns that you slapped another member")
    @cooldown(1, 5, BucketType.user)
    async def slap(self, ctx, member: discord.Member):
        if member.id in [member.id for member in ctx.guild.members if member.bot]:
            await ctx.reply("Hey, you can't slap bots!")

        elif member.id == ctx.message.author.id:
            await ctx.reply("Really? I don't think its a good idea.")

        else:
            await ctx.reply(f"{ctx.author.mention} slapped {member.mention} in the face!")

    @hybrid_command(description="Posts a image of Pikachu")
    @cooldown(1, 5, BucketType.user)
    async def pikachu(self, ctx):
        url = "https://some-random-api.ml/img/pikachu"

        async with request("GET", url) as response:
            if response.status == 200:
                data = await response.json(content_type='text/html')

                if data["link"][-3:] == "jpg":
                    embed = Embed(title="Here's an image of Pikachu",
                                  colour=Colour(0x27E4FF))
                    embed.set_image(url=data["link"])
                    await ctx.reply(embed=embed)

                else:
                    embed = Embed(
                        title=f"Here's a picture of Pikachu", colour=Colour(0x27E4FF))
                    embed.set_image(url=data["link"])
                    await ctx.reply(embed=embed)

            else:
                await ctx.reply(f"API returned a {response.status} status.")

    @hybrid_command(description="Posts a picture of your Fortnite stats")
    @cooldown(1, 5, BucketType.user)
    async def fn(self, ctx, *, name: str):
        url = "https://fortnite-api.com/v1/stats/br/v2"

        async with request("GET", url, params={"name": name, "image": "all"}) as response:
            if response.status == 200:
                data = await response.json()
                await ctx.reply(data["data"]["image"])

            elif response.status == 403:
                await ctx.reply("The given user's account stats is private.")

            elif response.status == 404:
                await ctx.reply("User not found")

            else:
                print(url)
                await ctx.reply(f"API returned {response.status} status.")

    # @hybrid_command(description="Posts Covid19 Stats", aliases=["covid19"])
    # @cooldown(1, 5, BucketType.user)
    # async def covid(self, ctx, country: Optional[str], yesterday: Optional[str]):
    #     if country is not None:
    #         # Per country Covid Stats
    #         if country:
    #             url = f"https://corona.lmao.ninja/v2/countries/{country}?strict=true&yesterday=1" if yesterday else f"https://corona.lmao.ninja/v2/countries/{country}?strict=true"

    #             async with request("GET", url) as response:
    #                 if response.status == 200:
    #                     data = await response.json()

    #                     embed = Embed(
    #                         title=f"{country.title()} Covid-19 Cases", colour=Colour(0x27E4FF), timestamp=datetime.utcfromtimestamp(data['updated']/1000))
    #                     embed.set_thumbnail(
    #                         url=f"{data['countryInfo']['flag']}")
    #                     embed.add_field(name="Total Population", value="{:,}".format(
    #                         data['population']))
    #                     embed.add_field(
    #                         name="\u200b", value="\u200b")
    #                     embed.add_field(
    #                         name="\u200b", value="\u200b")
    #                     embed.add_field(
    #                         name="Today Covid Cases" if not yesterday else "Yesterday Covid Cases", value="None/Not Updated" if data['todayCases'] == 0 else f"{data['todayCases']:,}")
    #                     embed.add_field(
    #                         name="Today Covid Deaths" if not yesterday else "Yesterday Covid Deaths", value="None/Not Updated" if data['todayDeaths'] == 0 else f"{data['todayDeaths']:,}")
    #                     embed.add_field(
    #                         name="\u200b", value="\u200b")
    #                     embed.add_field(name="Total Covid Cases",
    #                                     value=f"{data['cases']:,}")
    #                     embed.add_field(name="Total Covid Deaths",
    #                                     value=f"{data['deaths']:,}")
    #                     embed.add_field(name="Total Recovered",
    #                                     value=f"{data['recovered']:,}")

    #                     user = await self.bot.fetch_user(755362525125672990)

    #                     embed.set_footer(
    #                         text="Stay Safe Everybody ✌️", icon_url=user.avatar_url)

    #                     await ctx.reply(embed=embed)

    #                 else:
    #                     if not response.status == 404:
    #                         await ctx.reply(f"API responded with {response.status} status")
    #                     else:
    #                         await ctx.reply("Country Not Found :)")

    #         # Global Previous Day's Covid Stats
    #         elif country.lower() == "true":
    #             url = "https://corona.lmao.ninja/v2/all?yesterday=true"

    #             async with request("GET", url) as response:
    #                 if response.status == 200:
    #                     data = await response.json()

    #                     embed = Embed(
    #                         title="Global Covid-19 Cases", colour=Colour(0x27E4FF), timestamp=datetime.utcfromtimestamp(data['updated']/1000))
    #                     embed.set_image(
    #                         url="https://assets.wam.ae/uploads/2020/07/3265571968478696090.jpg")

    #                     embed.add_field(name="Yesterday Covid Cases",
    #                                     value=f"{data['todayCases']:,}")
    #                     embed.add_field(name="Yesterday Covid Deaths",
    #                                     value=f"{data['todayDeaths']:,}")
    #                     embed.add_field(
    #                         name="\u200b", value="\u200b")
    #                     embed.add_field(name="Total Covid Cases",
    #                                     value=f"{data['cases']:,}")
    #                     embed.add_field(name="Total Covid Deaths",
    #                                     value=f"{data['deaths']:,}")
    #                     embed.add_field(name="Total Recovered",
    #                                     value=f"{data['recovered']:,}")

    #                     user = await self.bot.fetch_user(755362525125672990)

    #                     embed.set_footer(
    #                         text="Stay Safe Everybody ✌️", icon_url=user.avatar_url)

    #                     await ctx.reply(embed=embed)
    #                 else:
    #                     await ctx.reply(f"API responded with {response.status} status")

    #     # Global Covid Stats
    #     else:
    #         url = "https://corona.lmao.ninja/v2/all?yesterday=true"

    #         async with request("GET", url) as response:
    #             if response.status == 200:
    #                 data = await response.json()

    #                 embed = Embed(
    #                     title="Global Covid-19 Cases", colour=Colour(0x27E4FF), timestamp=datetime.utcfromtimestamp(data['updated']/1000))
    #                 embed.set_image(
    #                     url="https://assets.wam.ae/uploads/2020/07/3265571968478696090.jpg")

    #                 embed.add_field(name="Today Covid Cases",
    #                                 value=f"{data['todayCases']:,}")
    #                 embed.add_field(name="Today Covid Deaths",
    #                                 value=f"{data['todayDeaths']:,}")
    #                 embed.add_field(
    #                     name="\u200b", value="\u200b")
    #                 embed.add_field(name="Total Covid Cases",
    #                                 value=f"{data['cases']:,}")
    #                 embed.add_field(name="Total Covid Deaths",
    #                                 value=f"{data['deaths']:,}")
    #                 embed.add_field(name="Total Recovered",
    #                                 value=f"{data['recovered']:,}")

    #                 user = await self.bot.fetch_user(755362525125672990)

    #                 embed.set_footer(
    #                     text="Stay Safe Everybody ✌️", icon_url=user.avatar_url)

    #                 await ctx.reply(embed=embed)
    #             else:
    #                 await ctx.reply(f"API responded with {response.status} status")

    @hybrid_command(description="Changes Nickname of Member", aliases=["nick"])
    @cooldown(1, 5, BucketType.user)
    async def nickname(self, ctx, member: discord.Member, *, nick: Optional[str]):
        if nick:
            if ctx.author.guild_permissions.manage_guild or member == ctx.author:
                await member.edit(nick=nick)
                await ctx.reply(f"Nickname has been successfully changed to **{nick}**")

            else:
                await ctx.reply(f"You do not have the required permissions", delete_after=5.0)

        else:
            if member.nick is None:
                await ctx.reply(f"Member already doesn't have a nickname.")

            else:
                if ctx.author.guild_permissions.manage_guild or member == ctx.author:
                    await member.edit(nick=nick)
                    await ctx.reply("Successfully removed nickname")


async def setup(bot):
    await bot.add_cog(Fun(bot))
