import discord
from discord.ext.commands import Bot, when_mentioned_or
from keep_alive import keep_alive
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import os
import json


async def get_prefix(bot, message):
    with open('./prefixes.json', mode="r") as file:
        prefixes = json.load(file)

    prefix = prefixes[str(message.guild.id)]
    return when_mentioned_or(prefix)(bot, message)


intents = discord.Intents(messages=True, guilds=True,
                          reactions=True, members=True, presences=True)

bot = Bot(command_prefix=get_prefix, intents=intents, help_command=None)

TOKEN = 'Nzc3NzM2Mjg2MzQ1NzU2NzQz.X7HxXA.RBsDDLiw3-_W7ft0hK_rl2N3Yhg'

scheduler = AsyncIOScheduler()

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


async def warning():
    channel = bot.get_channel(773582864335372288)
    await channel.send("Remember to adhere to the rules!")

scheduler.add_job(warning, CronTrigger(
    week="*", day_of_week=0, hour=9, minute=0, timezone="UTC"))


@bot.event
async def on_ready():
    print("Bot is online")
    print(f"Logged in as: {bot.user.name}")
    scheduler.start()

keep_alive()
bot.run(TOKEN)
