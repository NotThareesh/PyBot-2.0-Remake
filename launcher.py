import discord
import os
from discord.ext import commands
intents = discord.Intents(messages=True, guilds=True,
                          reactions=True, members=True, presences=True)
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
TOKEN = 'Nzc3NzM2Mjg2MzQ1NzU2NzQz.X7HxXA.RBsDDLiw3-_W7ft0hK_rl2N3Yhg'


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")


async def connect(ctx):
    await bot.connect(reconnect=True)
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
bot.run(TOKEN)
