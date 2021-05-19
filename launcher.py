import discord
from discord.ext.commands import Bot
import os

intents = discord.Intents(messages=True, guilds=True,
                          reactions=True, members=True, presences=True)
bot = Bot(command_prefix="!", intents=intents)

TOKEN = 'Nzc3NzM2Mjg2MzQ1NzU2NzQz.X7HxXA.RBsDDLiw3-_W7ft0hK_rl2N3Yhg'

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
