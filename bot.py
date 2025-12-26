import discord
from discord.ext import commands
import yt_dlp
import os

TOKEN = os.getenv("TOKEN")
VOICE_CHANNEL_ID = 1399640417535787079  # ✅ tumhara VC ID

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
            print("⚠️ Already connected")

# 🎶 PLAY COMMAND (~p song name)
@bot.command(name="p")
async def play(ctx, *, search):
    vc = ctx.voice_client

    if not vc:
        await ctx.send("❌ Bot VC me nahi hai")
        return

    # 🔥 BEST yt-dlp OPTIONS (NO ADS + HQ + NO CAPTCHA)
    ydl_opts = {
        "format": "bestaudio/best",
        "default_search": "ytsearch",
        "quiet": True,
        "noplaylist": True,
        "cookiefile": "cookies.txt",   # 👈 MOST IMPORTANT
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "opus",
            "preferredquality": "0"
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search, download=False)

            if "entries" in info:
                info = info["entries"][0]

            audio_url = info["url"]
            title = info.get("title", "Unknown")

        if vc.is_playing():
            vc.stop()

        source = await discord.FFmpegOpusAudio.from_probe(audio_url)
        source = discord.PCMVolumeTransformer(source, volume=1.2)  # 🔊 clear sound

        vc.play(source)

        await ctx.send(f"🎶 Now Playing: **{title}**")

    except Exception as e:
        await ctx.send("❌ Song play nahi ho paya, dusra try karo")
        print(e)

# ❌ STOP DISABLED (VC LOCK)
@bot.command()
@commands.has_permissions(administrator=True)
async def stop(ctx):
    await ctx.send("❌ VC fixed hai, disconnect disabled")

bot.run(TOKEN)