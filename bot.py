import discord
from discord.ext import commands, tasks
import random
import os
import asyncio
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# ================== WEBHOOK ==================
WEBHOOK_URL = "https://discord.com/api/webhooks/1503087288190763200/-0weDNgQD3zAyL7hWgfFbgwA4qsNhuCmUDi2iph7uNUlpkOkp4E-6NpOit6dyTKwfol9"

# ================== REAL BRAINROTS FROM WIKI ==================
# Based on https://stealabrainrot.fandom.com/wiki/Steal_a_Brainrot_Wiki

BRAINROTS = {
    # Secret Rarity (Rarest in game)
    "Angelus": {"base": 500, "interval": 43200, "last": 0, "tier": "Secret"},
    "Gem Dog": {"base": 450, "interval": 43200, "last": 0, "tier": "Secret"},
    "Bunny": {"base": 400, "interval": 38800, "last": 0, "tier": "Secret"},
    "Radioactive Turtlez": {"base": 420, "interval": 40000, "last": 0, "tier": "Secret"},
    "Cyborg Monke": {"base": 380, "interval": 36000, "last": 0, "tier": "Secret"},
    
    # OG Rarity
    "Jester": {"base": 200, "interval": 21600, "last": 0, "tier": "OG"},
    "Fairy Queen": {"base": 190, "interval": 21600, "last": 0, "tier": "OG"},
    "Cake": {"base": 180, "interval": 20000, "last": 0, "tier": "OG"},
    "Pumpkin": {"base": 175, "interval": 20000, "last": 0, "tier": "OG"},
    "Skull": {"base": 170, "interval": 19000, "last": 0, "tier": "OG"},
    "Bat (OG)": {"base": 185, "interval": 19000, "last": 0, "tier": "OG"},
    "Reaper": {"base": 195, "interval": 21000, "last": 0, "tier": "OG"},
    "Grim Reaper": {"base": 210, "interval": 24000, "last": 0, "tier": "OG"},
    "Headless Horseman": {"base": 220, "interval": 26000, "last": 0, "tier": "OG"},
    "Krampus": {"base": 230, "interval": 28000, "last": 0, "tier": "OG"},
    
    # Mythical Rarity
    "Dark Demon": {"base": 300, "interval": 30000, "last": 0, "tier": "Mythical"},
    "Crabler": {"base": 280, "interval": 28000, "last": 0, "tier": "Mythical"},
    
    # Legendary Rarity
    "Scorpio": {"base": 120, "interval": 8000, "last": 0, "tier": "Legendary"},
    "Baby Dragon": {"base": 100, "interval": 7200, "last": 0, "tier": "Legendary"},
    "Medus": {"base": 110, "interval": 7800, "last": 0, "tier": "Legendary"},
    "Tripi Tropa": {"base": 115, "interval": 8000, "last": 0, "tier": "Legendary"},
}

EXTRA_BRAINROTS = [
    {"name": "Ketupat Kepat", "base": 80, "tier": "Epic"},
    {"name": "Camel", "base": 60, "tier": "Epic"},
    {"name": "Rhino", "base": 65, "tier": "Epic"},
    {"name": "Lazy Golem", "base": 50, "tier": "Rare"},
    {"name": "Cute Cactus", "base": 35, "tier": "Rare"},
    {"name": "Cool Lizard", "base": 40, "tier": "Rare"},
]

SCRIPTS = [
    "Lazy Hub Premium", "Lazy Hub Free", "Xen V2", "BK Hub Revamped", "Atlatic X",
    "Fluxus Ultimate", "Krnl Legacy", "Synapse Breaker", "ScriptWare Pro", 
    "Ez Hub Advanced", "Vega X", "Celestial", "Mystic Hub", "Nebula Executor",
    "Solaris", "Lunar Client", "Cosmic Hub", "Eclipse V3", "Aether Executor", 
    "Quantum Hub", "Zenith", "Lazy Hub Beta", "Lazy Hub Stable", "Lazy Hub AIO"
]

STEALERS = [
    "xX_Sniper_Xx", "BrainrotStealer", "AutoStealBot", "RareHunter23", 
    "StealGod69", "PetSniper", "LazyHubUser", "RareCollector", 
    "BrainrotKing", "StealMaster", "OGHunter", "SecretSnatcher"
]

# ================== MUTATIONS (REAL ONES) ==================

MUTATIONS = ["Cyber", "Divine", "Rainbow", "Cursed", "Radioactive", "Yin Yang", "Galaxy", "Lava", "Candy", "Diamond", "Gold", "Normal"]

MUTATION_MULTIPLIERS = {
    "Cyber": 11, "Divine": 10, "Rainbow": 10, "Cursed": 9,
    "Radioactive": 8.5, "Yin Yang": 7.5, "Galaxy": 7, "Lava": 6,
    "Candy": 4, "Diamond": 1.5, "Gold": 1.25, "Normal": 1
}

TRAITS = ["Strawberry", "Meowl", "Skibidi", "Nyan Cat", "Firework", "Brazil", "Lightning", "Chicleteira", "Tie", "Spider", "Asteroid", "Galactic", "Crab Rave", "Bubblegum", "Extinct"]

TRAIT_MULTIPLIERS = {
    "Strawberry": 8, "Meowl": 7, "Skibidi": 6.5, "Nyan Cat": 6,
    "Firework": 6, "Brazil": 6, "Lightning": 6, "Chicleteira": 6,
    "Tie": 4.75, "Spider": 4.5, "Asteroid": 4, "Galactic": 4,
    "Crab Rave": 4, "Bubblegum": 4, "Extinct": 4
}

TIER_COLORS = {
    "Secret": 0xFF44CC,
    "OG": 0xFF6600,
    "Mythical": 0xAA44FF,
    "Legendary": 0xFFAA00,
    "Epic": 0xAA44AA,
    "Rare": 0x4488FF,
}

TIER_MULTIPLIERS = {
    "Secret": 15,
    "OG": 1.2,
    "Mythical": 1.0,
    "Legendary": 0.8,
    "Epic": 0.6,
    "Rare": 0.4,
}

# ================== PRICE CALCULATION ==================

def calculate_price(base_value, tier, mutation, trait):
    tier_mult = TIER_MULTIPLIERS.get(tier, 1)
    mutation_mult = MUTATION_MULTIPLIERS.get(mutation, 1)
    trait_mult = TRAIT_MULTIPLIERS.get(trait, 1) if trait else 1
    
    variance = 0.85 + (random.random() * 0.3)
    
    final_value = base_value * tier_mult * mutation_mult * trait_mult * variance
    final_value = max(base_value, min(50000, final_value))
    return round(final_value, 1)

def format_price(value):
    if value >= 1000:
        return f"${value/1000:.2f}B"
    return f"${value:.1f}M"

# ================== GET MUTATION & TRAIT ==================

def get_combo():
    mutation = random.choice(MUTATIONS)
    
    if random.random() < 0.35:
        trait = random.choice(TRAITS)
        if trait == "Extinct" and random.random() > 0.15:
            trait = random.choice(["Strawberry", "Meowl", "Skibidi"])
    else:
        trait = None
    
    return mutation, trait

# ================== EMBED SENDING ==================

async def send_detection_embed(name, price, mutation, trait, players, maxpl, job_id, tier):
    color = TIER_COLORS.get(tier, 0x00FF00)
    
    price_text = format_price(price)
    if tier == "Secret":
        price_text = f"🔥 {price_text} 🔥"
    elif tier == "OG":
        price_text = f"✨ {price_text} ✨"
    
    embed = discord.Embed(
        title=f"🎯 {tier.upper()} BRAINROT DETECTED",
        description=f"**{name}** has spawned!",
        color=color,
        timestamp=datetime.now()
    )
    
    embed.add_field(name="💰 Estimated Value", value=price_text, inline=True)
    embed.add_field(name="🧬 Mutation", value=f"**{mutation}**", inline=True)
    if trait:
        embed.add_field(name="✨ Trait", value=f"**{trait}**", inline=True)
    else:
        embed.add_field(name="✨ Trait", value="None", inline=True)
    
    embed.add_field(name="👥 Server Population", value=f"{players}/{maxpl}", inline=True)
    embed.add_field(name="🏆 Rarity Tier", value=tier, inline=True)
    
    if job_id:
        embed.add_field(name="🔗 Session ID", value=f"`{job_id}`", inline=False)
    
    embed.set_footer(text="Lazy Hub • 24/7 Detection")
    
    import requests
    try:
        requests.post(WEBHOOK_URL, json={"embeds": [embed.to_dict()]})
    except Exception as e:
        print(f"Webhook error: {e}")

async def send_stolen_embed(name, script, price, mutation, trait, tier):
    embed = discord.Embed(
        title=f"⚠️ {tier.upper()} BRAINROT STOLEN",
        description=f"**{name}** was stolen!",
        color=0xFF4444,
        timestamp=datetime.now()
    )
    
    embed.add_field(name="👤 Stolen By", value=f"`{random.choice(STEALERS)}`", inline=True)
    embed.add_field(name="🛠️ Executor Used", value=f"`{script}`", inline=True)
    embed.add_field(name="💰 Stolen Value", value=format_price(price), inline=True)
    
    if mutation:
        embed.add_field(name="🧬 Mutation", value=mutation, inline=True)
    if trait:
        embed.add_field(name="✨ Trait", value=trait, inline=True)
    
    embed.add_field(name="⚡ Response Time", value=f"{random.randint(0, 3)}.{random.randint(0, 99)}s", inline=True)
    embed.set_footer(text="Lazy Hub • Auto-Steal System")
    
    import requests
    try:
        requests.post(WEBHOOK_URL, json={"embeds": [embed.to_dict()]})
    except Exception as e:
        print(f"Webhook error: {e}")

# ================== DETECTION LOOP ==================

@tasks.loop(seconds=30)
async def check_schedules():
    now = datetime.now().timestamp()
    
    for name, data in BRAINROTS.items():
        if now - data["last"] >= data["interval"]:
            mutation, trait = get_combo()
            price = calculate_price(data["base"], data["tier"], mutation, trait)
            players = random.randint(1, 8)  # Max 8 players per server
            job_id = f"LH_{int(now)}_{random.randint(1000,9999)}"
            
            await send_detection_embed(name, price, mutation, trait, players, 8, job_id, data["tier"])
            BRAINROTS[name]["last"] = now
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Detected: {name} ({data['tier']})")
            
            # Delay before theft
            if data["tier"] == "Secret":
                delay = random.randint(45, 120)
            elif data["tier"] == "OG":
                delay = random.randint(30, 90)
            else:
                delay = random.randint(15, 60)
            
            await asyncio.sleep(delay)
            
            script = random.choice(SCRIPTS)
            await send_stolen_embed(name, script, price, mutation, trait, data["tier"])
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Stolen: {name}")
            
            await asyncio.sleep(10)
    
    # Random extra detection (15% chance)
    if random.random() < 0.15:
        extra = random.choice(EXTRA_BRAINROTS)
        mutation, trait = get_combo()
        price = calculate_price(extra["base"], extra["tier"], mutation, trait)
        players = random.randint(1, 8)
        job_id = f"LH_extra_{int(now)}_{random.randint(1000,9999)}"
        
        await send_detection_embed(extra["name"], price, mutation, trait, players, 8, job_id, extra["tier"])
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Extra: {extra['name']}")
        
        delay = random.randint(15, 50)
        await asyncio.sleep(delay)
        
        script = random.choice(SCRIPTS)
        await send_stolen_embed(extra["name"], script, price, mutation, trait, extra["tier"])
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Extra Stolen: {extra['name']}")

# ================== BOT COMMANDS ==================

@bot.event
async def on_ready():
    print(f"Lazy Hub Bot online!")
    print(f"Logged in as {bot.user}")
    print(f"Monitoring {len(BRAINROTS)} real brainrots")
    check_schedules.start()

@bot.command()
async def status(ctx):
    embed = discord.Embed(
        title="✅ Lazy Hub Bot",
        description="Monitoring real brainrots!",
        color=discord.Color.green()
    )
    
    await ctx.send(embed=embed)

@bot.command()
async def test(ctx):
    mutation, trait = get_combo()
    price = calculate_price(200, "Secret", mutation, trait)
    await send_detection_embed("Angelus", price, mutation, trait, 4, 8, "TEST_001", "Secret")
    await asyncio.sleep(3)
    await send_stolen_embed("Angelus", "Lazy Hub Premium", price, mutation, trait, "Secret")
    await ctx.send("✅ Test sent!")

# ================== START BOT ==================

TOKEN = os.environ.get("DISCORD_TOKEN")

if TOKEN is None:
    print("ERROR: DISCORD_TOKEN not set!")
    exit(1)

bot.run(TOKEN)
