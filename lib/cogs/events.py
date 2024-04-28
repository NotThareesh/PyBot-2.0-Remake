from discord.ext.commands import Cog
from discord.ext.commands.errors import CommandNotFound, CommandOnCooldown, MissingPermissions, MissingRequiredArgument, BadArgument, BotMissingPermissions, CommandInvokeError
from discord.errors import Forbidden
from ..db import db


IGNORE_ERRORS = (CommandNotFound, BadArgument)


class Events(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Events Cog Loaded")

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        if any([isinstance(error, exception) for exception in IGNORE_ERRORS]):
            pass

        elif isinstance(error, CommandOnCooldown):
            await ctx.reply(f"Command is on {str(error.cooldown.type).split('.')[-1].capitalize()} cooldown. Please retry after {error.retry_after:,.2f} seconds.", ephemeral=True)

        elif isinstance(error, MissingRequiredArgument):
            await ctx.reply(f"One or more required arguments are missing.", ephemeral=True)

        elif isinstance(error, MissingPermissions):
            await ctx.reply(f"@{ctx.author} doesn't have the required permissions.", ephemeral=True)

        elif isinstance(error, BotMissingPermissions):
            await ctx.reply(f"I don't have the required permissions.", ephemeral=True)

        else:
            await self.bot.get_channel(778465578834853918).send("Something went wrong... Check the logs!")
            print(error)

    @Cog.listener()
    async def on_member_join(self, member):
        channel = db.field(
            "SELECT WelcomeChannel FROM guilds WHERE GuildID = ?", member.guild.id)

        db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)

        if not channel is None:
            await self.bot.get_channel(channel).send(f"{member.mention} has hopped onto the server. Hope you have a great time in {member.guild.name}")

        try:
            await member.send(f"Welcome to **{member.guild.name}**! I hope you have a nice time!")

        except Forbidden:
            pass

    @Cog.listener()
    async def on_member_remove(self, member):
        channel = db.field(
            "SELECT LeaveChannel FROM guilds WHERE GuildID = ?", member.guild.id)

        db.execute("DELETE FROM exp WHERE UserID = ?", member.id)

        if not channel is None:
            await self.bot.get_channel(channel).send(f"{member.mention} has left the server...")

    @Cog.listener()
    async def on_guild_join(self, guild):
        db.execute("INSERT INTO guilds (GuildID) VALUES (?)", guild.id)

        await self.bot.get_channel(778465578834853918).send(f"Bot has joined {guild.name} server.")

    @Cog.listener()
    async def on_guild_remove(self, guild):
        db.execute("DELETE FROM guilds where GuildID=?", guild.id)

        await self.bot.get_channel(778465578834853918).send(f"Bot has left {guild.name} server.")


async def setup(bot):
    await bot.add_cog(Events(bot))
