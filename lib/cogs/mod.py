from discord.ext.commands import Cog, command, cooldown, BucketType
from discord.ext import commands


class Mod(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        self.bot.cogs_ready.ready_up("mod")

    @command(name="clear", aliases=["purge"])
    @cooldown(1, 5, BucketType.user)
    @commands.has_role("Co-ordinators")
    async def clear(self, ctx, purge_amount: int = 10):
        await ctx.send("Tidying up your server")
        await ctx.channel.purge(limit=purge_amount + 2)


def setup(bot):
    bot.add_cog(Mod(bot))
