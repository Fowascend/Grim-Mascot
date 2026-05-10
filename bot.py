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

# ================== REAL BRAINROTS WITH CORRECT BASE PRICES (Millions) ==================
BRAINROT_VALUES = {
    # OG Brainrots (350B - 500B)
    "Skibidi Toilet": {"base": 350000, "tier": "OG", "min_b": 350, "max_b": 500},
    "Meowl": {"base": 400000, "tier": "OG", "min_b": 400, "max_b": 550},
    "Strawberry Elephant": {"base": 500000, "tier": "OG", "min_b": 500, "max_b": 650},
    
    # Secret Brainrots (5B+)
    "Garama and Madundung": {"base": 10000, "tier": "Secret", "min_b": 5, "max_b": 8},
    
    # Secret Brainrots (150M - 1B max, needs traits to go over 1B)
    "Cerberus": {"base": 150000, "tier": "Secret", "min_b": 0.15, "max_b": 1},
    "Capitano Moby": {"base": 125000, "tier": "Secret", "min_b": 0.125, "max_b": 1},
    "Cooki and Milki": {"base": 100000, "tier": "Secret", "min_b": 0.1, "max_b": 1},
    "Burguro and Fryuro": {"base": 75000, "tier": "Secret", "min_b": 0.075, "max_b": 1},
    "La Secret Combinasion": {"base": 50000, "tier": "Secret", "min_b": 0.05, "max_b": 1},
    "La Supreme Combinasion": {"base": 7000, "tier": "Secret", "min_b": 0.007, "max_b": 1},
    "Tictac Sahur": {"base": 6000, "tier": "Secret", "min_b": 0.006, "max_b": 1},
    "Ketupat Kepat": {"base": 5000, "tier": "Secret", "min_b": 0.005, "max_b": 1},
    "Los Tacoritas": {"base": 4000, "tier": "Secret", "min_b": 0.004, "max_b": 1},
    "La Extinct Grande": {"base": 3200, "tier": "Secret", "min_b": 0.0032, "max_b": 1},
    "Tralaledon": {"base": 3000, "tier": "Secret", "min_b": 0.003, "max_b": 1},
    "Chillin Chili": {"base": 3000, "tier": "Secret", "min_b": 0.003, "max_b": 1},
    "Ketchuru and Musturu": {"base": 40, "tier": "Secret", "min_b": 0.04, "max_b": 1},
    "Popcuro and Fizuro": {"base": 170, "tier": "Secret", "min_b": 0.17, "max_b": 1},
    "Dragon Cannelloni": {"base": 250, "tier": "Secret", "min_b": 0.25, "max_b": 1},
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

# ================== SCRIPTS ==================
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
    names = list(BRAINROT_VALUES.keys())
    weights = []
    for name in names:
        if BRAINROT_VALUES[name]["tier"] == "OG":
            weights.append(50)
        elif name == "Garama and Madundung":
            weights.append(30)
        else:
            weights.append(20)
    
    name = random.choices(names, weights=weights, k=1)[0]
    tier = BRAINROT_VALUES[name]["tier"]
    base_price = BRAINROT_VALUES[name]["base"]
    min_b = BRAINROT_VALUES[name]["min_b"]
    max_b = BRAINROT_VALUES[name]["max_b"]
    return name, tier, base_price, min_b, max_b

def get_mutation():
    muts = []
    weights = []
    for mut, data in MUTATIONS.items():
        muts.append(mut)
        weights.append(data["chance"])
    mutation = random.choices(muts, weights=weights, k=1)[0]
    return mutation, MUTATIONS[mutation]["mult"]

def get_multiple_traits():
    """Returns 0-3 traits"""
    # Higher chance for traits on valuable brainrots
    num_traits = random.choices([0, 1, 2, 3], weights=[30, 35, 25, 10], k=1)[0]
    
    traits = []
    total_mult = 1
    
    available_traits = list(TRAITS.keys())
    weights = [TRAITS[t]["chance"] for t in available_traits]
    
    for _ in range(num_traits):
        if available_traits:
            trait = random.choices(available_traits, weights=weights[:len(available_traits)], k=1)[0]
            traits.append(trait)
            total_mult *= TRAITS[trait]["mult"]
            idx = available_traits.index(trait)
            available_traits.pop(idx)
            weights.pop(idx)
    
    return traits, total_mult

def calculate_price(base_price, mutation_mult, trait_mult, min_billions, max_billions):
    variance = 0.9 + (random.random() * 0.2)
    final_millions = base_price * mutation_mult * trait_mult * variance
    
    min_millions = min_billions * 1000
    max_millions = max_billions * 1000
    
    # Cap at max billions
    final_millions = min(final_millions, max_millions)
    final_millions = max(final_millions, min_millions)
    
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
    embed.add_field(name=f"✨ Traits ({len(traits)})", value=trait_text, inline=True)
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

# ================== DETECTION LOOP ==================
@tasks.loop(seconds=25)
async def check_schedules():
    now = datetime.now().timestamp()
    
    if random.random() < 0.4:
        name, tier, base_price, min_b, max_b = get_random_brainrot()
        mutation, mutation_mult = get_mutation()
        traits, trait_mult = get_multiple_traits()
        
        price = calculate_price(base_price, mutation_mult, trait_mult, min_b, max_b)
        
        # Enforce rule: If base is under 150M (0.15B), cannot exceed 1B unless Garama
        if tier == "Secret" and base_price < 150 and name != "Garama and Madundung":
            if price > 1000:  # 1B
                price = random.uniform(500, 999)
        
        # Enforce rule: To be over 1B, must have traits AND mutation (not Normal)
        if price >= 1000 and tier != "OG":
            if len(traits) == 0 or mutation == "Normal":
                price = random.uniform(500, 999)
        
        players = random.randint(1, 8)
        job_id = f"SAB_{int(now)}_{random.randint(1000,9999)}"
        
        await send_detection_embed(name, price, mutation, traits, players, job_id, tier)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] DETECTED: {name} ({tier}) - {format_price(price)} with {len(traits)} traits")
        
        delay = random.randint(10, 45)
        await asyncio.sleep(delay)
        
        script = random.choice(SCRIPTS)
        await send_stolen_embed(name, script, price, mutation, traits, tier)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] STOLEN: {name}")
        
        await asyncio.sleep(random.randint(5, 15))

@bot.event
async def on_ready():
    print(f"Steal a Brainrot Bot online!")
    print(f"Logged in as {bot.user}")
    print(f"Monitoring {len(BRAINROT_VALUES)} Secret/OG brainrots")
    check_schedules.start()

@bot.command()
async def status(ctx):
    og_count = sum(1 for v in BRAINROT_VALUES.values() if v["tier"] == "OG")
    secret_count = sum(1 for v in BRAINROT_VALUES.values() if v["tier"] == "Secret")
    
    embed = discord.Embed(title="✅ Steal a Brainrot Bot", color=discord.Color.green())
    embed.add_field(name="🔴 OG Brainrots", value=og_count, inline=True)
    embed.add_field(name="💖 Secret Brainrots", value=secret_count, inline=True)
    embed.add_field(name="💰 Max Value", value="Secret: 1B (needs traits) | OG: 500B", inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def test(ctx):
    name, tier, base_price, min_b, max_b = get_random_brainrot()
    mutation, mutation_mult = get_mutation()
    traits, trait_mult = get_multiple_traits()
    price = calculate_price(base_price, mutation_mult, trait_mult, min_b, max_b)
    await send_detection_embed(name, price, mutation, traits, 4, "TEST_001", tier)
    await asyncio.sleep(3)
    await send_stolen_embed(name, "Xen Hub Pro", price, mutation, traits, tier)
    await ctx.send("✅ Test sent!")

TOKEN = os.environ.get("DISCORD_TOKEN")
if TOKEN is None:
    print("ERROR: DISCORD_TOKEN environment variable not set!")
    exit(1)

bot.run(TOKEN)
