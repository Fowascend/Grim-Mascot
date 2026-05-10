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
# Secret Brainrots (can spawn on red carpet)
SECRET_BRAINROTS = [
    "Secret Lucky Block", "Nuclearo Dinossauro", "DJ Panda", "Money Money Puggy", "Tang Tang Keletang",
    "Ketupat Kepat", "Tictac Sahur", "Ketchuru and Musturu", "Lavadorito Spinito", "Garama and Madundung",
    "Ventoliero Pavonero", "Cash or Card", "Burguro And Fryuro", "Capitano Moby", "Cerberus", "Dragon Cannelloni",
    "Los Mi Gatitos", "Los Burritos", "Mariachi Corazoni", "Tacorita Bicicleta", "Los Sweethearts", "Camera Ramena",
    "Los Hotspositos", "Snailo Clovero", "Chicleteira Cupideira", "Los Spooky Combinasionas", "Los Jolly Combinasionas",
    "Cigno Fulgoro", "Churrito Bunnito", "La Exctinct Grande", "Los Bros", "La Spooky Grande", "Chillin Chili", 
    "Chipso and Queso", "Money Money Reindeer", "Tuff Toucan", "Tralaledon", "Gobblino Uniciclino", "Esok Sekolah",
    "Los Cupids", "Los Puggies", "W or L", "La Jolly Grande", "Los Primos", "Los Mariachis", "Evelidon", "Los Tacoritas",
    "Lovin Rose", "La Taco Combinasion", "Orcaledon", "Swaggy Bros", "La Lucky Grande", "La Romantic Grande", "Gym Bros",
    "Jolly Jolly Sahur", "Gold Gold Gold", "Fishino Clownino", "Nacho Spyder", "La Easter Grande", "Cloverat Clapat",
    "Spaghetti Tualetti", "Festive 67", "Los Spaghettis", "Sammyni Fattini", "Ginger Gerat", "La Ginger Sekolah", "Los Chillis",
    "Spooky and Pumpky", "La Food Combinasion", "Fragrama and Chocrama", "La Casa Boo", "Los Sekolahs", "Foxini Lanternini",
    "La Secret Combinasionas", "Los Amigos", "Fortunu and Cashuru", "Reinito Sleighito", "Ketupat Bros", "Cooki and Milki",
    "Rosey and Teddy", "Popcuru and Fizzuru", "Bunny and Eggy", "Celestial Pegasus", "Hydra Bunny", "La Supreme Combinasion",
    "Digi Narwhal", "Love Love Bear", "Dragon Gingerini", "Hydra Dragon Cannelloni", "Griffin"
]

# OG Brainrots
OG_BRAINROTS = [
    "Skibidi Toilet", "Meowl", "Strawberry Elephant", "Headless Horseman"
]

# Epic/Rare Brainrots (extra pool)
EXTRA_BRAINROTS = [
    "Camel", "Rhino", "Lazy Golem", "Cute Cactus", "Cool Lizard", "Scorpio", "Baby Dragon"
]

# ================== REAL MUTATIONS (Currently Obtainable) ==================
MUTATIONS = {
    "Normal": {"mult": 1.0, "chance": 40, "obtain": "Base brainrot"},
    "Gold": {"mult": 1.25, "chance": 25, "obtain": "Natural spawn on red carpet"},
    "Diamond": {"mult": 1.5, "chance": 20, "obtain": "Natural spawn on red carpet"},
    "Rainbow": {"mult": 10, "chance": 8, "obtain": "Natural spawn (rare) / Rainbow Machine Event"},
    "Divine": {"mult": 10, "chance": 5, "obtain": "Divine Event (every 30 minutes)"},
    "Cyber": {"mult": 11, "chance": 2, "obtain": "Cyber Event / Cyber Craft Machine"}
}

# ================== REAL TRAITS (Currently Obtainable) ==================
TRAITS = {
    # S-Tier Traits (Admin Events)
    "Strawberry": {"mult": 8, "chance": 3, "obtain": "Strawberry Elephant spawn event"},
    "Meowl": {"mult": 7, "chance": 4, "obtain": "Meowl spawn event"},
    "Lightning": {"mult": 6, "chance": 5, "obtain": "Galaxy-themed admin event"},
    "Firework": {"mult": 6, "chance": 5, "obtain": "July 4th / Fireworks celebration"},
    "Brazil": {"mult": 6, "chance": 5, "obtain": "Brazil concert event"},
    "Nyan Cat": {"mult": 6, "chance": 5, "obtain": "Nyan Cat admin event"},
    "Chicleteira Graffiti": {"mult": 6, "chance": 4, "obtain": "Ritual: 2 Chicleteira Bicicleteira"},
    
    # A-Tier Traits (Rituals + Events)
    "Tie": {"mult": 4.75, "chance": 6, "obtain": "Ritual: 4 Dul Dul Dul in square"},
    "Spider": {"mult": 4.5, "chance": 6, "obtain": "Ritual: 4 Sammyni Spyderini in square"},
    "Galactic": {"mult": 4, "chance": 7, "obtain": "Ritual: 3 La Vacca Saturno Saturnita"},
    "Bombardiro": {"mult": 4, "chance": 7, "obtain": "Ritual: 3 Bombardiro Crocodilo lined up"},
    "Extinct": {"mult": 4, "chance": 5, "obtain": "Extinct Event (every 2 hours)"},
    "Crab Rave": {"mult": 4, "chance": 6, "obtain": "Admin crab event"},
    "Bubblegum": {"mult": 4, "chance": 6, "obtain": "Bubblegum Machine / Feed 10 Candy"},
    
    # Weather Traits
    "Rain": {"mult": 2.5, "chance": 15, "obtain": "Random rain weather"},
    "Snowy": {"mult": 3, "chance": 8, "obtain": "Random snowfall weather"},
    "Starfall": {"mult": 3.5, "chance": 4, "obtain": "Random weather (rarest)"}
}

# ================== PRICE RANGES (Realistic - IN MILLIONS) ==================
# Prices are in diamonds (M = millions)
TIER_PRICE_RANGES = {
    "Secret": {"min": 5, "max": 80},      # 5M - 80M diamonds
    "OG": {"min": 2, "max": 40},          # 2M - 40M diamonds
    "Epic": {"min": 0.5, "max": 5},       # 500k - 5M diamonds
    "Rare": {"min": 0.1, "max": 1}        # 100k - 1M diamonds
}

SCRIPTS = [
    "Lazy Hub Premium", "Xen V2", "BK Hub Revamped", "Atlatic X",
    "Fluxus Ultimate", "Krnl Legacy", "Synapse Breaker", "ScriptWare Pro", 
    "Ez Hub Advanced", "Vega X", "Celestial", "Mystic Hub"
]

STEALERS = [
    "xX_Sniper_Xx", "BrainrotStealer", "AutoSteal", "RareHunter", 
    "StealGod", "PetSniper", "LazyHubUser", "RareCollector", 
    "BrainrotKing", "StealMaster", "OGHunter", "SecretSnatcher"
]

TIER_COLORS = {
    "Secret": 0xFF44CC,
    "OG": 0xFF6600,
    "Epic": 0xAA44FF,
    "Rare": 0x4488FF,
}

# ================== PRICE CALCULATION (REALISTIC) ==================

def get_random_brainrot():
    """Returns a random real brainrot from the wiki"""
    if random.random() < 0.7:  # 70% chance for Secret
        name = random.choice(SECRET_BRAINROTS)
        tier = "Secret"
    elif random.random() < 0.85:  # 15% chance for OG
        name = random.choice(OG_BRAINROTS)
        tier = "OG"
    else:  # 15% chance for Epic/Rare
        name = random.choice(EXTRA_BRAINROTS)
        tier = "Epic"
    
    return name, tier

def get_mutation():
    """Returns a random mutation based on actual spawn chances"""
    mutations_list = []
    weights = []
    for mut, data in MUTATIONS.items():
        mutations_list.append(mut)
        weights.append(data["chance"])
    
    mutation = random.choices(mutations_list, weights=weights, k=1)[0]
    return mutation, MUTATIONS[mutation]["mult"]

def get_trait():
    """Returns a random trait (35% chance) based on actual obtain rates"""
    if random.random() < 0.35:  # 35% chance to have a trait
        traits_list = []
        weights = []
        for trait, data in TRAITS.items():
            traits_list.append(trait)
            weights.append(data["chance"])
        
        trait = random.choices(traits_list, weights=weights, k=1)[0]
        return trait, TRAITS[trait]["mult"]
    return None, 1

def calculate_price(tier, mutation_mult, trait_mult):
    """Calculates realistic price in millions"""
    price_range = TIER_PRICE_RANGES.get(tier, {"min": 0.1, "max": 5})
    base_price = random.uniform(price_range["min"], price_range["max"])
    
    # Apply multipliers
    final_price = base_price * mutation_mult * trait_mult
    
    # Cap at reasonable values
    final_price = min(final_price, 150)  # Max 150M for rarest combos
    final_price = max(final_price, 0.05)  # Min 50k
    
    return round(final_price, 2)

def format_price(price_millions):
    """Formats price in millions (M) or billions (B) if over 1000M"""
    if price_millions >= 1000:
        return f"${price_millions/1000:.2f}B"
    return f"${price_millions:.2f}M"

# ================== EMBED SENDING ==================

async def send_detection_embed(name, price, mutation, trait, players, job_id, tier):
    color = TIER_COLORS.get(tier, 0x00FF00)
    
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

@tasks.loop(seconds=45)
async def check_schedules():
    now = datetime.now().timestamp()
    
    # Random delay between detections (60-180 seconds)
    if random.random() < 0.15:  # 15% chance to trigger
        name, tier = get_random_brainrot()
        mutation, mutation_mult = get_mutation()
        trait, trait_mult = get_trait()
        
        price = calculate_price(tier, mutation_mult, trait_mult)
        players = random.randint(1, 8)
        job_id = f"LH_{int(now)}_{random.randint(1000,9999)}"
        
        await send_detection_embed(name, price, mutation, trait, players, job_id, tier)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] DETECTED: {name} ({tier}) - {format_price(price)}")
        
        # Delay before theft (30-120 seconds)
        delay = random.randint(30, 120)
        await asyncio.sleep(delay)
        
        script = random.choice(SCRIPTS)
        await send_stolen_embed(name, script, price, mutation, trait, tier)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] STOLEN: {name}")

# ================== BOT COMMANDS ==================

@bot.event
async def on_ready():
    print(f"Lazy Hub Bot online!")
    print(f"Logged in as {bot.user}")
    print(f"Using REAL brainrots from wiki")
    check_schedules.start()

@bot.command()
async def status(ctx):
    embed = discord.Embed(
        title="✅ Lazy Hub Bot",
        description="Monitoring real Brainrot Evolution brainrots!",
        color=discord.Color.green()
    )
    embed.add_field(name="📊 Secret Brainrots", value=str(len(SECRET_BRAINROTS)), inline=True)
    embed.add_field(name="🔥 OG Brainrots", value=str(len(OG_BRAINROTS)), inline=True)
    embed.add_field(name="🧬 Mutations", value=str(len(MUTATIONS)), inline=True)
    embed.add_field(name="✨ Traits", value=str(len(TRAITS)), inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def test(ctx):
    name, tier = get_random_brainrot()
    mutation, mutation_mult = get_mutation()
    trait, trait_mult = get_trait()
    price = calculate_price(tier, mutation_mult, trait_mult)
    await send_detection_embed(name, price, mutation, trait, 4, "TEST_001", tier)
    await asyncio.sleep(5)
    await send_stolen_embed(name, "Lazy Hub Premium", price, mutation, trait, tier)
    await ctx.send("✅ Test sent!")

# ================== START BOT ==================

TOKEN = os.environ.get("DISCORD_TOKEN")

if TOKEN is None:
    print("ERROR: DISCORD_TOKEN environment variable not set!")
    exit(1)

bot.run(TOKEN)
