#!/usr/bin/env python3
# she be banging on my python

import os
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv

from db import init_db

intents = discord.Intents.all()
bot = commands.Bot("$", intents=intents)

load_dotenv()

token = os.getenv("DISCORD_TOKEN")

async def on_ready():
    info = await bot.application_info()
    print(f"[+] {info.name} is online.")

async def load():
    for file in os.listdir('./functions'):
        if file.endswith('.py'):
            await bot.load_extension(f'functions.{file[:-3]}')

async def main():
    init_db()

    bot.add_listener(on_ready)
    await load()
    # the line below just complains that "token" is None even though it does get loaded. so i just made pyright ignore it.
    await bot.start(token) # type: ignore

asyncio.run(main())
