import discord
from discord.ext.commands import Bot, when_mentioned_or
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
from lib.db import db
import secret
import asyncio


def get_prefix(bot, message):
    prefix = db.field(
        "SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
    return when_mentioned_or(prefix)(bot, message)


intents = discord.Intents.all()

bot = Bot(command_prefix=get_prefix, intents=intents, help_command=None)

TOKEN = os.getenv('TOKEN')

scheduler = AsyncIOScheduler()


async def load_extension():
    for filename in os.listdir('lib/cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'lib.cogs.{filename[:-3]}')

db.autosave(scheduler)


@bot.event
async def on_ready():
    print("Bot is online")
    print(f"Logged in as: {bot.user.name}")


async def main():
    async with bot:
        await load_extension()
        await bot.start(TOKEN)

scheduler.start()

asyncio.run(main())
