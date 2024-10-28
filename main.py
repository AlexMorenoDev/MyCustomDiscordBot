import os
import logging
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands
from functionalities.WeatherInfo import WeatherInfo
from functionalities.SeriesProgress import SeriesProgress
from functionalities.MusicPlayer import MusicPlayer

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("asyncio").setLevel(logging.DEBUG)


async def main():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True

    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f'¡{bot.user.name} se ha conectado a Discord!')

    await bot.add_cog(WeatherInfo(bot))
    await bot.add_cog(SeriesProgress(bot, "data/series_progress.txt"))
    await bot.add_cog(MusicPlayer(bot))
    await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())