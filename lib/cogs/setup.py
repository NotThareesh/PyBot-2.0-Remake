from discord.ext.commands import Cog, has_permissions, hybrid_command
from discord import TextChannel
from ..db import db


class Setup(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Setup Cog Loaded")

    @hybrid_command(description="Changes Bot Prefix", aliases=["changeprefix"])
    @has_permissions(manage_guild=True)
    async def chprefix(self, ctx, prefix: str):
        if len(prefix) > 2:
            await ctx.reply("The prefix can not be more than 2 characters in length.")

        else:
            db.execute(
                "UPDATE guilds SET Prefix = ? WHERE GuildID = ?", prefix, ctx.guild.id)

            await ctx.reply(f"Prefix set to **{prefix}**")
            await ctx.guild.me.edit(nick=f"[{prefix}] {self.bot.user.name}")

    @hybrid_command(description="Sets the welcome channel", aliases=["welcome"])
    @has_permissions(manage_guild=True)
    async def welcomechannel(self, ctx, channelid: TextChannel):
        db.execute(
            "UPDATE guilds SET WelcomeChannel = ? WHERE GuildID = ?", channelid.id, ctx.guild.id)

        await ctx.reply(f"Welcome channel is set to {channelid.mention}")

        await self.bot.get_channel(channelid.id).send(
            "I will be sending welcome messages here from now on.", delete_after=10.0)

    @hybrid_command(description="Sets the good-bye channel", aliases=["leave"])
    @has_permissions(manage_guild=True)
    async def leavechannel(self, ctx, channelid: TextChannel):
        db.execute(
            "UPDATE guilds SET LeaveChannel = ? WHERE GuildID = ?", channelid.id, ctx.guild.id)

        await ctx.reply(f"Leave channel is set to {channelid.mention}")


async def setup(bot):
    await bot.add_cog(Setup(bot))
