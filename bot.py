import discord
from discord.ext import commands
import yt_dlp
import os

# ================== CONFIG ==================

TOKEN = os.getenv("TOKEN")
VOICE_CHANNEL_ID = 1399640417535787079 
VOICE_CHANNEL_ID = 1452746895691878492
VOICE_CHANNEL_ID = 1377605445253857482
VOICE_CHANNEL_ID = 1398924017242472458# Fixed VC

# 🔐 WHITELISTS (START EMPTY / SAFE)
WHITELIST_ROLE_IDS = []
WHITELIST_USER_IDS = []

OWNER_ID = 819464202728505364  # 🔴 Apna Discord ID yahan daalo

# ============================================

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="~", intents=intents)

# ================== SECURITY CHECK ==================

def is_whitelisted(ctx):
    if ctx.author.id == OWNER_ID:
        return True

    if ctx.author.id in WHITELIST_USER_IDS:
        return True

    for role in ctx.author.roles:
        if role.id in WHITELIST_ROLE_IDS:
            return True

    return False

# ================== BOT READY ==================

@bot.event
async def on_ready():
    print(f"✅ Music Bot Online: {bot.user}")

    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel:
        try:
            await channel.connect()
            print("🔒 Joined fixed voice channel")
        except:
            print("⚠️ Already connected")

# ================== PLAY COMMAND ==================

@bot.command(name="p")
@commands.cooldown(1, 5, commands.BucketType.user)
async def play(ctx, *, search):
    if not is_whitelisted(ctx):
        await ctx.send("⛔ Tum authorized nahi ho.")
        return

    vc = ctx.voice_client
    if not vc:
        await ctx.send("❌ Bot VC me nahi hai")
        return

    ydl_opts = {
        "format": "bestaudio/best",
        "default_search": "ytsearch",
        "quiet": True,
        "noplaylist": True,
        "cookiefile": "cookies.txt",
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
        source = discord.PCMVolumeTransformer(source, volume=1.2)
        vc.play(source)

        await ctx.send(f"🎶 Now Playing: **{title}**")

    except Exception as e:
        await ctx.send("❌ Song play nahi ho paya")
        print(e)

# ================== WHITELIST COMMANDS ==================

@bot.command()
async def wl_add_role(ctx, role: discord.Role):
    if ctx.author.id != OWNER_ID:
        return

    if role.id not in WHITELIST_ROLE_IDS:
        WHITELIST_ROLE_IDS.append(role.id)
        await ctx.send(f"✅ Role whitelisted: **{role.name}**")
    else:
        await ctx.send("⚠️ Role already whitelisted")

@bot.command()
async def wl_remove_role(ctx, role: discord.Role):
    if ctx.author.id != OWNER_ID:
        return

    if role.id in WHITELIST_ROLE_IDS:
        WHITELIST_ROLE_IDS.remove(role.id)
        await ctx.send(f"❌ Role removed: **{role.name}**")
    else:
        await ctx.send("⚠️ Role whitelist me nahi hai")

@bot.command()
async def wl_add_user(ctx, user: discord.Member):
    if ctx.author.id != OWNER_ID:
        return

    if user.id not in WHITELIST_USER_IDS:
        WHITELIST_USER_IDS.append(user.id)
        await ctx.send(f"✅ User whitelisted: **{user}**")
    else:
        await ctx.send("⚠️ User already whitelisted")

@bot.command()
async def wl_remove_user(ctx, user: discord.Member):
    if ctx.author.id != OWNER_ID:
        return

    if user.id in WHITELIST_USER_IDS:
        WHITELIST_USER_IDS.remove(user.id)
        await ctx.send(f"❌ User removed: **{user}**")
    else:
        await ctx.send("⚠️ User whitelist me nahi hai")

@bot.command()
async def wl_list(ctx):
    if ctx.author.id != OWNER_ID:
        return

    roles = [f"<@&{r}>" for r in WHITELIST_ROLE_IDS]
    users = [f"<@{u}>" for u in WHITELIST_USER_IDS]

    await ctx.send(
        f"🔐 **WHITELIST**\n"
        f"**Roles:** {', '.join(roles) if roles else 'None'}\n"
        f"**Users:** {', '.join(users) if users else 'None'}"
    )

# ================== STOP LOCK ==================

@bot.command()
@commands.has_permissions(administrator=True)
async def stop(ctx):
    await ctx.send("🔒 VC fixed hai, disconnect disabled")

# ================== RUN ==================

bot.run(TOKEN)
