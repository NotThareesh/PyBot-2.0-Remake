from discord import Embed, Colour
from discord.ext.commands import Cog, command
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands.core import cooldown
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

    if len(params) != 0:
        params = " ".join(params)
    else:
        return f"`{cmd_and_aliases}`"

    return f"`{cmd_and_aliases} {params}`"


class HelpMenu(ListPageSource):
    def __init__(self, ctx, data):
        self.ctx = ctx

        super().__init__(data, per_page=6)

    async def write_page(self, menu, fields=[]):
        offset = (menu.current_page*self.per_page) + 1
        len_data = len(self.entries)

        embed = Embed(title="Help",
                      description="Welcome to the help dialog!",
                      colour=Colour(0x27E4FF))

        embed.set_thumbnail(url=self.ctx.guild.me.avatar_url)
        embed.set_footer(
            text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} commands.")

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        return embed

    async def format_page(self, menu, entries):
        fields = []

        for entry in entries:
            fields.append(
                (entry.description or "No description", syntax(entry)))

        return await self.write_page(menu, fields)


class Help(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Help Cog Loaded")

    async def cog_before_invoke(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            return ctx.command.reset_cooldown(ctx)

    async def cmd_help(self, ctx, command):
        embed = Embed(title=f"Help with `{command}`",
                      description=syntax(command),
                      colour=Colour(0x27E4FF))

        embed.add_field(name="Command description",
                        value=command.description if command.description else command.help)

        await ctx.send(embed=embed)

    @command(name="help", description="Returns a help dialog of all the commands")
    @cooldown(1, 5, BucketType.user)
    async def help(self, ctx, cmd: Optional[str]):
        if cmd is None:
            menu = MenuPages(source=HelpMenu(ctx, list(self.bot.commands)))

            await menu.start(ctx)

        else:
            if (command := get(self.bot.commands, name=cmd)):
                await self.cmd_help(ctx, command)

            else:
                await ctx.send("That command does not exist.")


def setup(bot):
    bot.add_cog(Help(bot))
