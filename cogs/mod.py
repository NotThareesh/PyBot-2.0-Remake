import discord
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument
from discord.ext.commands import Cog, command, has_role, has_permissions


class Mod(Cog):

    @Cog.listener()
    async def on_ready(self):
        print("Mod Cog Loaded")

    @command(description="Clears messages in a particular channel. Defaults to 10 messages")
    @has_role('Co-ordinators')
    async def clear(self, ctx, amount: int = 10):
        await ctx.send(f"Tidying up your server")
        await ctx.channel.purge(limit=amount+2)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("Please specify the amount of messages to delete.")

    @command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        if reason:
            await ctx.send(f"{member.mention} was kicked for {reason}!")
        else:
            await ctx.send(f"{member.mention} was kicked!")

    @command(description="Bans Members from the server")
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"{member} was **banned**")

    @command(description="Unbans Members from the server")
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{member.mention} was unbanned")

                return


def setup(bot):
    bot.add_cog(Mod(bot))
