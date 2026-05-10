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
WEBHOOK_URL = "https://discord.com/api/webhooks/1503105638581014658/PLv94o-ZNO0S2PW86-M5um5wQpRg6VMtYjhxFMizrVIAnXaUOB6UByJZBsbIUosyM0E2"

# ================== REAL BRAINROTS (Secret + OG only) ==================
BRAINROT_VALUES = {
    # OG Brainrots (Can reach 23B with good traits/mutations)
    "Skibidi Toilet": {"base": 350000, "tier": "OG", "max_b": 23},
    "Meowl": {"base": 400000, "tier": "OG", "max_b": 23},
    "Strawberry Elephant": {"base": 500000, "tier": "OG", "max_b": 23},
    
    # Secret High Value (Max 5B)
    "Cerberus": {"base": 150000, "tier": "Secret", "max_b": 5},
    "Capitano Moby": {"base": 125000, "tier": "Secret", "max_b": 5},
    "Cooki and Milki": {"base": 100000, "tier": "Secret", "max_b": 5},
    "Dragon Cannelloni": {"base": 250, "tier": "Secret", "max_b": 23},
    "Burguro and Fryuro": {"base": 75000, "tier": "Secret", "max_b": 5},
    "La Secret Combinasion": {"base": 50000, "tier": "Secret", "max_b": 5},
    "Ketchuru and Musturu": {"base": 7500, "tier": "Secret", "max_b": 5},
    "La Supreme Combinasion": {"base": 7000, "tier": "Secret", "max_b": 5},
    "Tictac Sahur": {"base": 6000, "tier": "Secret", "max_b": 5},
    "Ketupat Kepat": {"base": 5000, "tier": "Secret", "max_b": 5},
    "Los Tacoritas": {"base": 4000, "tier": "Secret", "max_b": 5},
    "La Extinct Grande": {"base": 3200, "tier": "Secret", "max_b": 5},
    "Tralaledon": {"base": 3000, "tier": "Secret", "max_b": 5},
    "Chillin Chili": {"base": 3000, "tier": "Secret", "max_b": 5},
    "Garama and Madundung": {"base": 10000, "tier": "Secret", "max_b": 5},
    "Popcuro and Fizuro": {"base": 170, "tier": "Secret", "max_b": 5},
}

# ================== MUTATIONS ==================
MUTATIONS = {
    "Normal": {"mult": 1.0, "chance": 40},
    "Gold": {"mult": 1.25, "chance": 25},
    "Diamond": {"mult": 1.5, "chance": 20},
    "Rainbow": {"mult": 10, "chance": 8},
    "Divine": {"mult": 10, "chance": 5},
    "Cyber": {"mult": 11, "chance": 2}
}

# ================== TRAITS ==================
TRAITS = {
    "Strawberry": {"mult": 8, "chance": 3},
    "Meowl": {"mult": 7, "chance": 4},
    "Lightning": {"mult": 6, "chance": 5},
    "Firework": {"mult": 6, "chance": 5},
    "Brazil": {"mult": 6, "chance": 5},
    "Tie": {"mult": 4.75, "chance": 6},
    "Spider": {"mult": 4.5, "chance": 6},
    "Galactic": {"mult": 4, "chance": 7},
    "Extinct": {"mult": 4, "chance": 5},
}

# ================== SCRIPTS (No Lazy Hub) ==================
SCRIPTS = [
    "Xen Hub V2", "BK Hub Revamped", "Haze Hub Premium", "Xen Hub Pro",
    "BK Hub Ultimate", "Haze Hub AIO", "Xen Hub Legacy", "BK Hub X",
    "Haze Hub Advanced", "Xen Hub Beta", "BK Hub Elite", "Haze Hub Free"
]

# ================== CENSORED NAMES ==================
CENSORED_NAMES = ["************", "**********", "****", "*********", "*******", "***********"]

TIER_COLORS = {
    "OG": 0xFF0000,
    "Secret": 0xFF44CC,
}

def get_random_brainrot():
    """Returns a random brainrot weighted by value"""
    names = list(BRAINROT_VALUES.keys())
    # Weight OG and Dragon higher for better spawns
    weights = []
    for name in names:
        if BRAINROT_VALUES[name]["tier"] == "OG":
            weights.append(50)
        elif name == "Dragon Cannelloni":
            weights.append(40)
        else:
            weights.append(25)
    
    name = random.choices(names, weights=weights, k=1)[0]
    tier = BRAINROT_VALUES[name]["tier"]
    base_price = BRAINROT_VALUES[name]["base"]
    max_b = BRAINROT_VALUES[name]["max_b"]
    return name, tier, base_price, max_b

def get_mutation():
    muts = []
    weights = []
    for mut, data in MUTATIONS.items():
        muts.append(mut)
        weights.append(data["chance"])
    mutation = random.choices(muts, weights=weights, k=1)[0]
    return mutation, MUTATIONS[mutation]["mult"]

def get_multiple_traits():
    """Returns 0-3 traits for a brainrot (higher value pets get more traits)"""
    num_traits = random.choices([0, 1, 2, 3], weights=[40, 35, 18, 7], k=1)[0]
    
    traits = []
    total_mult = 1
    
    # Get available traits
    available_traits = list(TRAITS.keys())
    weights = [TRAITS[t]["chance"] for t in available_traits]
    
    for _ in range(num_traits):
        if available_traits:
            trait = random.choices(available_traits, weights=weights[:len(available_traits)], k=1)[0]
            traits.append(trait)
            total_mult *= TRAITS[trait]["mult"]
            # Remove to avoid duplicates
            idx = available_traits.index(trait)
            available_traits.pop(idx)
            weights.pop(idx)
    
    return traits, total_mult

def calculate_price(base_price, mutation_mult, trait_mult, max_billions):
    """Calculates price with cap"""
    variance = 0.9 + (random.random() * 0.2)
    final_millions = base_price * mutation_mult * trait_mult * variance
    
    # Cap at max billions
    max_millions = max_billions * 1000
    final_millions = min(final_millions, max_millions)
    final_millions = max(final_millions, base_price * 0.7)
    
    return round(final_millions, 2)

def format_price(price_millions):
    if price_millions >= 1000:
        return f"${price_millions/1000:.2f}B"
    return f"${price_millions:.0f}M"

def get_censored_name():
    return random.choice(CENSORED_NAMES)

async def send_detection_embed(name, price, mutation, traits, players, job_id, tier):
    color = TIER_COLORS.get(tier, 0xFF44CC)
    
    trait_text = ", ".join(traits) if traits else "None"
    if traits and len(traits) >= 2:
        trait_text = f"**{trait_text}** 🔥"
    
    embed = discord.Embed(
        title=f"🎯 {tier.upper()} BRAINROT DETECTED",
        description=f"**{name}** has spawned on the red carpet!",
        color=color,
        timestamp=datetime.now()
    )
    
    embed.add_field(name="💰 Estimated Value", value=format_price(price), inline=True)
    embed.add_field(name="🧬 Mutation", value=f"**{mutation}**", inline=True)
    embed.add_field(name="✨ Traits ({len(traits)})", value=trait_text, inline=True)
    embed.add_field(name="👥 Server Population", value=f"{players}/8", inline=True)
    embed.add_field(name="🏆 Rarity", value=tier, inline=True)
    embed.add_field(name="🔗 Session ID", value=f"`{job_id}`", inline=False)
    embed.set_footer(text="Steal a Brainrot • 24/7 Detection")
    
    import requests
    try:
        requests.post(WEBHOOK_URL, json={"embeds": [embed.to_dict()]})
    except Exception as e:
        print(f"Webhook error: {e}")

async def send_stolen_embed(name, script, price, mutation, traits, tier):
    trait_text = ", ".join(traits) if traits else "None"
    
    embed = discord.Embed(
        title=f"⚠️ {tier.upper()} BRAINROT STOLEN",
        description=f"**{name}** was stolen!",
        color=0xFF4444,
        timestamp=datetime.now()
    )
    
    embed.add_field(name="👤 Stolen By", value=f"`{get_censored_name()}`", inline=True)
    embed.add_field(name="🛠️ Executor Used", value=f"`{script}`", inline=True)
    embed.add_field(name="💰 Stolen Value", value=format_price(price), inline=True)
    embed.add_field(name="🧬 Mutation", value=mutation, inline=True)
    embed.add_field(name="✨ Traits", value=trait_text, inline=True)
    embed.add_field(name="⚡ Response Time", value=f"{random.randint(0, 3)}.{random.randint(0, 99)}s", inline=True)
    embed.set_footer(text="Auto-Steal System • Xen Hub/BK Hub/Haze Hub")
    
    import requests
    try:
        requests.post(WEBHOOK_URL, json={"embeds": [embed.to_dict()]})
    except Exception as e:
        print(f"Webhook error: {e}")

# ================== DETECTION LOOP (SENDS MORE LOGS) ==================
@tasks.loop(seconds=25)
async def check_schedules():
    now = datetime.now().timestamp()
    
    # Send detections more frequently (40% chance every 25 seconds)
    if random.random() < 0.4:
        name, tier, base_price, max_b = get_random_brainrot()
        mutation, mutation_mult = get_mutation()
        traits, trait_mult = get_multiple_traits()
        
        price = calculate_price(base_price, mutation_mult, trait_mult, max_b)
        players = random.randint(1, 8)
        job_id = f"SAB_{int(now)}_{random.randint(1000,9999)}"
        
        await send_detection_embed(name, price, mutation, traits, players, job_id, tier)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] DETECTED: {name} ({tier}) - {format_price(price)} with {len(traits)} traits")
        
        # Shorter delay before theft (10-45 seconds)
        delay = random.randint(10, 45)
        await asyncio.sleep(delay)
        
        script = random.choice(SCRIPTS)
        await send_stolen_embed(name, script, price, mutation, traits, tier)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] STOLEN: {name}")
        
        # Small delay between detections
        await asyncio.sleep(random.randint(5, 15))

@bot.event
async def on_ready():
    print(f"Steal a Brainrot Bot online!")
    print(f"Logged in as {bot.user}")
    print(f"Monitoring {len(BRAINROT_VALUES)} Secret/OG brainrots")
    print(f"Sending frequent detection logs")
    check_schedules.start()

@bot.command()
async def status(ctx):
    og_count = sum(1 for v in BRAINROT_VALUES.values() if v["tier"] == "OG")
    secret_count = sum(1 for v in BRAINROT_VALUES.values() if v["tier"] == "Secret")
    
    embed = discord.Embed(title="✅ Steal a Brainrot Bot", color=discord.Color.green())
    embed.add_field(name="🔴 OG Brainrots", value=og_count, inline=True)
    embed.add_field(name="💖 Secret Brainrots", value=secret_count, inline=True)
    embed.add_field(name="⚡ Detection Rate", value="~1-2 per minute", inline=True)
    embed.add_field(name="💰 Max Value", value="23B (OG/Dragon only)", inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def test(ctx):
    name, tier, base_price, max_b = get_random_brainrot()
    mutation, mutation_mult = get_mutation()
    traits, trait_mult = get_multiple_traits()
    price = calculate_price(base_price, mutation_mult, trait_mult, max_b)
    await send_detection_embed(name, price, mutation, traits, 4, "TEST_001", tier)
    await asyncio.sleep(3)
    await send_stolen_embed(name, "Xen Hub Pro", price, mutation, traits, tier)
    await ctx.send("✅ Test sent!")

TOKEN = os.environ.get("DISCORD_TOKEN")
if TOKEN is None:
    print("ERROR: DISCORD_TOKEN environment variable not set!")
    exit(1)

bot.run(TOKEN)
