from discord.ext.commands import Cog
from discord.ext.commands.errors import CommandNotFound, CommandOnCooldown, MissingPermissions
from discord.utils import get
import json


class Events(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Events Cog Loaded")

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            await ctx.send("Command not found.", delete_after=5.0)

        elif isinstance(error, CommandOnCooldown):
            await ctx.send(f"Command is on cool down. Please retry after {round(error.retry_after)} seconds", delete_after=5.0)

        elif isinstance(error, MissingPermissions):
            await ctx.send(f"@{ctx.author} doesn't have the required permissions.", delete_after=5.0)

    @Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(773736558259994624)
        await channel.send(f"Welcome {member.mention}! Hope you have a great time in this server!")

        role = get(member.guild.roles, name="Testers")
        await member.add_roles(role)

    @Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(773736558259994624)
        await channel.send(f"{member.mention} left the server!")

    @Cog.listener()
    async def on_guild_join(self, guild):
        with open("prefixes.json", mode="r") as file:
            prefixes = json.load(file)

        prefixes[str(guild.id)] = "!"

        with open("prefixes.json", mode="w") as file:
            json.dump(prefixes, file, indent=4)

    @Cog.listener()
    async def on_guild_remove(self, guild):
        with open("prefixes.json", mode="r") as file:
            prefixes = json.load(file)

        prefixes.pop(str(guild.id))

        with open("prefixes.json", mode="w") as file:
            json.dump(prefixes, file, indent=4)


def setup(bot):
    bot.add_cog(Events(bot))
