import discord
from discord.ext.commands import Bot, when_mentioned_or
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
from lib.db import db


def get_prefix(bot, message):
    prefix = db.field(
        "SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
    return when_mentioned_or(prefix)(bot, message)


intents = discord.Intents(messages=True, guilds=True,
                          reactions=True, members=True, presences=True)

bot = Bot(command_prefix=get_prefix, intents=intents, help_command=None)

TOKEN = 'Nzc3NzM2Mjg2MzQ1NzU2NzQz.X7HxXA.RBsDDLiw3-_W7ft0hK_rl2N3Yhg'

scheduler = AsyncIOScheduler()

for filename in os.listdir("lib/cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"lib.cogs.{filename[:-3]}")


db.autosave(scheduler)


@ bot.event
async def on_ready():
    print("Bot is online")
    print(f"Logged in as: {bot.user.name}")

scheduler.start()
bot.run(TOKEN)
