import discord
from discord.ext import commands
import yt_dlp
import os

TOKEN = os.getenv("TOKEN")
VOICE_CHANNEL_ID = 1399640417535787079  # 👈 apna VC ID yaha paste karo

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="~", intents=intents)

@bot.event
async def on_ready():
    print(f"Music Bot Online: {bot.user}")
    channel = bot.get_channel(VOICE_CHANNEL_ID)

    if channel:
        try:
            await channel.connect()
            print("✅ Joined fixed voice channel")
        except:
            print("⚠️ Already connected or error")

# 🔥 Play command
@bot.command(name="p")
async def play(ctx, *, search):
    vc = ctx.voice_client

    if not vc:
        await ctx.send("❌ Bot VC me nahi hai")
        return

    ydl_opts = {
        "format": "bestaudio",
        "default_search": "ytsearch",
        "quiet": True,
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search, download=False)
        if "entries" in info:
            info = info["entries"][0]

        audio_url = info["url"]
        title = info["title"]

    if vc.is_playing():
        vc.stop()

    source = await discord.FFmpegOpusAudio.from_probe(audio_url)
    vc.play(source)

    await ctx.send(f"🎶 Now Playing: **{title}**")

# ❌ Stop disabled (VC lock)
@bot.command()
@commands.has_permissions(administrator=True)
async def stop(ctx):
    await ctx.send("❌ VC fixed hai, disconnect disabled")

bot.run(TOKEN)