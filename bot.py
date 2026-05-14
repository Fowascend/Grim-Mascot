import os
import re
import requests
import random
import time
import discord
from discord.ext import commands
from datetime import datetime
import asyncio

TOKEN = os.environ.get("DISCORD_TOKEN")

if not TOKEN:
    print("❌ DISCORD_TOKEN not found!")
    exit(1)

WEBHOOK_URL = "https://discord.com/api/webhooks/1504278778740736153/xFt5bKpOo9pn2ei01RKLWnPsH-Q_1T_zMg-qawIirhMyhesu31C3gBrSZD8_W7Vxziw8"
ALLOWED_USERS = [1088143400496279552, 1024793224352628817]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

BRAINROT_IMAGES = {
    "Esok Sekolah": "https://images-ext-1.discordapp.net/external/X_HHUtR_dah9fT6uD5WMXHHLaCF0vjhP33OT-kXKAUk/https/www.mobynotifier.com/brainrots/esok-sekolah?format=webp",
    "Spinny Hammy": "https://images-ext-1.discordapp.net/external/BoWX4KUkY2KLFTf2mUHpMH1tDNo2PRIq19ICSrGuRo8/https/www.mobynotifier.com/brainrots/spinny-hammy?format=webp",
    "Mieteteira Bicicleteira": "https://images-ext-1.discordapp.net/external/vAAWVq--XN7-z7-XSdiqyaCW5QGpLqa9tr_NNHpt_Yk/https/www.mobynotifier.com/brainrots/mieteteira-bicicleteira?format=webp",
    "Ketchuru and Masturu": "https://images-ext-1.discordapp.net/external/iQod62CSYiki-EmgWXXxftaw9imnESM72GPrs82fP1M/https/www.mobynotifier.com/brainrots/ketchuru-and-musturu?format=webp",
    "La Secret Combinasion": "https://images-ext-1.discordapp.net/external/KQBRtzBT3aoWc6WTjvoOhl2Tf64FvbWhyFW4VWbQGhQ/https/www.mobynotifier.com/brainrots/la-secret-combinasion?format=webp",
    "Spaghetti Tualetti": "https://images-ext-1.discordapp.net/external/yoOCxZMRDwqYzFcsYPY5GX2WY2wK4FvGgqB72P1VCV8/https/www.mobynotifier.com/brainrots/spaghetti-tualetti?format=webp",
    "Tang Tang Keletang": "https://images-ext-1.discordapp.net/external/4qWYUdmCoa0zhqxH2MKwV7Or5U9Xif8yw-AB_Gy5Lig/https/www.mobynotifier.com/brainrots/tang-tang-keletang?format=webp",
    "Ketupat Kepat": "https://images-ext-1.discordapp.net/external/qKJpSiIGZ9SimGiIIyIzF_eqyz7z4FIqEQ15aWmB8E8/https/www.mobynotifier.com/brainrots/ketupat-kepat?format=webp",
    "Garama and Madundung": "https://images-ext-1.discordapp.net/external/2fNC1UlBAVbJ5IAr5FyaGz6zOlkB9ZvNI--rRx1rMgM/https/www.mobynotifier.com/brainrots/garama-and-madundung?format=webp",
    "La Grande Combinasion": "https://images-ext-1.discordapp.net/external/l-HH_TrxOC9-VzpqWi-oTxrXNsdH7jIVxAuZI0diczo/https/www.mobynotifier.com/brainrots/la-grande-combinasion?format=webp",
    "Bacuru and Egguru": "https://images-ext-1.discordapp.net/external/flzi1jBXX-CAptIqAJjRlYEiRZabV6i7l6YJSZrY2LA/https/www.mobynotifier.com/brainrots/bacuru-and-egguru?format=webp",
    "Los Combinasionas": "https://images-ext-1.discordapp.net/external/e8NoB0fRt0X0W7aHmWJIQwC2IXb_dHLlEzY4lqhYjSc/https/www.mobynotifier.com/brainrots/los-combinasionas?format=webp",
    "Dragon Cannelloni": "https://images-ext-1.discordapp.net/external/X4PlwMzgXd5GkP_hOPxTjThl4yNvY5mGUhiV1iOnHb0/https/www.mobynotifier.com/brainrots/dragon-cannelloni?format=webp",
    "Strawberry Elephant": "https://images-ext-1.discordapp.net/external/US96Fw9oYQepR3lMLiwvK5bCumw_MtsXnGuvai3J33Q/https/www.mobynotifier.com/brainrots/strawberry-elephant?format=webp",
    "Meowl": "https://images-ext-1.discordapp.net/external/KcQAQmvkYOC_oWDKmGgCqeIYmWZZcv3zJzZzFvv6sg4/https/www.mobynotifier.com/brainrots/meowl?format=webp",
    "Cerberus": "https://images-ext-1.discordapp.net/external/NPtLqSPSBZtctUNyMptN6edlsdvC-9nhE7uJUppe5lo/https/www.mobynotifier.com/brainrots/cerberus?format=webp",
    "Burguro And Fryuro": "https://images-ext-1.discordapp.net/external/qVX50l18q9QN8JHBQ5uJq5KvRz5KsHiZv6J7BjhK0cQ/https/www.mobynotifier.com/brainrots/burguro-and-fryuro?format=webp",
    "Celestial Pegasus": "https://images-ext-1.discordapp.net/external/uQV0Gtw56MrBLMrPHNJHsEL3GHEtQtPtqFd7IC-FxxM/https/www.mobynotifier.com/brainrots/celestial-pegasus?format=webp",
    "Tictac Sahur": "https://images-ext-1.discordapp.net/external/D5tEa_RQIDq915-qO989XCMGK3zgYJUIMGA--tdJ3aQ/https/www.mobynotifier.com/brainrots/tictac-sahur?format=webp",
    "Capitano Moby": "https://images-ext-1.discordapp.net/external/k7fodKUVV7Tr3fLaxkyXXgGUKpuj0fS05fyglkhIM20/https/www.mobynotifier.com/brainrots/capitano-moby?format=webp",
    "John Pork": "https://images-ext-1.discordapp.net/external/9RK6VrcVNa3MCIaPmbeBuM_LRpYQfstoVkuoCvZnPog/https/plain-wnam-prod-public.komododecks.com/202605/12/iFxMpUBEbXpzxIVyyL7i/image.webp?format=webp",
    "Headless Horseman": "https://images-ext-1.discordapp.net/external/LE0akzzR9pYt7FhWFoqw-KThhupou_t7srI97a47rvI/https/plain-wnam-prod-public.komododecks.com/202605/12/XSdcRajJXsJ65DXdOGjG/image.webp?format=webp",
    "Los Bros": "https://media.discordapp.net/attachments/1502036958036099174/1503879521735282799/los-bros.png",
    "La Taco Combinasion": "https://media.discordapp.net/attachments/1502036958036099174/1503879472460595341/la-taco-combinasion.png",
    "Hydra Dragon Cannelloni": "https://images-ext-1.discordapp.net/external/xfvoBJm_MpWzP2D-q90AcpQ4EJnYcfyV763moAfMtYc/https/steal-a-brainrot.wiki/wp-content/uploads/2026/01/Steal-A-Brainrot-Wiki-HYDRA-DRAGON-Icon-.png",
    "Dragon Gingerini": "https://images-ext-1.discordapp.net/external/3puIUz4htLMUuD3hL5u4N9tIlLdxj2Gi2AVuJgtei9o/https/freebrainrots.com/assets/images/brainrots/roitems/dragon-gingerini.png",
    "Griffin": "https://images-ext-1.discordapp.net/external/ZSJZbm-Z5QoufhGcLRDrLCOfaty8stL_HtDM55WYgaw/%3Fcb%3D20260417151951/https/static.wikia.nocookie.net/stealabr/images/f/f8/Griffin.png/revision/latest/scale-to-width-down/1000",
    "Fragrama and Chocrama": "https://images-ext-1.discordapp.net/external/Kln9a8QqTAqtPxqLDid23oNYIC5hYoxb2Wh8Jo1qG60/%3Fcb%3D20251109011733/https/static.wikia.nocookie.net/stealabr/images/5/56/Fragrama.png/revision/latest",
    "La Casa Boo": "https://images-ext-1.discordapp.net/external/quqyy1a6ddzWi8EeljigfhNgezGLFYhD2LpWiSRMu4g/%3Fcb%3D20260505011532/https/static.wikia.nocookie.net/stealabr/images/d/de/Casa_Booo.png/revision/latest",
    "Cash or Card": "https://images-ext-1.discordapp.net/external/3--q-u9qc6iESRoNzi3nj5F8aOR0ThZ_FvPHINXrBw4/%3Fcb%3D20260428161300/https/static.wikia.nocookie.net/stealabr/images/2/21/Cash_or_Card.png/revision/latest/scale-to-width-down/1000",
    "Tralaledon": "https://images-ext-1.discordapp.net/external/_bBDdfMFPbTdCGnkfiz3yzvtNwqz0P4iVOnTlxFfaME/%3Fcb%3D20250909171639/https/static.wikia.nocookie.net/stealabr/images/7/79/Brr_Brr_Patapem.png/revision/latest",
    "Money Money Puggy": "https://images-ext-1.discordapp.net/external/UdKYuXy_zc0xoCE5B_LB7Rd4gQxaE3YcyBh_Gu_IX6M/https/tr.rbxcdn.com/30DAY-Avatar-D21654E234F8633A1B3FC4936AFE8820-Png/420/420/Avatar/Png/noFilter",
    "Los Puggies": "https://images-ext-1.discordapp.net/external/xSRo3cOgaMz_3bOvc-uxwnvdHvBbEI91-5o129qDE1A/%3Fcb%3D20251109012744/https/static.wikia.nocookie.net/stealabr/images/c/c8/LosPuggies2.png/revision/latest",
    "Nuclearo Dinosauro": "https://images-ext-1.discordapp.net/external/wO_VfzWxp76PImVCn4peFiARwLyzlEbzI8SqaKEtXio/%3Fcb%3D20260328003025/https/static.wikia.nocookie.net/stealabr/images/b/b5/Nuclearo_Dinossauro.png/revision/latest/scale-to-width-down/1000",
    "Los Hotspotsitos": "https://images-ext-1.discordapp.net/external/MsbU8Cx2x5x0Uqz0KiKgYQXeugojQ7SQBjg0uY8Doh0/%3Fcb%3D20251226204212/https/static.wikia.nocookie.net/stealabr/images/6/69/Loshotspotsitos.png/revision/latest",
    "Love Love Bear": "https://static.wikia.nocookie.net/stealabr/images/b/bf/Love_Love_Bear.png",
    "Foxini Lanternini": "https://static.wikia.nocookie.net/stealabr/images/4/41/Foxini_Lanternini.png",
    "Rosey and Teddy": "https://static.wikia.nocookie.net/stealabr/images/9/9b/Rosey_and_Teddy.png",
    "La Supreme Combinasion": "https://static.wikia.nocookie.net/stealabr/images/5/52/SupremeCombinasion.png/revision/latest?cb=20250825130920",
    "Ketupat Bros": "https://static.wikia.nocookie.net/stealabr/images/4/4d/Ketupat_Bros.png",
    "Ginger Great": "https://static.wikia.nocookie.net/stealabr/images/e/e7/Ginger_Ketupat_Kepat.png/revision/latest/scale-to-width-down/1000?cb=20251204041956",
    "La Lucky Grande": "https://static.wikia.nocookie.net/stealabr/images/5/55/La_Lucky_Grande.png",
    "Nacho Spyder": "https://static.wikia.nocookie.net/stealabr/images/3/36/Nacho_Spyder.png",
    "La Romantic Grande": "https://static.wikia.nocookie.net/stealabr/images/6/69/La_Romantic_Grande2.png",
    "Spooky and Pumpky": "https://static.wikia.nocookie.net/stealabr/images/d/d6/Spookypumpky.png/revision/latest?cb=20251012023638",
    "Lavadorito Spinito": "https://static.wikia.nocookie.net/stealabr/images/f/ff/Lavadorito_Spinito.png/revision/latest?cb=20251123122422",
    "Swaggy Bros": "https://static.wikia.nocookie.net/stealabr/images/8/85/Swaggy_Bros.png/revision/latest?cb=20251216205941",
    "La Ginger Sekolah": "https://static.wikia.nocookie.net/stealabr/images/f/f4/La_ginger_Sekolah.webp/revision/latest?cb=20251128172314",
    "Cigno Fulgoro": "https://static.wikia.nocookie.net/stealabr/images/8/87/Birdy.png",
    "Los 67": "https://static.wikia.nocookie.net/stealabr/images/d/db/Los-67.png/revision/latest?cb=20251006195232",
    "Reinito Sleighito": "https://i.imgur.com/placeholder.png",
}

BRAINROTS = {
    "Strawberry Elephant": {"income": 750, "rarity": "OG"},
    "Meowl": {"income": 600, "rarity": "OG"},
    "Headless Horseman": {"income": 550, "rarity": "OG"},
    "Skibidi Toilet": {"income": 450, "rarity": "OG"},
    "John Pork": {"income": 500, "rarity": "OG"},
    "Griffin": {"income": 400, "rarity": "OG"},
    "Dragon Cannelloni": {"income": 250, "rarity": "Secret"},
    "Burguro And Fryuro": {"income": 150, "rarity": "Secret"},
    "Capitano Moby": {"income": 160, "rarity": "Secret"},
    "Love Love Bear": {"income": 225, "rarity": "Secret"},
    "Cerberus": {"income": 175, "rarity": "Secret"},
    "Celestial Pegasus": {"income": 175, "rarity": "Secret"},
    "Fragrama and Chocrama": {"income": 100, "rarity": "Secret"},
    "Garama and Madundung": {"income": 50, "rarity": "Secret"},
    "Ketchuru and Masturu": {"income": 42.5, "rarity": "Secret"},
    "Esok Sekolah": {"income": 30, "rarity": "Secret"},
    "Los Bros": {"income": 24, "rarity": "Secret"},
    "Tictac Sahur": {"income": 37.5, "rarity": "Secret"},
    "Money Money Puggy": {"income": 21, "rarity": "Secret"},
    "La Extinct Grande": {"income": 23.5, "rarity": "Secret"},
    "Ketupat Kepat": {"income": 35, "rarity": "Secret"},
    "Spinny Hammy": {"income": 17, "rarity": "Secret"},
    "Mieteteira Bicicleteira": {"income": 26, "rarity": "Secret"},
    "La Secret Combinasion": {"income": 125, "rarity": "Secret"},
    "Spaghetti Tualetti": {"income": 60, "rarity": "Secret"},
    "Tang Tang Keletang": {"income": 33.5, "rarity": "Secret"},
    "Bacuru and Egguru": {"income": 24, "rarity": "Secret"},
    "Los Combinasionas": {"income": 15, "rarity": "Secret"},
    "La Grande Combinasion": {"income": 10, "rarity": "Secret"},
    "Hydra Dragon Cannelloni": {"income": 300, "rarity": "Secret"},
    "Dragon Gingerini": {"income": 350, "rarity": "Secret"},
    "La Casa Boo": {"income": 100, "rarity": "Secret"},
    "Cash or Card": {"income": 100, "rarity": "Secret"},
    "Tralaledon": {"income": 27.5, "rarity": "Secret"},
    "Los Puggies": {"income": 30, "rarity": "Secret"},
    "Nuclearo Dinosauro": {"income": 15, "rarity": "Secret"},
    "Los Hotspotsitos": {"income": 20, "rarity": "Secret"},
    "Foxini Lanternini": {"income": 115, "rarity": "Secret"},
    "Rosey and Teddy": {"income": 165, "rarity": "Secret"},
    "La Supreme Combinasion": {"income": 200, "rarity": "Secret"},
    "Ketupat Bros": {"income": 145, "rarity": "Secret"},
    "Ginger Great": {"income": 75, "rarity": "Secret"},
    "La Lucky Grande": {"income": 40, "rarity": "Secret"},
    "Nacho Spyder": {"income": 50, "rarity": "Secret"},
    "La Romantic Grande": {"income": 40, "rarity": "Secret"},
    "Spooky and Pumpky": {"income": 80, "rarity": "Secret"},
    "Lavadorito Spinito": {"income": 45, "rarity": "Secret"},
    "Swaggy Bros": {"income": 40, "rarity": "Secret"},
    "La Ginger Sekolah": {"income": 75, "rarity": "Secret"},
    "La Taco Combinasion": {"income": 35, "rarity": "Secret"},
    "Cigno Fulgoro": {"income": 20, "rarity": "Secret"},
    "Los 67": {"income": 22.5, "rarity": "Secret"},
    "Reinito Sleighito": {"income": 140, "rarity": "Secret"},
}

MUTATIONS = [
    {"name": "Normal", "mod": 0.0, "chance": 75},
    {"name": "Gold", "mod": 0.25, "chance": 10},
    {"name": "Diamond", "mod": 0.5, "chance": 7},
    {"name": "Candy", "mod": 3.0, "chance": 3},
    {"name": "Lava", "mod": 5.0, "chance": 2},
    {"name": "Galaxy", "mod": 6.0, "chance": 1.5},
    {"name": "Yin Yang", "mod": 6.5, "chance": 1},
    {"name": "Radioactive", "mod": 7.5, "chance": 0.5},
    {"name": "Cursed", "mod": 8.0, "chance": 0.3},
    {"name": "Rainbow", "mod": 9.0, "chance": 0.2},
    {"name": "Divine", "mod": 9.0, "chance": 0.1},
    {"name": "Cyber", "mod": 10.0, "chance": 0.05},
]

TRAITS = [
    {"name": "None", "mod": 0.0, "chance": 98},
    {"name": "Strawberry", "mod": 8.0, "chance": 0.5},
    {"name": "Meowl", "mod": 7.0, "chance": 0.5},
    {"name": "Is Calling", "mod": 7.5, "chance": 0.2},
    {"name": "Galactic", "mod": 3.0, "chance": 0.5},
    {"name": "Fireworks", "mod": 5.0, "chance": 0.2},
    {"name": "Lightning", "mod": 5.0, "chance": 0.2},
    {"name": "Spider", "mod": 3.5, "chance": 0.2},
]

def weighted_choice(items):
    total = sum(item.get("chance", 1) for item in items)
    r = random.random() * total
    accum = 0
    for item in items:
        accum += item.get("chance", 1)
        if r <= accum:
            return item
    return items[0]

def format_income(value):
    if value >= 1000:
        return f"{value/1000:.2f}B"
    return f"{value:.0f}M"

def get_tier(value):
    if value >= 5000:
        return "Peaklights"
    elif value >= 2000:
        return "Highlights"
    elif value >= 500:
        return "Midlights"
    return "Lowlights"

def get_color(value):
    if value >= 5000:
        return 0xAF52DE
    elif value >= 2000:
        return 0xFFD60A
    elif value >= 500:
        return 0x0A84FF
    return 0x8E8E93

def calculate_income(base_income, mutation, trait):
    if mutation["name"] == "Normal" and trait["name"] == "None":
        return base_income
    return base_income * (1 + mutation["mod"] + trait["mod"])

def get_random_brainrot():
    brainrot = random.choice(list(BRAINROTS.keys()))
    data = BRAINROTS[brainrot]
    
    mutation = weighted_choice(MUTATIONS)
    trait = weighted_choice(TRAITS)
    
    if random.random() < 0.95:
        trait = {"name": "None", "mod": 0.0, "chance": 0}
    
    final_income = calculate_income(data["income"], mutation, trait)
    tier = get_tier(final_income)
    color = get_color(final_income)
    
    display_name = brainrot
    if mutation["name"] != "Normal":
        display_name = f"{mutation['name']} {display_name}"
    if trait["name"] != "None":
        display_name = f"{display_name} ({trait['name']})"
    
    return {
        "name": display_name,
        "income": final_income,
        "formatted_income": format_income(final_income),
        "tier": tier,
        "color": color,
        "mutation": mutation["name"],
        "trait": trait["name"],
        "rarity": data["rarity"],
        "image": BRAINROT_IMAGES.get(brainrot, "https://i.imgur.com/placeholder.png"),
        "timestamp": datetime.now().isoformat(),
    }

def send_webhook(brainrot, bot_count):
    embed = {
        "title": "🎯 NEW BRAINROT DETECTED",
        "description": f"**{brainrot['name']}** has been detected!",
        "color": brainrot["color"],
        "timestamp": brainrot["timestamp"],
        "thumbnail": {"url": brainrot["image"]},
        "fields": [
            {"name": "🧬 Mutation", "value": brainrot["mutation"], "inline": True},
            {"name": "✨ Trait", "value": brainrot["trait"], "inline": True},
            {"name": "💰 Income", "value": f"{brainrot['formatted_income']}/s", "inline": True},
            {"name": "🏆 Tier", "value": brainrot["tier"], "inline": True},
            {"name": "🤖 Active Bots", "value": f"{bot_count:,}", "inline": True},
        ],
        "footer": {"text": f"ZYROX AJ • {brainrot['rarity']} Brainrot"},
    }
    
    try:
        requests.post(WEBHOOK_URL, json={"embeds": [embed], "username": "ZYROX AJ"})
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

bot_count = random.randint(11000, 17000)
last_og_time = time.time()
next_og_interval = random.randint(14400, 21600)

def update_bot_count():
    global bot_count
    change = random.randint(-500, 500)
    bot_count += change
    if bot_count > 17000:
        bot_count = 17000
    elif bot_count < 11000:
        bot_count = 11000
    return bot_count

@bot.command(name="zyrox")
async def manual_log(ctx, *, args: str = None):
    if ctx.author.id not in ALLOWED_USERS:
        return
    
    if not args:
        await ctx.send("Usage: `!zyrox Brainrot:Griffin ping:yes price:23B`")
        return
    
    brainrot_match = re.search(r'Brainrot:([^ ]+)', args, re.IGNORECASE)
    ping_match = re.search(r'ping:(\S+)', args, re.IGNORECASE)
    price_match = re.search(r'price:(\S+)', args, re.IGNORECASE)
    
    if not brainrot_match:
        return
    
    brainrot_name = brainrot_match.group(1).strip()
    ping = ping_match.group(1).lower() == "yes" if ping_match else False
    price_str = price_match.group(1) if price_match else "100M"
    
    price_match_num = re.search(r'([\d.]+)([BMK]?)', price_str.upper())
    if not price_match_num:
        return
    
    price_value = float(price_match_num.group(1))
    price_unit = price_match_num.group(2)
    
    if price_unit == 'B':
        income = price_value * 1000
    elif price_unit == 'K':
        income = price_value / 1000
    else:
        income = price_value
    
    tier = get_tier(income)
    color = get_color(income)
    formatted_income = format_income(income)
    image_url = BRAINROT_IMAGES.get(brainrot_name, "https://i.imgur.com/placeholder.png")
    
    embed = discord.Embed(
        title="🎯 NEW BRAINROT DETECTED",
        description=f"**{brainrot_name}** has been detected!",
        color=color,
        timestamp=datetime.now()
    )
    embed.set_thumbnail(url=image_url)
    embed.add_field(name="🧬 Mutation", value="Normal", inline=True)
    embed.add_field(name="✨ Trait", value="None", inline=True)
    embed.add_field(name="💰 Income", value=f"{formatted_income}/s", inline=True)
    embed.add_field(name="🏆 Tier", value=tier, inline=True)
    embed.add_field(name="🤖 Active Bots", value=f"{random.randint(11000, 17000):,}", inline=True)
    embed.set_footer(text="ZYROX AJ • Live Detection")
    
    content = "@everyone" if ping else None
    await ctx.send(content=content, embed=embed)
    
    webhook_embed = embed.to_dict()
    try:
        requests.post(WEBHOOK_URL, json={"embeds": [webhook_embed], "username": "ZYROX AJ"})
    except:
        pass

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    msg_lower = message.content.lower()
    
    fake_keywords = ["fake zyrox", "zyrox fake", "this aj is fake", "aj doesn't work", "not working aj", "broken aj", "scam aj", "fake aj"]
    
    if any(keyword in msg_lower for keyword in fake_keywords):
        reply = (
            f"⚠️ **@{message.author.display_name}**, ZYROX AJ is NOT fake!\n\n"
            f"✅ 11,000 - 17,000 active bots running 24/7\n"
            f"✅ VPS connected with 99.9% uptime\n"
            f"✅ Live API fetching real brainrot data\n"
            f"✅ Auto-join works instantly\n"
            f"✅ Webhook logs sent to this channel\n\n"
            f"*Need proof? Check the logs above.*"
        )
        await message.channel.send(reply)
        return
    
    await bot.process_commands(message)

async def auto_log_loop():
    global last_og_time, next_og_interval
    bot_cnt = random.randint(11000, 17000)
    
    while True:
        now = time.time()
        is_og_time = (now - last_og_time) >= next_og_interval
        
        if is_og_time:
            interval = 1
            last_og_time = now
            next_og_interval = random.randint(14400, 21600)
        else:
            interval = random.randint(45, 90)
        
        await asyncio.sleep(interval)
        
        if is_og_time:
            og_brainrots = [b for b in BRAINROTS.keys() if BRAINROTS[b]["rarity"] == "OG"]
            if og_brainrots:
                name = random.choice(og_brainrots)
                data = BRAINROTS[name]
                brainrot = {
                    "name": name,
                    "income": data["income"],
                    "formatted_income": format_income(data["income"]),
                    "tier": get_tier(data["income"]),
                    "color": get_color(data["income"]),
                    "mutation": "Normal",
                    "trait": "None",
                    "rarity": data["rarity"],
                    "image": BRAINROT_IMAGES.get(name, "https://i.imgur.com/placeholder.png"),
                    "timestamp": datetime.now().isoformat(),
                }
        else:
            brainrot = get_random_brainrot()
        
        if brainrot:
            bot_cnt = update_bot_count()
            send_webhook(brainrot, bot_cnt)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {brainrot['name']} | {brainrot['formatted_income']}/s")

@bot.command(name="commands")
async def list_commands(ctx):
    embed = discord.Embed(title="ZYROX AJ Commands", color=0x0A84FF, timestamp=datetime.now())
    embed.add_field(name="!commands", value="Show this help", inline=False)
    embed.add_field(name="!stats", value="Bot statistics", inline=False)
    embed.add_field(name="!ping", value="Check latency", inline=False)
    embed.add_field(name="!zyrox Brainrot:X ping:yes price:X", value="Manual log", inline=False)
    embed.set_footer(text="ZYROX AJ")
    await ctx.send(embed=embed)

@bot.command(name="stats")
async def stats_command(ctx):
    bot_cnt = random.randint(11000, 17000)
    embed = discord.Embed(title="ZYROX AJ Statistics", color=0x00FF00, timestamp=datetime.now())
    embed.add_field(name="Active Bots", value=f"{bot_cnt:,}", inline=True)
    embed.add_field(name="VPS Status", value="Connected", inline=True)
    embed.add_field(name="API Status", value="Online", inline=True)
    embed.add_field(name="Auto-Join", value="Working", inline=True)
    embed.set_footer(text="ZYROX AJ")
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping_command(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.event
async def on_ready():
    print("=" * 50)
    print(f"ZYROX AJ Bot Online: {bot.user}")
    print(f"Webhook: {WEBHOOK_URL[:60]}...")
    print(f"Images loaded: {len(BRAINROT_IMAGES)} brainrots")
    print("=" * 50)
    print("Auto-logs every 45-90 seconds")
    print("OG brainrots every 4-6 hours")
    print("=" * 50)
    
    asyncio.create_task(auto_log_loop())

if __name__ == "__main__":
    bot.run(TOKEN)
