from discord import Embed, Colour
from discord.ext.commands import Cog, command
from discord.utils import get
from discord.ext.menus import MenuPages, ListPageSource
from typing import Optional


def syntax(command):
    cmd_and_aliases = " | ".join([str(command), *command.aliases])
    params = []

    for key, value in command.params.items():
        if key not in ("self", "ctx"):
            params.append(f"[{key}]" if "Optional" in str(
                value) else f"<{key}>")

    params = " ".join(params)

    return f"`{cmd_and_aliases} {params}`"


class Help(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Help Cog Loaded")

    async def cmd_help(self, ctx, command):
        embed = Embed(title=f"Help with `{command}`",
                      description=syntax(command),
                      colour=Colour(0x27E4FF))

        embed.add_field(name="Command description",
                        value=command.description if command.description else command.help)

        await ctx.send(embed=embed)

    @command(name="help", description="Returns a help dialog of all the commands")
    async def help(self, ctx, cmd: Optional[str]):
        if cmd is None:
            pass

        else:
            if (command := get(self.bot.commands, name=cmd)):
                await self.cmd_help(ctx, command)

            else:
                await ctx.send("That command does not exist.")


def setup(bot):
    bot.add_cog(Help(bot))
