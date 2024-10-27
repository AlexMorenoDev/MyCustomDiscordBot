import os
import logging
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands
from bots.weather_bot import WeatherBot

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("asyncio").setLevel(logging.DEBUG)


async def main():
    
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='!', intents=intents)

    await bot.add_cog(WeatherBot(bot))
    await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())