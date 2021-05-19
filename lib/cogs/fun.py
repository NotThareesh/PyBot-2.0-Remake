from discord.ext.commands import Cog, command, BucketType, cooldown
from discord import Embed, Colour
from aiohttp import request
import datetime


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        self.bot.cogs_ready.ready_up("fun")

    @command(description="Displays the version of the bot", aliases=["info"])
    @cooldown(1, 5, BucketType.user)
    async def version(self, ctx):
        await ctx.send("I am PyBot 2.0")

    @command(name="ping")
    @cooldown(1, 5, BucketType.user)
    async def ping(self, ctx):
        await ctx.send(f"Pong {round(self.bot.latency, 2)}ms")

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


def setup(bot):
    bot.add_cog(Fun(bot))
