import discord
from discord.ext.commands import Cog, hybrid_command, has_permissions
from typing import Optional
from better_profanity import profanity
from ..db import db


class Mod(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = {}

        with open("whitelisted_words.txt", "r") as white_words_file:
            white_words_list = []
            for x in white_words_file.readlines():
                white_words_list.append(x.strip("\n"))

        profanity.load_censor_words(whitelist_words=white_words_list)

        query = db.execute("SELECT GuildID, Prefix, Profanity FROM guilds")
        result = db.cur.fetchall()

        for id, prefix, prof in result:
            self.data[id] = [prefix, prof]

    @Cog.listener()
    async def on_ready(self):
        print("Mod Cog Loaded")

    async def cog_before_invoke(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            return ctx.command.reset_cooldown(ctx)

    @Cog.listener()
    async def on_message(self, message):
        prof = self.data[message.guild.id][1]

        if prof == 1:
            if profanity.contains_profanity(message.content):
                await message.delete()

        if message.content == f"<@{self.bot.user.id}>" and message.mention_everyone is False:
            prefix = db.field(
                "SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)

            await message.channel.send(f"Use **{prefix}help** to invoke the help command")

    @hybrid_command(description="Deletes messages in a particular channel")
    @has_permissions(administrator=True, manage_channels=True)
    async def clear(self, ctx, amount: Optional[int]):
        if amount <= 0:
            await ctx.reply("Please provide a valid number")
        elif amount > 50:
            await ctx.reply("Please provide a smaller number")
        else:
            await ctx.reply(f"Tidying up your server")
            await ctx.channel.purge(limit=amount+2, bulk=True)

    @hybrid_command(description="Kicks members out of the server")
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member):
        await member.kick()
        await ctx.reply(f"{member.mention} was kicked!")

    @hybrid_command(description="Bans Members from the server")
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: Optional[str]):
        await ctx.guild.ban(user=member, reason=reason)
        await ctx.reply(f"{member} was **banned**")

    @hybrid_command(description="Unbans Members from the server")
    @has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.reply(f"{member.mention} was unbanned")

                return

    @hybrid_command(description="Control Profanity Filter")
    @has_permissions(manage_messages=True)
    async def profanity(self, ctx, value: Optional[str]):
        if not value is None:
            if value.lower() in ('1', 'true', 'enable'):
                db.execute(
                    "UPDATE guilds SET Profanity = ? WHERE GuildID = ?", 1, ctx.guild.id)

                self.data[ctx.guild.id][1] = 1

                await ctx.reply("Profanity filter is enabled in this server")
            elif value.lower() in ('0', 'false', 'disable'):
                db.execute(
                    "UPDATE guilds SET Profanity = ? WHERE GuildID = ?", 0, ctx.guild.id)

                self.data[ctx.guild.id][1] = 0

                await ctx.reply("Profanity filter is disabled in this server")
        else:
            if db.execute("SELECT Profanity FROM guilds WHERE GuildID = ?", ctx.guild.id) == 1:
                await ctx.reply("Profanity filter is enabled")
            else:
                await ctx.reply("Profanity filter is disabled")


async def setup(bot):
    await bot.add_cog(Mod(bot))
