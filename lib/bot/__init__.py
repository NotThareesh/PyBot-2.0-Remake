from discord import Intents
from discord.ext.commands import Bot as BotBase
from discord.ext.commands.errors import CommandNotFound
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from glob import glob
from time import sleep

PREFIX = "!"
OWNER_ID = [755362525125672990]
COGS = [path.split("/")[-1][:-3] for path in glob("./lib/cogs/*.py")]


class Ready:
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} Cog Ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.guild = None
        self.cogs_ready = Ready()
        self.scheduler = AsyncIOScheduler()
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_ID, intents=Intents.all(),)

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")

        print("Setup Complete")

    def run(self):
        token = "Nzc3NzM2Mjg2MzQ1NzU2NzQz.X7HxXA.RBsDDLiw3-_W7ft0hK_rl2N3Yhg"
        print("Running bot....")
        self.setup()
        super().run(token, reconnect=True)

    async def warn(self):
        await self.logs_channel.send("Remember to adhere to the rules!")
        await self.logs_channel.send("Remember to adhere to the rules!")

    @staticmethod
    async def on_connect():
        print("Bot Connected")

    async def on_error(self, error, *args, **kwargs):
        if error == "on_command_error":
            await args[0].send("Something went wrong")

        await self.logs_channel.send("An Error Occurred")
        raise Exception

    async def on_command_error(self, context, exception):
        if isinstance(exception, CommandNotFound):
            await context.send("Command Not Found")

        elif hasattr(exception, "original"):
            raise exception.original

        else:
            raise exception

    async def on_ready(self):
        self.stdout = self.get_channel(773582864335372288)
        self.logs_channel = self.get_channel(778465578834853918)
        self.scheduler.add_job(
            self.warn, CronTrigger(week="*", hour="0", minute="0", day_of_week="0", timezone="utc"))

        while not self.cogs_ready.all_ready:
            sleep(0.5)

        print("Bot is Ready")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


bot = Bot()
