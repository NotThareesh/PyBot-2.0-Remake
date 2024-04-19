from discord.ext.commands import command, Cog, has_permissions
from discord.ext.commands.converter import TextChannelConverter
from discord.ext.commands.errors import ChannelNotFound
from ..db import db


class Setup(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Setup Cog Loaded")

    @command(description="Changes Bot Prefix", aliases=["changeprefix"])
    @has_permissions(manage_guild=True)
    async def chprefix(self, ctx, prefix: str):
        if len(prefix) > 5:
            await ctx.send("The prefix can not be more than 5 characters in length.")

        else:
            db.execute(
                "UPDATE guilds SET Prefix = ? WHERE GuildID = ?", prefix, ctx.guild.id)

            await ctx.send(f"Prefix set to **{prefix}**.")
            await ctx.guild.me.edit(nick=f"[{prefix}] {self.bot.user.name}")

    @command(description="Sets the welcome channel", aliases=["welcome"])
    @has_permissions(manage_guild=True)
    async def welcomeChannel(self, ctx, channelID: TextChannelConverter):
        db.execute(
            "UPDATE guilds SET WelcomeChannel = ? WHERE GuildID = ?", channelID.id, ctx.guild.id)

        await ctx.send(f"Welcome channel is set to {channelID.mention}")

        await self.bot.get_channel(channelID.id).send(
            "I will be sending welcome messages here from now on.", delete_after=10.0)

    @command(description="Sets the good-bye channel", aliases=["leave"])
    @has_permissions(manage_guild=True)
    async def leaveChannel(self, ctx, channelID: TextChannelConverter):
        db.execute(
            "UPDATE guilds SET LeaveChannel = ? WHERE GuildID = ?", channelID.id, ctx.guild.id)

        await ctx.send(f"Leave channel is set to {channelID.mention}")


async def setup(bot):
    await bot.add_cog(Setup(bot))
