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

# ================== REAL BRAINROTS WITH ACTUAL BASE VALUES (in Millions) ==================
# Based on actual in-game values from Steal a Brainrot wiki

BRAINROT_VALUES = {
    # Secret Brainrots (Highest value)
    "Capitano Moby": {"base": 850, "tier": "Secret"},
    "Dragon Cannelloni": {"base": 250, "tier": "Secret"},
    "Hydra Dragon Cannelloni": {"base": 500, "tier": "Secret"},
    "Celestial Pegasus": {"base": 400, "tier": "Secret"},
    "Hydra Bunny": {"base": 350, "tier": "Secret"},
    "Griffin": {"base": 450, "tier": "Secret"},
    "Cerberus": {"base": 300, "tier": "Secret"},
    "Garama and Madundung": {"base": 280, "tier": "Secret"},
    "Fragrama and Chocrama": {"base": 200, "tier": "Secret"},
    "Ketupat Kepat": {"base": 180, "tier": "Secret"},
    "Secret Lucky Block": {"base": 150, "tier": "Secret"},
    "Nuclearo Dinossauro": {"base": 220, "tier": "Secret"},
    "DJ Panda": {"base": 190, "tier": "Secret"},
    "Money Money Puggy": {"base": 210, "tier": "Secret"},
    "Tang Tang Keletang": {"base": 170, "tier": "Secret"},
    "Tictac Sahur": {"base": 160, "tier": "Secret"},
    "Ketchuru and Musturu": {"base": 230, "tier": "Secret"},
    "Lavadorito Spinito": {"base": 240, "tier": "Secret"},
    "Ventoliero Pavonero": {"base": 260, "tier": "Secret"},
    "Cash or Card": {"base": 290, "tier": "Secret"},
    "Burguro And Fryuro": {"base": 270, "tier": "Secret"},
    "Los Mi Gatitos": {"base": 140, "tier": "Secret"},
    "Los Burritos": {"base": 145, "tier": "Secret"},
    "Mariachi Corazoni": {"base": 155, "tier": "Secret"},
    "Tacorita Bicicleta": {"base": 165, "tier": "Secret"},
    "Los Sweethearts": {"base": 175, "tier": "Secret"},
    "Camera Ramena": {"base": 185, "tier": "Secret"},
    "Los Hotspositos": {"base": 195, "tier": "Secret"},
    "Snailo Clovero": {"base": 125, "tier": "Secret"},
    "Chicleteira Cupideira": {"base": 135, "tier": "Secret"},
    "Los Spooky Combinasionas": {"base": 310, "tier": "Secret"},
    "Los Jolly Combinasionas": {"base": 320, "tier": "Secret"},
    "Cigno Fulgoro": {"base": 330, "tier": "Secret"},
    "Churrito Bunnito": {"base": 340, "tier": "Secret"},
    "La Exctinct Grande": {"base": 500, "tier": "Secret"},
    "Los Bros": {"base": 120, "tier": "Secret"},
    "La Spooky Grande": {"base": 400, "tier": "Secret"},
    "Chillin Chili": {"base": 110, "tier": "Secret"},
    "Chipso and Queso": {"base": 130, "tier": "Secret"},
    "Money Money Reindeer": {"base": 380, "tier": "Secret"},
    "Tuff Toucan": {"base": 100, "tier": "Secret"},
    "Tralaledon": {"base": 420, "tier": "Secret"},
    "Gobblino Uniciclino": {"base": 390, "tier": "Secret"},
    "Esok Sekolah": {"base": 105, "tier": "Secret"},
    "Los Cupids": {"base": 200, "tier": "Secret"},
    "Los Puggies": {"base": 115, "tier": "Secret"},
    "W or L": {"base": 95, "tier": "Secret"},
    "La Jolly Grande": {"base": 450, "tier": "Secret"},
    "Los Primos": {"base": 125, "tier": "Secret"},
    "Los Mariachis": {"base": 135, "tier": "Secret"},
    "Evelidon": {"base": 280, "tier": "Secret"},
    "Los Tacoritas": {"base": 145, "tier": "Secret"},
    "Lovin Rose": {"base": 155, "tier": "Secret"},
    "La Taco Combinasion": {"base": 300, "tier": "Secret"},
    "Orcaledon": {"base": 350, "tier": "Secret"},
    "Swaggy Bros": {"base": 160, "tier": "Secret"},
    "La Lucky Grande": {"base": 380, "tier": "Secret"},
    "La Romantic Grande": {"base": 390, "tier": "Secret"},
    "Gym Bros": {"base": 170, "tier": "Secret"},
    "Jolly Jolly Sahur": {"base": 200, "tier": "Secret"},
    "Gold Gold Gold": {"base": 500, "tier": "Secret"},
    "Fishino Clownino": {"base": 180, "tier": "Secret"},
    "Nacho Spyder": {"base": 190, "tier": "Secret"},
    "La Easter Grande": {"base": 350, "tier": "Secret"},
    "Cloverat Clapat": {"base": 220, "tier": "Secret"},
    "Spaghetti Tualetti": {"base": 230, "tier": "Secret"},
    "Festive 67": {"base": 240, "tier": "Secret"},
    "Los Spaghettis": {"base": 210, "tier": "Secret"},
    "Sammyni Fattini": {"base": 250, "tier": "Secret"},
    "Ginger Gerat": {"base": 260, "tier": "Secret"},
    "La Ginger Sekolah": {"base": 270, "tier": "Secret"},
    "Los Chillis": {"base": 140, "tier": "Secret"},
    "Spooky and Pumpky": {"base": 310, "tier": "Secret"},
    "La Food Combinasion": {"base": 320, "tier": "Secret"},
    "La Casa Boo": {"base": 290, "tier": "Secret"},
    "Los Sekolahs": {"base": 150, "tier": "Secret"},
    "Foxini Lanternini": {"base": 280, "tier": "Secret"},
    "La Secret Combinasionas": {"base": 450, "tier": "Secret"},
    "Los Amigos": {"base": 120, "tier": "Secret"},
    "Fortunu and Cashuru": {"base": 260, "tier": "Secret"},
    "Reinito Sleighito": {"base": 330, "tier": "Secret"},
    "Ketupat Bros": {"base": 200, "tier": "Secret"},
    "Cooki and Milki": {"base": 170, "tier": "Secret"},
    "Rosey and Teddy": {"base": 180, "tier": "Secret"},
    "Popcuru and Fizzuru": {"base": 190, "tier": "Secret"},
    "Bunny and Eggy": {"base": 210, "tier": "Secret"},
    "La Supreme Combinasion": {"base": 500, "tier": "Secret"},
    "Digi Narwhal": {"base": 300, "tier": "Secret"},
    "Love Love Bear": {"base": 250, "tier": "Secret"},
    "Dragon Gingerini": {"base": 350, "tier": "Secret"},
    
    # OG Brainrots
    "Strawberry Elephant": {"base": 400, "tier": "OG"},
    "Meowl": {"base": 350, "tier": "OG"},
    "Skibidi Toilet": {"base": 300, "tier": "OG"},
    "Headless Horseman": {"base": 450, "tier": "OG"},
    
    # Epic/Rare Brainrots
    "Scorpio": {"base": 50, "tier": "Epic"},
    "Baby Dragon": {"base": 40, "tier": "Epic"},
    "Camel": {"base": 15, "tier": "Rare"},
    "Rhino": {"base": 20, "tier": "Rare"},
    "Lazy Golem": {"base": 10, "tier": "Rare"},
    "Cute Cactus": {"base": 5, "tier": "Rare"},
    "Cool Lizard": {"base": 8, "tier": "Rare"},
}

# ================== REAL MUTATIONS ==================
MUTATIONS = {
    "Normal": {"mult": 1.0, "chance": 40},
    "Gold": {"mult": 1.25, "chance": 25},
    "Diamond": {"mult": 1.5, "chance": 20},
    "Rainbow": {"mult": 10, "chance": 8},
    "Divine": {"mult": 10, "chance": 5},
    "Cyber": {"mult": 11, "chance": 2}
}

# ================== REAL TRAITS ==================
TRAITS = {
    "Strawberry": {"mult": 8, "chance": 3},
    "Meowl": {"mult": 7, "chance": 4},
    "Lightning": {"mult": 6, "chance": 5},
    "Firework": {"mult": 6, "chance": 5},
    "Brazil": {"mult": 6, "chance": 5},
    "Nyan Cat": {"mult": 6, "chance": 5},
    "Chicleteira Graffiti": {"mult": 6, "chance": 4},
    "Tie": {"mult": 4.75, "chance": 6},
    "Spider": {"mult": 4.5, "chance": 6},
    "Galactic": {"mult": 4, "chance": 7},
    "Bombardiro": {"mult": 4, "chance": 7},
    "Extinct": {"mult": 4, "chance": 5},
    "Crab Rave": {"mult": 4, "chance": 6},
    "Bubblegum": {"mult": 4, "chance": 6}
}

SCRIPTS = [
    "Lazy Hub Premium", "Xen V2", "BK Hub Revamped", "Atlatic X",
    "Fluxus Ultimate", "Krnl Legacy", "Synapse Breaker", "ScriptWare Pro", 
    "Ez Hub Advanced", "Vega X", "Celestial", "Mystic Hub"
]

CENSORED_NAMES = [
    "************", "**********", "****", "*********", "*******", "***********", "******", "********"
]

TIER_COLORS = {
    "Secret": 0xFF44CC,
    "OG": 0xFF6600,
    "Epic": 0xAA44FF,
    "Rare": 0x4488FF,
}

# ================== PRICE CALCULATION ==================

def get_random_brainrot():
    brainrot_names = list(BRAINROT_VALUES.keys())
    name = random.choice(brainrot_names)
    tier = BRAINROT_VALUES[name]["tier"]
    base_value = BRAINROT_VALUES[name]["base"]
    return name, tier, base_value

def get_mutation():
    mutations_list = []
    weights = []
    for mut, data in MUTATIONS.items():
        mutations_list.append(mut)
        weights.append(data["chance"])
    mutation = random.choices(mutations_list, weights=weights, k=1)[0]
    return mutation, MUTATIONS[mutation]["mult"]

def get_trait():
    if random.random() < 0.35:
        traits_list = []
        weights = []
        for trait, data in TRAITS.items():
            traits_list.append(trait)
            weights.append(data["chance"])
        trait = random.choices(traits_list, weights=weights, k=1)[0]
        return trait, TRAITS[trait]["mult"]
    return None, 1

def calculate_price(base_value, mutation_mult, trait_mult):
    # Add randomness (15% variance)
    variance = 0.85 + (random.random() * 0.3)
    final_price = base_value * mutation_mult * trait_mult * variance
    # Cap at reasonable max (25B for rarest combos)
    final_price = min(final_price, 25000)
    final_price = max(final_price, base_value * 0.7)
    return round(final_price, 2)

def format_price(price_millions):
    if price_millions >= 1000:
        return f"${price_millions/1000:.2f}B"
    return f"${price_millions:.2f}M"

def get_censored_name():
    return random.choice(CENSORED_NAMES)

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

# ================== DETECTION LOOP ==================

@tasks.loop(seconds=50)
async def check_schedules():
    now = datetime.now().timestamp()
    
    if random.random() < 0.15:
        name, tier, base_value = get_random_brainrot()
        mutation, mutation_mult = get_mutation()
        trait, trait_mult = get_trait()
        
        price = calculate_price(base_value, mutation_mult, trait_mult)
        players = random.randint(1, 8)
        job_id = f"LH_{int(now)}_{random.randint(1000,9999)}"
        
        await send_detection_embed(name, price, mutation, trait, players, job_id, tier)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] DETECTED: {name} ({tier}) - Base: {base_value}M -> Final: {format_price(price)}")
        
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
    print(f"Monitoring {len(BRAINROT_VALUES)} brainrots with real base values")
    check_schedules.start()

@bot.command()
async def status(ctx):
    secret_count = sum(1 for v in BRAINROT_VALUES.values() if v["tier"] == "Secret")
    og_count = sum(1 for v in BRAINROT_VALUES.values() if v["tier"] == "OG")
    epic_count = sum(1 for v in BRAINROT_VALUES.values() if v["tier"] == "Epic")
    rare_count = sum(1 for v in BRAINROT_VALUES.values() if v["tier"] == "Rare")
    
    embed = discord.Embed(
        title="✅ Lazy Hub Bot",
        description="Monitoring real Brainrot Evolution brainrots with correct base values!",
        color=discord.Color.green()
    )
    embed.add_field(name="🔴 Secret", value=str(secret_count), inline=True)
    embed.add_field(name="🟠 OG", value=str(og_count), inline=True)
    embed.add_field(name="🟣 Epic", value=str(epic_count), inline=True)
    embed.add_field(name="🔵 Rare", value=str(rare_count), inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def test(ctx):
    name, tier, base_value = get_random_brainrot()
    mutation, mutation_mult = get_mutation()
    trait, trait_mult = get_trait()
    price = calculate_price(base_value, mutation_mult, trait_mult)
    await send_detection_embed(name, price, mutation, trait, 4, "TEST_001", tier)
    await asyncio.sleep(3)
    await send_stolen_embed(name, "Lazy Hub Premium", price, mutation, trait, tier)
    await ctx.send("✅ Test sent!")

# ================== START BOT ==================

TOKEN = os.environ.get("DISCORD_TOKEN")

if TOKEN is None:
    print("ERROR: DISCORD_TOKEN environment variable not set!")
    exit(1)

bot.run(TOKEN)
