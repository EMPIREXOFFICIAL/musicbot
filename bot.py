import discord
from discord.ext import commands
import yt_dlp
import os

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="~", intents=intents)

@bot.event
async def on_ready():
    print(f"Music Bot Online: {bot.user}")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
    else:
        await ctx.send("❌ Voice channel join karo")

@bot.command()
async def play(ctx, *, search):
    if not ctx.voice_client:
        await ctx.invoke(join)

    ydl_opts = {
        "format": "bestaudio",
        "quiet": True,
        "default_search": "ytsearch",
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search, download=False)

        # ytsearch result ka first video
        if "entries" in info:
            info = info["entries"][0]

        audio_url = info["url"]
        title = info.get("title", "Unknown")

    source = await discord.FFmpegOpusAudio.from_probe(audio_url)
    ctx.voice_client.play(source)

    await ctx.send(f"🎶 Now Playing: **{title}**")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

bot.run(os.getenv("TOKEN"))