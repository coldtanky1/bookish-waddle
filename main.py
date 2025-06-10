import os
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv

from db import init_db
from functions.construct import Construct
from functions.create import Create
from functions.infrastructure import Infrastructure
from functions.mil import Military
from functions.stats import Stats

intents = discord.Intents.all()
bot = commands.Bot("$", intents=intents)

load_dotenv()

token = os.getenv("DISCORD_TOKEN")

async def on_ready():
    info = await bot.application_info()
    print(f"[+] {info.name} is online.")

async def main():
    init_db()

    await bot.add_cog(Create(bot))
    await bot.add_cog(Construct(bot))
    await bot.add_cog(Stats(bot))
    await bot.add_cog(Military(bot))
    await bot.add_cog(Infrastructure(bot))
    bot.add_listener(on_ready)
    # the line below just complains that "token" is None even though it does get loaded. so i just made pyright ignore it.
    await bot.start(token) # type: ignore

asyncio.run(main())
