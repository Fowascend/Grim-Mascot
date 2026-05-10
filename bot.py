import discord
from discord.ext import commands, tasks
import random
import os
import asyncio
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# ================== WEBHOOK (UPDATED) ==================
WEBHOOK_URL = "https://discord.com/api/webhooks/1503087288190763200/-0weDNgQD3zAyL7hWgfFbgwA4qsNhuCmUDi2iph7uNUlpkOkp4E-6NpOit6dyTKwfol9"

# ================== ONLY OG & SECRET RARITY BRAINROTS (150M+ VALUE) ==================

BRAINROTS = {
    # OG Rarity (Original/Exclusive)
    "Jester": {"base": 150, "interval": 14400, "last": 0, "tier": "OG", "world": "Event"},
    "Fairy Queen": {"base": 155, "interval": 14400, "last": 0, "tier": "OG", "world": "Event"},
    "Cake": {"base": 160, "interval": 14400, "last": 0, "tier": "OG", "world": "Event"},
    "Pumpkin": {"base": 165, "interval": 14400, "last": 0, "tier": "OG", "world": "Event"},
    "Skull": {"base": 170, "interval": 15600, "last": 0, "tier": "OG", "world": "Event"},
    "Bat": {"base": 175, "interval": 15600, "last": 0, "tier": "OG", "world": "Event"},
    "Reaper": {"base": 180, "interval": 16800, "last": 0, "tier": "OG", "world": "Event"},
    "Grim Reaper": {"base": 190, "interval": 18000, "last": 0, "tier": "OG", "world": "Event"},
    "Headless Horseman": {"base": 200, "interval": 21600, "last": 0, "tier": "OG", "world": "Event"},
    "Krampus": {"base": 210, "interval": 21600, "last": 0, "tier": "OG", "world": "Event"},
    
    # Secret Rarity (Highest in game)
    "Huge Cat": {"base": 250, "interval": 28800, "last": 0, "tier": "Secret", "world": "Any"},
    "Huge Dog": {"base": 260, "interval": 28800, "last": 0, "tier": "Secret", "world": "Any"},
    "Huge Dragon": {"base": 280, "interval": 32400, "last": 0, "tier": "Secret", "world": "Any"},
    "Titanic Mutant": {"base": 350, "interval": 43200, "last": 0, "tier": "Secret", "world": "Event"},
    "Godshmallow": {"base": 400, "interval": 43200, "last": 0, "tier": "Secret", "world": "World 5"},
}

EXTRA_BRAINROTS = [
    {"name": "Ancient Kraken", "base": 300, "tier": "Secret", "world": "World 4"},
    {"name": "Marshcut", "base": 320, "tier": "Secret", "world": "World 5"},
    {"name": "Rudy", "base": 280, "tier": "Secret", "world": "World 5"},
    {"name": "Sekzari", "base": 290, "tier": "Secret", "world": "World 3"},
    {"name": "Anubis", "base": 310, "tier": "Secret", "world": "World 3"}
]

# Script names (Lazy Hub branding)
SCRIPTS = [
    "Lazy Hub Premium", "Lazy Hub Free", "Xen V2", "BK Hub Revamped", "Atlatic X",
    "Fluxus Ultimate", "Krnl Legacy", "Synapse Breaker", "ScriptWare Pro", 
    "Ez Hub Advanced", "Vega X", "Celestial", "Mystic Hub", "Nebula Executor",
    "Solaris", "Lunar Client", "Cosmic Hub", "Eclipse V3", "Aether Executor", 
    "Quantum Hub", "Zenith", "Lazy Hub Beta", "Lazy Hub Stable", "Lazy Hub AIO"
]

# ================== MUTATIONS ==================

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

# Tier colors and multipliers
TIER_COLORS = {
    "Secret": 0xFF44CC,
    "OG": 0xFF6600,
}

TIER_MULTIPLIERS = {
    "Secret": 15,
    "OG": 1.2,
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
    
    # 40% chance for a trait
    if random.random() < 0.4:
        trait = random.choice(TRAITS)
        # Extinct trait is rare
        if trait == "Extinct" and random.random() > 0.15:
            trait = random.choice(["Strawberry", "Meowl", "Skibidi"])
    else:
        trait = None
    
    return mutation, trait

# ================== EMBED SENDING ==================

async def send_detection_embed(name, price, mutation, trait, players, maxpl, job_id, tier, world):
    color = TIER_COLORS.get(tier, 0x00FF00)
    
    price_text = format_price(price)
    if tier == "Secret":
        price_text = f"🔥 {price_text} 🔥"
    elif tier == "OG":
        price_text = f"✨ {price_text} ✨"
    
    embed = discord.Embed(
        title=f"🎯 {tier.upper()} BRAINROT DETECTED",
        description=f"**{name}** has spawned in a server!",
        color=color,
        timestamp=datetime.now()
    )
    
    embed.add_field(name="💰 Estimated Value", value=price_text, inline=True)
    embed.add_field(name="🧬 Mutation", value=f"**{mutation}**", inline=True)
    if trait:
        embed.add_field(name="✨ Trait", value=f"**{trait}**", inline=True)
    else:
        embed.add_field(name="✨ Trait", value="None", inline=True)
    
    embed.add_field(name="🌍 World", value=world, inline=True)
    embed.add_field(name="👥 Server Population", value=f"{players}/{maxpl}", inline=True)
    embed.add_field(name="🏆 Rarity Tier", value=tier, inline=True)
    
    if job_id:
        embed.add_field(name="🔗 Session ID", value=f"`{job_id}`", inline=False)
    
    embed.set_footer(text="Lazy Hub • 24/7 Detection • Auto-Steal Ready")
    
    import requests
    try:
        requests.post(WEBHOOK_URL, json={"embeds": [embed.to_dict()]})
    except Exception as e:
        print(f"Webhook error: {e}")

async def send_stolen_embed(name, script, price, mutation, trait, tier, world):
    embed = discord.Embed(
        title=f"⚠️ {tier.upper()} BRAINROT STOLEN",
        description=f"**{name}** was successfully stolen!",
        color=0xFF4444,
        timestamp=datetime.now()
    )
    
    embed.add_field(name="👤 Stolen By", value="`Auto-Steal System`", inline=True)
    embed.add_field(name="🛠️ Executor Used", value=f"`{script}`", inline=True)
    embed.add_field(name="💰 Stolen Value", value=format_price(price), inline=True)
    
    if mutation:
        embed.add_field(name="🧬 Mutation", value=mutation, inline=True)
    if trait:
        embed.add_field(name="✨ Trait", value=trait, inline=True)
    
    embed.add_field(name="🌍 World", value=world, inline=True)
    embed.add_field(name="⚡ Response Time", value=f"{random.randint(0, 3)}.{random.randint(0, 99)}s", inline=True)
    embed.set_footer(text="Lazy Hub • Theft Alert • Join discord.gg/lazyhub")
    
    import requests
    try:
        requests.post(WEBHOOK_URL, json={"embeds": [embed.to_dict()]})
    except Exception as e:
        print(f"Webhook error: {e}")

# ================== DETECTION LOOP ==================

@tasks.loop(seconds=45)
async def check_schedules():
    now = datetime.now().timestamp()
    
    for name, data in BRAINROTS.items():
        if now - data["last"] >= data["interval"]:
            mutation, trait = get_combo()
            price = calculate_price(data["base"], data["tier"], mutation, trait)
            players = random.randint(3, 12)
            job_id = f"LH_{int(now)}_{random.randint(1000,9999)}"
            
            await send_detection_embed(name, price, mutation, trait, players, 12, job_id, data["tier"], data["world"])
            BRAINROTS[name]["last"] = now
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Detected: {name} ({data['tier']}) value: {format_price(price)}")
            
            # Delay based on tier
            if data["tier"] == "Secret":
                delay = random.randint(60, 180)
            else:
                delay = random.randint(30, 120)
            
            await asyncio.sleep(delay)
            
            script = random.choice(SCRIPTS)
            await send_stolen_embed(name, script, price, mutation, trait, data["tier"], data["world"])
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Stolen: {name}")
            
            await asyncio.sleep(15)
    
    # Random extra detection (20% chance)
    if random.random() < 0.2:
        extra = random.choice(EXTRA_BRAINROTS)
        mutation, trait = get_combo()
        price = calculate_price(extra["base"], extra["tier"], mutation, trait)
        players = random.randint(3, 10)
        job_id = f"LH_extra_{int(now)}_{random.randint(1000,9999)}"
        
        await send_detection_embed(extra["name"], price, mutation, trait, players, 12, job_id, extra["tier"], extra["world"])
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Extra Detected: {extra['name']}")
        
        delay = random.randint(20, 90)
        await asyncio.sleep(delay)
        
        script = random.choice(SCRIPTS)
        await send_stolen_embed(extra["name"], script, price, mutation, trait, extra["tier"], extra["world"])
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Extra Stolen: {extra['name']}")

# ================== BOT COMMANDS ==================

@bot.event
async def on_ready():
    print(f"Lazy Hub Bot is online!")
    print(f"Logged in as {bot.user}")
    print(f"Monitoring {len(BRAINROTS)} OG/Secret brainrots (150M+ value)")
    check_schedules.start()

@bot.command()
async def status(ctx):
    embed = discord.Embed(
        title="✅ Lazy Hub Bot Status",
        description="Monitoring high-value OG & Secret brainrots only!",
        color=discord.Color.green()
    )
    
    og_count = sum(1 for pet in BRAINROTS.values() if pet["tier"] == "OG")
    secret_count = sum(1 for pet in BRAINROTS.values() if pet["tier"] == "Secret")
    
    embed.add_field(name="📊 OG Brainrots", value=str(og_count), inline=True)
    embed.add_field(name="🔥 Secret Brainrots", value=str(secret_count), inline=True)
    embed.add_field(name="💰 Minimum Value", value="150M+", inline=True)
    
    await ctx.send(embed=embed)

@bot.command()
async def test(ctx):
    """Test the webhook"""
    mutation, trait = get_combo()
    price = calculate_price(200, "Secret", mutation, trait)
    await send_detection_embed("Huge Cat", price, mutation, trait, 6, 12, "TEST_001", "Secret", "Any")
    await asyncio.sleep(3)
    await send_stolen_embed("Huge Cat", "Lazy Hub Premium", price, mutation, trait, "Secret", "Any")
    await ctx.send("✅ Test sent to webhook!")

@bot.command()
async def next(ctx):
    """Show when next brainrots spawn"""
    now = datetime.now().timestamp()
    
    embed = discord.Embed(
        title="⏰ Next Scheduled High-Value Brainrots",
        description="OG & Secret rarity only",
        color=discord.Color.blue()
    )
    
    items = []
    for name, data in BRAINROTS.items():
        remaining = data["interval"] - (now - data["last"])
        if remaining > 0:
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)
            items.append((remaining, f"**{name}** ({data['tier']}): {minutes}m {seconds}s"))
    
    items.sort(key=lambda x: x[0])
    
    for _, text in items[:10]:
        embed.add_field(name="", value=text, inline=False)
    
    await ctx.send(embed=embed)

# ================== START BOT ==================

TOKEN = os.environ.get("DISCORD_TOKEN")

if TOKEN is None:
    print("ERROR: DISCORD_TOKEN environment variable not set!")
    exit(1)

bot.run(TOKEN)
