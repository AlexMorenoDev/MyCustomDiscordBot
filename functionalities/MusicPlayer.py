import yt_dlp
import discord
from discord.ext import commands
from multiprocessing import Process, Queue


class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.FFMPEG_OPTIONS = "-vn -af 'volume=0.2'"
        self.YDL_OPTIONS = {"format": "bestaudio", "noplaylist": True}


    @staticmethod
    def download_audio(search, ydl_options, queue):
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(f"ytsearch:{search}", download=False)
            if "entries" in info:
                info = info["entries"][0]
            url = info["url"]
            title = info["title"]
            queue.put((url, title))


    @commands.command(name="play", help="Reproduce la canción que le digas.")
    async def play(self, ctx, *, search):
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if not voice_channel:
            return await ctx.send("¡No estás en un canal de voz! Para reproducir música entra a un canal de voz primero.")
        if not ctx.voice_client:
            await voice_channel.connect()

        async with ctx.typing():
            queue = Queue()
            process = Process(target=self.download_audio, args=(search, self.YDL_OPTIONS, queue))
            process.start()
            process.join()

            info = queue.get()
            url, title = info[0], info[1]
            self.queue.append((url, title))
            await ctx.send(f"Añadido a la cola de reproducción: **{title}**")

        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)


    async def play_next(self, ctx):
        if self.queue:
            url, title = self.queue.pop(0)
            source = discord.FFmpegPCMAudio(
                url, 
                before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", 
                options=self.FFMPEG_OPTIONS
            )
            ctx.voice_client.play(source, after=lambda _:self.bot.loop.create_task(self.play_next(ctx)))
            await ctx.send(f"Se está reproduciendo: **{title}**")
        elif not ctx.voice_client.is_playing():
            await ctx.send("La cola de reproducción está vacía.")


    @commands.command(name="skip", help="Omite la canción que esté reproduciéndose.")
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Canción omitida.")
            