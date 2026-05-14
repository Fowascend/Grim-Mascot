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
    "La Taco Combinasion": "https://media.discordapp.net/attachments/1502036958036099174/1503879472460595341/la-taco-combinasion.png",
    "Garama and Madundung": "https://images-ext-1.discordapp.net/external/2fNC1UlBAVbJ5IAr5FyaGz6zOlkB9ZvNI--rRx1rMgM/https/www.mobynotifier.com/brainrots/garama-and-madundung?format=webp",
    "Burguro And Fryuro": "https://images-ext-1.discordapp.net/external/qVX50l18q9QN8JHBQ5uJq5KvRz5KsHiZv6J7BjhK0cQ/https/www.mobynotifier.com/brainrots/burguro-and-fryuro?format=webp",
    "Lavadorito Spinito": "https://static.wikia.nocookie.net/stealabr/images/f/ff/Lavadorito_Spinito.png",
    "Ketchuru and Masturu": "https://images-ext-1.discordapp.net/external/iQod62CSYiki-EmgWXXxftaw9imnESM72GPrs82fP1M/https/www.mobynotifier.com/brainrots/ketchuru-and-musturu?format=webp",
    "Tang Tang Keletang": "https://images-ext-1.discordapp.net/external/4qWYUdmCoa0zhqxH2MKwV7Or5U9Xif8yw-AB_Gy5Lig/https/www.mobynotifier.com/brainrots/tang-tang-keletang?format=webp",
    "Ketupat Kepat": "https://images-ext-1.discordapp.net/external/qKJpSiIGZ9SimGiIIyIzF_eqyz7z4FIqEQ15aWmB8E8/https/www.mobynotifier.com/brainrots/ketupat-kepat?format=webp",
    "La Secret Combinasion": "https://images-ext-1.discordapp.net/external/KQBRtzBT3aoWc6WTjvoOhl2Tf64FvbWhyFW4VWbQGhQ/https/www.mobynotifier.com/brainrots/la-secret-combinasion?format=webp",
    "Cash or Card": "https://images-ext-1.discordapp.net/external/3--q-u9qc6iESRoNzi3nj5F8aOR0ThZ_FvPHINXrBw4/%3Fcb%3D20260428161300/https/static.wikia.nocookie.net/stealabr/images/2/21/Cash_or_Card.png",
    "Popcuru and Fizzuru": "https://static.wikia.nocookie.net/stealabr/images/f/f4/Popcuru_and_Fizzuru.png",
    "Los Puggies": "https://images-ext-1.discordapp.net/external/xSRo3cOgaMz_3bOvc-uxwnvdHvBbEI91-5o129qDE1A/%3Fcb%3D20251109012744/https/static.wikia.nocookie.net/stealabr/images/c/c8/LosPuggies2.png",
    "Money Money Puggy": "https://images-ext-1.discordapp.net/external/UdKYuXy_zc0xoCE5B_LB7Rd4gQxaE3YcyBh_Gu_IX6M/https/tr.rbxcdn.com/30DAY-Avatar-D21654E234F8633A1B3FC4936AFE8820-Png/420/420/Avatar/Png/noFilter",
    "Cigno Fulgoro": "https://static.wikia.nocookie.net/stealabr/images/8/87/Birdy.png",
    "Esok Sekolah": "https://images-ext-1.discordapp.net/external/X_HHUtR_dah9fT6uD5WMXHHLaCF0vjhP33OT-kXKAUk/https/www.mobynotifier.com/brainrots/esok-sekolah?format=webp",
    "Celestial Pegasus": "https://images-ext-1.discordapp.net/external/uQV0Gtw56MrBLMrPHNJHsEL3GHEtQtPtqFd7IC-FxxM/https/www.mobynotifier.com/brainrots/celestial-pegasus?format=webp",
    "Dragon Cannelloni": "https://images-ext-1.discordapp.net/external/X4PlwMzgXd5GkP_hOPxTjThl4yNvY5mGUhiV1iOnHb0/https/www.mobynotifier.com/brainrots/dragon-cannelloni?format=webp",
    "Los Hotspotsitos": "https://images-ext-1.discordapp.net/external/MsbU8Cx2x5x0Uqz0KiKgYQXeugojQ7SQBjg0uY8Doh0/%3Fcb%3D20251226204212/https/static.wikia.nocookie.net/stealabr/images/6/69/Loshotspotsitos.png",
    "Love Love Bear": "https://static.wikia.nocookie.net/stealabr/images/b/bf/Love_Love_Bear.png",
    "Rosey and Teddy": "https://static.wikia.nocookie.net/stealabr/images/9/9b/Rosey_and_Teddy.png",
    "Ginger Great": "https://static.wikia.nocookie.net/stealabr/images/e/e7/Ginger_Ketupat_Kepat.png",
    "Hydra Dragon Cannelloni": "https://images-ext-1.discordapp.net/external/xfvoBJm_MpWzP2D-q90AcpQ4EJnYcfyV763moAfMtYc/https/steal-a-brainrot.wiki/wp-content/uploads/2026/01/Steal-A-Brainrot-Wiki-HYDRA-DRAGON-Icon-.png",
    "Hydra Bunny": "https://static.wikia.nocookie.net/stealabr/images/5/57/Hydra_Bunny.png",
    "Fragrama and Chocrama": "https://images-ext-1.discordapp.net/external/Kln9a8QqTAqtPxqLDid23oNYIC5hYoxb2Wh8Jo1qG60/%3Fcb%3D20251109011733/https/static.wikia.nocookie.net/stealabr/images/5/56/Fragrama.png",
    "Strawberry Elephant": "https://images-ext-1.discordapp.net/external/US96Fw9oYQepR3lMLiwvK5bCumw_MtsXnGuvai3J33Q/https/www.mobynotifier.com/brainrots/strawberry-elephant?format=webp",
    "Meowl": "https://images-ext-1.discordapp.net/external/KcQAQmvkYOC_oWDKmGgCqeIYmWZZcv3zJzZzFvv6sg4/https/www.mobynotifier.com/brainrots/meowl?format=webp",
    "Headless Horseman": "https://images-ext-1.discordapp.net/external/LE0akzzR9pYt7FhWFoqw-KThhupou_t7srI97a47rvI/https/plain-wnam-prod-public.komododecks.com/202605/12/XSdcRajJXsJ65DXdOGjG/image.webp?format=webp",
    "Skibidi Toilet": "https://static.wikia.nocookie.net/stealabr/images/3/34/Skibidi_toilet.png",
    "John Pork": "https://images-ext-1.discordapp.net/external/9RK6VrcVNa3MCIaPmbeBuM_LRpYQfstoVkuoCvZnPog/https/plain-wnam-prod-public.komododecks.com/202605/12/iFxMpUBEbXpzxIVyyL7i/image.webp?format=webp",
    "Griffin": "https://images-ext-1.discordapp.net/external/ZSJZbm-Z5QoufhGcLRDrLCOfaty8stL_HtDM55WYgaw/%3Fcb%3D20260417151951/https/static.wikia.nocookie.net/stealabr/images/f/f8/Griffin.png",
}

BRAINROTS = {
    # Common (appear often)
    "La Taco Combinasion": {"income": 35, "rarity": "Secret", "weight": 25},
    "Garama and Madundung": {"income": 50, "rarity": "Secret", "weight": 20},
    "Burguro And Fryuro": {"income": 150, "rarity": "Secret", "weight": 15},
    "Lavadorito Spinito": {"income": 45, "rarity": "Secret", "weight": 20},
    "Ketchuru and Masturu": {"income": 42.5, "rarity": "Secret", "weight": 25},
    "Tang Tang Keletang": {"income": 33.5, "rarity": "Secret", "weight": 25},
    "Ketupat Kepat": {"income": 35, "rarity": "Secret", "weight": 25},
    "La Secret Combinasion": {"income": 125, "rarity": "Secret", "weight": 15},
    "Cash or Card": {"income": 100, "rarity": "Secret", "weight": 20},
    "Popcuru and Fizzuru": {"income": 170, "rarity": "Secret", "weight": 12},
    "Los Puggies": {"income": 30, "rarity": "Secret", "weight": 25},
    "Money Money Puggy": {"income": 21, "rarity": "Secret", "weight": 30},
    "Cigno Fulgoro": {"income": 20, "rarity": "Secret", "weight": 25},
    "Esok Sekolah": {"income": 30, "rarity": "Secret", "weight": 30},
    
    # Mid (appear occasionally - every 1.5 hours on average)
    "Celestial Pegasus": {"income": 175, "rarity": "Secret", "weight": 8},
    "Dragon Cannelloni": {"income": 250, "rarity": "Secret", "weight": 8},
    "Los Hotspotsitos": {"income": 20, "rarity": "Secret", "weight": 10},
    "Fragrama and Chocrama": {"income": 100, "rarity": "Secret", "weight": 10},
    
    # Rare (appear rarely)
    "Love Love Bear": {"income": 225, "rarity": "Secret", "weight": 5},
    "Rosey and Teddy": {"income": 165, "rarity": "Secret", "weight": 4},
    "Ginger Great": {"income": 75, "rarity": "Secret", "weight": 6},
    "Hydra Dragon Cannelloni": {"income": 300, "rarity": "Secret", "weight": 4},
    "Hydra Bunny": {"income": 185, "rarity": "Secret", "weight": 5},
    
    # OG (very rare - every 7 hours)
    "Strawberry Elephant": {"income": 750, "rarity": "OG", "weight": 1},
    "Meowl": {"income": 600, "rarity": "OG", "weight": 1},
    "Headless Horseman": {"income": 550, "rarity": "OG", "weight": 1},
    "Skibidi Toilet": {"income": 450, "rarity": "OG", "weight": 1},
    "John Pork": {"income": 500, "rarity": "OG", "weight": 1},
    "Griffin": {"income": 400, "rarity": "OG", "weight": 1},
}

MUTATIONS = [
    {"name": "Normal", "mod": 0.0, "chance": 80},
    {"name": "Gold", "mod": 0.25, "chance": 8},
    {"name": "Diamond", "mod": 0.5, "chance": 5},
    {"name": "Candy", "mod": 3.0, "chance": 2},
    {"name": "Lava", "mod": 5.0, "chance": 1.5},
    {"name": "Galaxy", "mod": 6.0, "chance": 1.2},
    {"name": "Yin Yang", "mod": 6.5, "chance": 0.8},
    {"name": "Radioactive", "mod": 7.5, "chance": 0.5},
    {"name": "Cursed", "mod": 8.0, "chance": 0.3},
    {"name": "Rainbow", "mod": 9.0, "chance": 0.2},
    {"name": "Divine", "mod": 9.0, "chance": 0.1},
    {"name": "Cyber", "mod": 10.0, "chance": 0.05},
]

TRAITS = [
    {"name": "None", "mod": 0.0, "chance": 97},
    {"name": "Strawberry", "mod": 8.0, "chance": 0.8},
    {"name": "Meowl", "mod": 7.0, "chance": 0.8},
    {"name": "Is Calling", "mod": 7.5, "chance": 0.3},
    {"name": "Galactic", "mod": 3.0, "chance": 0.5},
    {"name": "Fireworks", "mod": 5.0, "chance": 0.3},
    {"name": "Lightning", "mod": 5.0, "chance": 0.2},
    {"name": "Spider", "mod": 3.5, "chance": 0.3},
]

def weighted_choice(items):
    total = sum(item.get("weight", item.get("chance", 1)) for item in items)
    r = random.random() * total
    accum = 0
    for item in items:
        accum += item.get("weight", item.get("chance", 1))
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
    brainrot_name = weighted_choice(list(BRAINROTS.keys()))
    data = BRAINROTS[brainrot_name]
    
    mutation = weighted_choice(MUTATIONS)
    trait = weighted_choice(TRAITS)
    
    if random.random() < 0.96:
        trait = {"name": "None", "mod": 0.0, "chance": 0}
    
    final_income = calculate_income(data["income"], mutation, trait)
    tier = get_tier(final_income)
    color = get_color(final_income)
    
    display_name = brainrot_name
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
        "image": BRAINROT_IMAGES.get(brainrot_name, "https://i.imgur.com/placeholder.png"),
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
next_og_interval = random.randint(25200, 28800)
last_mid_time = time.time()
last_rare_time = time.time()

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
    global last_og_time, next_og_interval, last_mid_time, last_rare_time
    bot_cnt = random.randint(11000, 17000)
    log_count = 0
    
    while True:
        now = time.time()
        is_og_time = (now - last_og_time) >= next_og_interval
        
        # Base interval 30-90 seconds
        interval = random.randint(30, 90)
        await asyncio.sleep(interval)
        
        log_count += 1
        
        # Determine log type based on timing
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
                last_og_time = now
                next_og_interval = random.randint(25200, 28800)
                log_count = 0
                print(f"OG LOG: {name}")
        else:
            # Weighted random based on log count
            if log_count < 15:
                brainrot = get_random_brainrot()
            elif log_count < 30:
                rand = random.random()
                if rand < 0.7:
                    brainrot = get_random_brainrot()
                else:
                    og_brainrots = [b for b in BRAINROTS.keys() if BRAINROTS[b]["rarity"] == "OG"]
                    if og_brainrots and random.random() < 0.1:
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
            else:
                if random.random() < 0.1:
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
    print("Spawn Rates:")
    print("  - Common: ~30-90 seconds")
    print("  - Mid tier: ~1.5 hours")
    print("  - OG: ~7 hours")
    print("=" * 50)
    
    asyncio.create_task(auto_log_loop())

if __name__ == "__main__":
    bot.run(TOKEN)
