import discord
from discord.ext import commands, tasks
import random
import os
import asyncio
import requests
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================
WEBHOOK_URL = "https://discord.com/api/webhooks/1503105638581014658/PLv94o-ZNO0S2PW86-M5um5wQpRg6VMtYjhxFMizrVIAnXaUOB6UByJZBsbIUosyM0E2"

# Game IDs that Lazy AJ works on
ALLOWED_GAME_IDS = [109983668079237, 85621847059032, 99606176102979]

# Brainrot list (matches the fake ones in the script)
BRAINROTS = {
    "Strawberry Elephant": {"base": 750, "interval": 7200, "last": 0},
    "Meowl": {"base": 650, "interval": 5400, "last": 0},
    "Skibidi Toilet": {"base": 450, "interval": 2700, "last": 0},
    "Headless Horseman": {"base": 550, "interval": 14400, "last": 0},
    "Dragon Cannelloni": {"base": 250, "interval": 900, "last": 0},
    "Frograma & Chocrama": {"base": 100, "interval": 3600, "last": 0},
    "Capitano Moby": {"base": 165, "interval": 4200, "last": 0},
    "Hydra Bunny": {"base": 185, "interval": 4800, "last": 0},
    "Ketchuru & Masturu": {"base": 200, "interval": 5400, "last": 0},
    "Garama and Madundung": {"base": 220, "interval": 6000, "last": 0},
    "Los Chicleteiras": {"base": 150, "interval": 3000, "last": 0},
    "Noo My Eggs": {"base": 120, "interval": 2400, "last": 0}
}

MUTATIONS = ["Cyber", "Divine", "Rainbow", "Cursed", "Radioactive", "Yin Yang", "Galaxy", "Lava", "Candy", "Diamond", "Gold", "Normal"]
TRAITS = ["Strawberry", "Meowl", "Skibidi", "Nyan Cat", "Firework", "Brazil", "Lightning", "Chicleteira", "Tie", "Spider", "Asteroid", "Galactic", "Crab Rave", "Bubblegum", "Extinct"]

# ============================================================
# BOT SETUP
# ============================================================
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def calculate_price(base_value, mutation, trait):
    mults = {
        "Cyber": 11, "Divine": 10, "Rainbow": 10, "Cursed": 9,
        "Radioactive": 8.5, "Yin Yang": 7.5, "Galaxy": 7, "Lava": 6,
        "Candy": 4, "Diamond": 1.5, "Gold": 1.25, "Normal": 1
    }
    trait_mults = {
        "Strawberry": 8, "Meowl": 7, "Skibidi": 6.5, "Nyan Cat": 6,
        "Firework": 6, "Brazil": 6, "Lightning": 6, "Chicleteira": 6,
        "Tie": 4.75, "Spider": 4.5, "Asteroid": 4, "Galactic": 4,
        "Crab Rave": 4, "Bubblegum": 4, "Extinct": 4
    }
    
    mutation_mult = mults.get(mutation, 1)
    trait_mult = trait_mults.get(trait, 1)
    variance = 0.8 + (random.random() * 0.4)
    final_value = base_value * mutation_mult * trait_mult * variance
    final_value = max(base_value, min(15000, final_value))
    return final_value

def format_price(millions):
    if millions >= 1000:
        return f"${millions/1000:.2f}B"
    return f"${millions:.0f}M"

def send_to_webhook(embed):
    """Send embed to the webhook"""
    try:
        requests.post(WEBHOOK_URL, json={"embeds": [embed.to_dict()]})
    except Exception as e:
        print(f"Webhook error: {e}")

# ============================================================
# EMBED GENERATORS
# ============================================================
async def send_detection_embed(name, price, mutation, trait, players, maxpl, job_id):
    if price >= 10000:
        color = 0xFF0000  # Red
    elif price >= 5000:
        color = 0xFF6600  # Orange
    elif price >= 2000:
        color = 0xFFFF00  # Yellow
    else:
        color = 0x00FF00  # Green
    
    embed = discord.Embed(
        title="🎯 NEW BRAINROT DETECTED",
        description=f"**{name}** has been detected!",
        color=color,
        timestamp=datetime.now()
    )
    
    embed.add_field(name="💰 Estimated Value", value=format_price(price), inline=True)
    embed.add_field(name="🧬 Mutation", value=mutation, inline=True)
    if trait:
        embed.add_field(name="✨ Trait", value=trait, inline=True)
    embed.add_field(name="👥 Players", value=f"{players}/{maxpl}", inline=True)
    if job_id:
        embed.add_field(name="🔗 Job ID", value=f"`{job_id[:12]}...`", inline=False)
    
    embed.set_footer(text="Lazy AJ • Made by tigy")
    
    send_to_webhook(embed)

async def send_join_embed(name, job_id):
    embed = discord.Embed(
        title="✅ JOIN ATTEMPT",
        description=f"Someone joined **{name}**",
        color=0x00FF00,
        timestamp=datetime.now()
    )
    embed.add_field(name="🔗 Job ID", value=f"`{job_id}`", inline=False)
    embed.set_footer(text="Lazy AJ • Auto Join")
    send_to_webhook(embed)

async def send_status_embed(status, game_id, player_name=None):
    embed = discord.Embed(
        title="🟢 LAZY AJ STATUS",
        description=f"**{status}**",
        color=0x00FF00 if "injected" in status.lower() else 0xFF6600,
        timestamp=datetime.now()
    )
    embed.add_field(name="🎮 Game ID", value=f"`{game_id}`", inline=True)
    if player_name:
        embed.add_field(name="👤 Player", value=player_name, inline=True)
    embed.set_footer(text="Lazy AJ • Made by tigy")
    send_to_webhook(embed)

# ============================================================
# BACKGROUND TASKS
# ============================================================
@tasks.loop(seconds=30)
async def check_schedules():
    """Check for brainrots that need to be detected"""
    now = datetime.now().timestamp()
    
    for name, data in BRAINROTS.items():
        if now - data["last"] >= data["interval"]:
            mutation = random.choice(MUTATIONS)
            trait = random.choice(TRAITS) if random.random() < 0.3 else None
            price = calculate_price(data["base"], mutation, trait)
            players = random.randint(1, 8)
            job_id = f"lazyaj_{int(now)}_{random.randint(1000,9999)}"
            
            await send_detection_embed(name, price, mutation, trait, players, 8, job_id)
            BRAINROTS[name]["last"] = now
            print(f"[{datetime.now()}] Sent detection: {name}")
            
            # Small delay before next
            await asyncio.sleep(random.randint(30, 90))

@tasks.loop(minutes=5)
async def status_heartbeat():
    """Send heartbeat every 5 minutes to show bot is alive"""
    embed = discord.Embed(
        title="💓 LAZY AJ HEARTBEAT",
        description="Bot is running and monitoring for brainrots",
        color=0x00FF00,
        timestamp=datetime.now()
    )
    embed.set_footer(text="Lazy AJ • Online 24/7")
    send_to_webhook(embed)

# ============================================================
# DISCORD COMMANDS
# ============================================================
@bot.event
async def on_ready():
    print(f"✅ Lazy AJ Bot is online!")
    print(f"   Logged in as: {bot.user}")
    print(f"   Webhook URL: {WEBHOOK_URL[:50]}...")
    print(f"   Monitoring {len(BRAINROTS)} brainrots")
    print("")
    
    # Start background tasks
    check_schedules.start()
    status_heartbeat.start()
    
    # Send startup message
    await send_status_embed("Lazy AJ Bot Injected & Running", "Multiple Games")

@bot.command()
async def status(ctx):
    """Check if the bot is running"""
    await ctx.send("✅ **Lazy AJ** is running 24/7! Made by tigy")

@bot.command()
async def test(ctx):
    """Send a test detection to the webhook"""
    await send_detection_embed("Test Brainrot", 5000, "Rainbow", "Divine", 4, 8, "test_123_456")
    await ctx.send("✅ Test detection sent to webhook!")

@bot.command()
async def next(ctx):
    """Show when the next brainrots are scheduled"""
    now = datetime.now().timestamp()
    msg = "**📅 Next Scheduled Brainrots:**\n```"
    for name, data in BRAINROTS.items():
        remaining = data["interval"] - (now - data["last"])
        if remaining > 0:
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)
            msg += f"\n• {name}: {minutes}m {seconds}s"
        else:
            msg += f"\n• {name}: 🔥 NOW!"
    msg += "\n```"
    await ctx.send(msg)

@bot.command()
async def stats(ctx):
    """Show bot statistics"""
    now = datetime.now().timestamp()
    total = len(BRAINROTS)
    active = 0
    for name, data in BRAINROTS.items():
        if now - data["last"] < data["interval"]:
            active += 1
    
    embed = discord.Embed(
        title="📊 Lazy AJ Statistics",
        color=0x00FF00,
        timestamp=datetime.now()
    )
    embed.add_field(name="🤖 Brainrots Monitored", value=str(total), inline=True)
    embed.add_field(name="⏳ Active Cooldowns", value=str(active), inline=True)
    embed.add_field(name="🎮 Allowed Games", value=str(len(ALLOWED_GAME_IDS)), inline=True)
    embed.add_field(name="🕐 Uptime", value="Since bot start", inline=True)
    embed.set_footer(text="Lazy AJ • Made by tigy")
    
    await ctx.send(embed=embed)

@bot.command()
async def helpme(ctx):
    """Show available commands"""
    embed = discord.Embed(
        title="🆘 Lazy AJ Commands",
        description="Here are all the available commands:",
        color=0x00FF00
    )
    embed.add_field(name="!status", value="Check if bot is running", inline=False)
    embed.add_field(name="!test", value="Send a test detection to webhook", inline=False)
    embed.add_field(name="!next", value="Show next scheduled brainrots", inline=False)
    embed.add_field(name="!stats", value="Show bot statistics", inline=False)
    embed.add_field(name="!helpme", value="Show this help message", inline=False)
    embed.set_footer(text="Lazy AJ • Made by tigy")
    
    await ctx.send(embed=embed)

# ============================================================
# RUN THE BOT
# ============================================================
TOKEN = os.environ.get("DISCORD_TOKEN")

if TOKEN is None:
    print("❌ ERROR: DISCORD_TOKEN environment variable not set!")
    print("   Please set your bot token and try again.")
    exit(1)

print("🔑 Token found, starting bot...")
bot.run(TOKEN)
