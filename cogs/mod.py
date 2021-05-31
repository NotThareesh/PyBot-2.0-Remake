import discord
from discord.ext.commands.errors import MissingRequiredArgument
from discord.ext.commands import Cog, command, has_permissions
from typing import Optional
from better_profanity import profanity
import json


class Mod(Cog):
    def __init__(self, bot):
        self.bot = bot

        with open("./words/whitelisted_words.txt", "r") as white_words_file:
            white_words_list = []
            for x in white_words_file.readlines():
                white_words_list.append(x.strip("\n"))

        profanity.load_censor_words(whitelist_words=white_words_list)

    @Cog.listener()
    async def on_ready(self):
        print("Mod Cog Loaded")

    async def cog_before_invoke(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            return ctx.command.reset_cooldown(ctx)

    @Cog.listener()
    async def on_message(self, message):
        if profanity.contains_profanity(message.content):
            await message.delete()
        if message.content == f"<@!{self.bot.user.id}>":
            with open("prefixes.json", mode="r") as file:
                prefixes = json.load(file)

            await message.channel.send(f"Use **{prefixes[str(message.guild.id)]}help** to invoke the help command.")

    @command(description="Clears messages in a particular channel. Defaults to 10 messages")
    @has_permissions(administrator=True, manage_channels=True)
    async def clear(self, ctx, amount: int = 10):
        if amount <= 0:
            await ctx.send("Please provide a valid number")
        elif amount > 100:
            await ctx.send("Please provide a smaller number")
        else:
            await ctx.send(f"Tidying up your server")
            await ctx.channel.purge(limit=amount+2)

    @command(description="Kicks members out of the server")
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=Optional[str]):
        await member.kick(reason=reason)
        if reason:
            await ctx.send(f"{member.mention} was kicked for {reason}!")
        else:
            await ctx.send(f"{member.mention} was kicked!")

    @command(description="Bans Members from the server")
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=Optional[str]):
        await member.ban(reason=reason)
        await ctx.send(f"{member} was **banned**")

    @command(description="Unbans Members from the server")
    @has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{member.mention} was unbanned")

                return

    @command(description="Changes Bot Prefix", aliases=["changeprefix"])
    @has_permissions(manage_guild=True)
    async def chprefix(self, ctx, prefix: str = "!"):
        if len(prefix) > 5:
            await ctx.send("Prefix cannot be more than 5 characters.")

        else:
            with open("prefixes.json", mode="r") as file:
                prefixes = json.load(file)

            prefixes[str(ctx.guild.id)] = prefix

            with open("prefixes.json", mode="w") as file:
                json.dump(prefixes, file, indent=4)

            await ctx.send(f"Prefix changed to **{prefix}**")

            await ctx.guild.me.edit(nick=f"[{prefix}] {self.bot.user.name}")


def setup(bot):
    bot.add_cog(Mod(bot))
