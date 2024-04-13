import discord
from discord.ext.commands import Cog, command, has_permissions
from typing import Optional
from better_profanity import profanity
from ..db import db


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
        prof = db.field(
            "SELECT Profanity FROM guilds WHERE GuildID = ?", message.guild.id)

        if prof != 0:
            if profanity.contains_profanity(message.content):
                await message.delete()

        if message.content == f"<@{self.bot.user.id}>" and message.mention_everyone is False:
            prefix = db.field(
                "SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)

            await message.channel.send(f"Use **{prefix}help** to invoke the help command.")

    @command(description="Deletes messages in a particular channel")
    @has_permissions(administrator=True, manage_channels=True)
    async def clear(self, ctx, amount: Optional[int]):
        if amount <= 0:
            await ctx.send("Please provide a valid number")
        elif amount > 100:
            await ctx.send("Please provide a smaller number")
        else:
            await ctx.send(f"Tidying up your server")
            await ctx.channel.purge(limit=amount+2)

    @command(description="Kicks members out of the server")
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member):
        await member.kick()

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

    @command(description="Control Profanity Filter")
    @has_permissions(manage_messages=True)
    async def profanity(self, ctx, value: Optional[str]):

        if not value is None:
            if value.lower() in ('1', 'true', 'enable'):
                db.execute(
                    "UPDATE guilds SET Profanity = ? WHERE GuildID = ?", 1, ctx.guild.id)

                await ctx.send("Profanity filter is enabled in this server")
            elif value.lower() in ('0', 'false', 'disable'):
                db.execute(
                    "UPDATE guilds SET Profanity = ? WHERE GuildID = ?", 0, ctx.guild.id)

                await ctx.send("Profanity filter is disabled in this server")
        else:
            if db.execute("SELECT Profanity FROM guilds WHERE GuildID = ?", ctx.guild.id) == 1:
                await ctx.send("Profanity filter is enabled")
            else:
                await ctx.send("Profanity filter is diabled")


async def setup(bot):
    await bot.add_cog(Mod(bot))
