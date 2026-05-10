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
WEBHOOK_URL = "https://discord.com/api/webhooks/1503105638581014658/PLv94o-ZNO0S2PW86-M5um5wQpRg6VMtYjhxFMizrVIAnXaUOB6UByJZBsbIUosyM0E2"

# ================== REAL BRAINROTS (Secret + OG only) ==================
# Base prices in MILLIONS (M)
BRAINROT_VALUES = {
    # OG Brainrots
    "Skibidi Toilet": {"price": 350000, "tier": "OG"},
    "Meowl": {"price": 400000, "tier": "OG"},
    "Strawberry Elephant": {"price": 500000, "tier": "OG"},
    
    # Secret Brainrots (Billions)
    "Cerberus": {"price": 150000, "tier": "Secret"},
    "Capitano Moby": {"price": 125000, "tier": "Secret"},
    "Cooki and Milki": {"price": 100000, "tier": "Secret"},
    "Dragon Cannelloni": {"price": 250, "tier": "Secret"},
    "Burguro and Fryuro": {"price": 75000, "tier": "Secret"},
    "La Secret Combinasion": {"price": 50000, "tier": "Secret"},
    "Ketchuru and Musturu": {"price": 7500, "tier": "Secret"},
    "La Supreme Combinasion": {"price": 7000, "tier": "Secret"},
    "Tictac Sahur": {"price": 6000, "tier": "Secret"},
    "Ketupat Kepat": {"price": 5000, "tier": "Secret"},
    "Los Tacoritas": {"price": 4000, "tier": "Secret"},
    "La Extinct Grande": {"price": 3200, "tier": "Secret"},
    "Tralaledon": {"price": 3000, "tier": "Secret"},
    "Chillin Chili": {"price": 3000, "tier": "Secret"},
    "Garama and Madundung": {"price": 10000, "tier": "Secret"},
    "Popciro and Fizuro": {"price": 170, "tier": "Secret"},
}

MUTATIONS = {
    "Normal": {"mult": 1.0, "chance": 40},
    "Gold": {"mult": 1.25, "chance": 25},
    "Diamond": {"mult": 1.5, "chance": 20},
    "Rainbow": {"mult": 10, "chance": 8},
    "Divine": {"mult": 10, "chance": 5},
    "Cyber": {"mult": 11, "chance": 2}
}

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

SCRIPTS = [
    "Lazy Hub Premium", "Xen V2", "BK Hub Revamped", "Atlatic X",
    "Fluxus Ultimate", "Krnl Legacy", "Synapse Breaker", "ScriptWare Pro", 
    "Ez Hub Advanced", "Vega X", "Celestial", "Mystic Hub"
]

CENSORED_NAMES = ["************", "**********", "****", "*********", "*******"]

TIER_COLORS = {
    "OG": 0xFF0000,
    "Secret": 0xFF44CC,
}

def get_random_brainrot():
    names = list(BRAINROT_VALUES.keys())
    weights = []
    for name in names:
        tier = BRAINROT_VALUES[name]["tier"]
        weights.append(60 if tier == "OG" else 40)
    name = random.choices(names, weights=weights, k=1)[0]
    tier = BRAINROT_VALUES[name]["tier"]
    base_price = BRAINROT_VALUES[name]["price"]
    return name, tier, base_price

def get_mutation():
    muts = []
    weights = []
    for mut, data in MUTATIONS.items():
        muts.append(mut)
        weights.append(data["chance"])
    mutation = random.choices(muts, weights=weights, k=1)[0]
    return mutation, MUTATIONS[mutation]["mult"]

def get_trait():
    if random.random() < 0.35:
        traits = []
        weights = []
        for trait, data in TRAITS.items():
            traits.append(trait)
            weights.append(data["chance"])
        trait = random.choices(traits, weights=weights, k=1)[0]
        return trait, TRAITS[trait]["mult"]
    return None, 1

def calculate_price(base_price, mutation_mult, trait_mult):
    variance = 0.9 + (random.random() * 0.2)
    final = base_price * mutation_mult * trait_mult * variance
    final = max(final, base_price * 0.85)
    return round(final, 2)

def format_price(price_millions):
    if price_millions >= 1000:
        return f"${price_millions/1000:.2f}B"
    return f"${price_millions:.0f}M"

def get_censored_name():
    return random.choice(CENSORED_NAMES)

async def send_detection_embed(name, price, mutation, trait, players, job_id, tier):
    color = TIER_COLORS.get(tier, 0xFF44CC)
    
    embed = discord.Embed(
        title=f"🎯 {tier.upper()} BRAINROT DETECTED",
        description=f"**{name}** has spawned on the red carpet!",
        color=color,
        timestamp=datetime.now()
    )
    
    embed.add_field(name="💰 Estimated Value", value=format_price(price), inline=True)
    embed.add_field(name="🧬 Mutation", value=f"**{mutation}**", inline=True)
    if trait:
        embed.add_field(name="✨ Trait", value=f"**{trait}**", inline=True)
    
    embed.add_field(name="👥 Server Population", value=f"{players}/8", inline=True)
    embed.add_field(name="🏆 Rarity", value=tier, inline=True)
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
    
    embed.add_field(name="👤 Stolen By", value=f"`{get_censored_name()}`", inline=True)
    embed.add_field(name="🛠️ Executor Used", value=f"`{script}`", inline=True)
    embed.add_field(name="💰 Stolen Value", value=format_price(price), inline=True)
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

@tasks.loop(seconds=50)
async def check_schedules():
    now = datetime.now().timestamp()
    
    if random.random() < 0.15:
        name, tier, base_price = get_random_brainrot()
        mutation, mutation_mult = get_mutation()
        trait, trait_mult = get_trait()
        
        price = calculate_price(base_price, mutation_mult, trait_mult)
        players = random.randint(1, 8)
        job_id = f"LH_{int(now)}_{random.randint(1000,9999)}"
        
        await send_detection_embed(name, price, mutation, trait, players, job_id, tier)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] DETECTED: {name} ({tier}) - {format_price(price)}")
        
        delay = random.randint(30, 120)
        await asyncio.sleep(delay)
        
        script = random.choice(SCRIPTS)
        await send_stolen_embed(name, script, price, mutation, trait, tier)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] STOLEN: {name}")

@bot.event
async def on_ready():
    print(f"Lazy Hub Bot online!")
    print(f"Logged in as {bot.user}")
    print(f"Monitoring {len(BRAINROT_VALUES)} Secret/OG brainrots")
    check_schedules.start()

@bot.command()
async def status(ctx):
    og_count = sum(1 for v in BRAINROT_VALUES.values() if v["tier"] == "OG")
    secret_count = sum(1 for v in BRAINROT_VALUES.values() if v["tier"] == "Secret")
    
    embed = discord.Embed(title="✅ Lazy Hub Bot", color=discord.Color.green())
    embed.add_field(name="🔴 OG Brainrots", value=og_count, inline=True)
    embed.add_field(name="💖 Secret Brainrots", value=secret_count, inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def test(ctx):
    name, tier, base_price = get_random_brainrot()
    mutation, mutation_mult = get_mutation()
    trait, trait_mult = get_trait()
    price = calculate_price(base_price, mutation_mult, trait_mult)
    await send_detection_embed(name, price, mutation, trait, 4, "TEST_001", tier)
    await asyncio.sleep(3)
    await send_stolen_embed(name, "Lazy Hub Premium", price, mutation, trait, tier)
    await ctx.send("✅ Test sent!")

TOKEN = os.environ.get("DISCORD_TOKEN")
if TOKEN is None:
    print("ERROR: DISCORD_TOKEN environment variable not set!")
    exit(1)
bot.run(TOKEN)
