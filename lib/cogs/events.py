from discord.ext.commands import Cog
from discord.ext.commands.errors import CommandNotFound, CommandOnCooldown, MissingPermissions, MissingRequiredArgument, BadArgument
from discord.errors import Forbidden
import traceback
import sys
from ..db import db


class Events(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Events Cog Loaded")

    @Cog.listener()
    async def on_error(self, error, *args, **kwargs):
        if error == "on_command_error":
            await args[0].send("Something went wrong.")

        channel = await self.bot.get_channel(778465578834853918)
        await channel.send("An Error Occured.")

        raise error

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            pass

        elif isinstance(error, BadArgument):
            pass

        elif isinstance(error, Forbidden):
            pass

        elif isinstance(error, CommandOnCooldown):
            await ctx.send(f"Command is on {str(error.cooldown.type).split('.')[-1]} cooldown. Please retry after {error.retry_after:,.2f} seconds.", delete_after=5.0)

        elif isinstance(error, MissingRequiredArgument):
            await ctx.send(f"One or more required arguments are missing.")

        elif isinstance(error, MissingPermissions):
            await ctx.send(f"@{ctx.author} doesn't have the required permissions.", delete_after=5.0)

        else:
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr)

    @Cog.listener()
    async def on_member_join(self, member):
        db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)
        try:
            await member.send(f"Welcome to **{member.guild.name}**! I hope you have a nice time!")
        except Forbidden:
            pass

    @Cog.listener()
    async def on_member_remove(self, member):
        db.execute("DELETE FROM exp WHERE UserID = ?", member.id)
        await self.bot.get_channel(773736558259994624).send(f"{member.mention} has left the server...")

    @Cog.listener()
    async def on_guild_join(self, guild):
        db.execute("INSERT INTO guilds (GuildID) VALUES (?)", guild.id)

    @Cog.listener()
    async def on_guild_remove(self, guild):
        db.execute("DELETE FROM guilds where GuildID=?", guild.id)


def setup(bot):
    bot.add_cog(Events(bot))
