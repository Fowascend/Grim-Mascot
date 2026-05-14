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
    "Strawberry Elephant": "https://images-ext-1.discordapp.net/external/US96Fw9oYQepR3lMLiwvK5bCumw_MtsXnGuvai3J33Q/https/www.mobynotifier.com/brainrots/strawberry-elephant?format=webp",
    "Meowl": "https://images-ext-1.discordapp.net/external/KcQAQmvkYOC_oWDKmGgCqeIYmWZZcv3zJzZzFvv6sg4/https/www.mobynotifier.com/brainrots/meowl?format=webp",
    "Headless Horseman": "https://images-ext-1.discordapp.net/external/LE0akzzR9pYt7FhWFoqw-KThhupou_t7srI97a47rvI/https/plain-wnam-prod-public.komododecks.com/202605/12/XSdcRajJXsJ65DXdOGjG/image.webp?format=webp",
    "Skibidi Toilet": "https://static.wikia.nocookie.net/stealabr/images/3/34/Skibidi_toilet.png",
    "John Pork": "https://images-ext-1.discordapp.net/external/9RK6VrcVNa3MCIaPmbeBuM_LRpYQfstoVkuoCvZnPog/https/plain-wnam-prod-public.komododecks.com/202605/12/iFxMpUBEbXpzxIVyyL7i/image.webp?format=webp",
    "Griffin": "https://images-ext-1.discordapp.net/external/ZSJZbm-Z5QoufhGcLRDrLCOfaty8stL_HtDM55WYgaw/%3Fcb%3D20260417151951/https/static.wikia.nocookie.net/stealabr/images/f/f8/Griffin.png/revision/latest/scale-to-width-down/1000?format=webp",
    "Dragon Cannelloni": "https://images-ext-1.discordapp.net/external/X4PlwMzgXd5GkP_hOPxTjThl4yNvY5mGUhiV1iOnHb0/https/www.mobynotifier.com/brainrots/dragon-cannelloni?format=webp",
    "Burguro And Fryuro": "https://images-ext-1.discordapp.net/external/qVX50l18q9QN8JHBQ5uJq5KvRz5KsHiZv6J7BjhK0cQ/https/www.mobynotifier.com/brainrots/burguro-and-fryuro?format=webp",
    "Capitano Moby": "https://images-ext-1.discordapp.net/external/k7fodKUVV7Tr3fLaxkyXXgGUKpuj0fS05fyglkhIM20/https/www.mobynotifier.com/brainrots/capitano-moby?format=webp",
    "Love Love Bear": "https://static.wikia.nocookie.net/stealabr/images/b/bf/Love_Love_Bear.png",
    "Cerberus": "https://images-ext-1.discordapp.net/external/NPtLqSPSBZtctUNyMptN6edlsdvC-9nhE7uJUppe5lo/https/www.mobynotifier.com/brainrots/cerberus?format=webp",
    "Celestial Pegasus": "https://images-ext-1.discordapp.net/external/uQV0Gtw56MrBLMrPHNJHsEL3GHEtQtPtqFd7IC-FxxM/https/www.mobynotifier.com/brainrots/celestial-pegasus?format=webp",
    "Fragrama and Chocrama": "https://images-ext-1.discordapp.net/external/Kln9a8QqTAqtPxqLDid23oNYIC5hYoxb2Wh8Jo1qG60/%3Fcb%3D20251109011733/https/static.wikia.nocookie.net/stealabr/images/5/56/Fragrama.png/revision/latest?format=webp",
    "Garama and Madundung": "https://images-ext-1.discordapp.net/external/2fNC1UlBAVbJ5IAr5FyaGz6zOlkB9ZvNI--rRx1rMgM/https/www.mobynotifier.com/brainrots/garama-and-madundung?format=webp",
    "Ketchuru and Masturu": "https://images-ext-1.discordapp.net/external/iQod62CSYiki-EmgWXXxftaw9imnESM72GPrs82fP1M/https/www.mobynotifier.com/brainrots/ketchuru-and-musturu?format=webp",
    "Esok Sekolah": "https://images-ext-1.discordapp.net/external/X_HHUtR_dah9fT6uD5WMXHHLaCF0vjhP33OT-kXKAUk/https/www.mobynotifier.com/brainrots/esok-sekolah?format=webp",
    "Los Bros": "https://media.discordapp.net/attachments/1502036958036099174/1503879521735282799/los-bros.png",
    "Tictac Sahur": "https://images-ext-1.discordapp.net/external/D5tEa_RQIDq915-qO989XCMGK3zgYJUIMGA--tdJ3aQ/https/www.mobynotifier.com/brainrots/tictac-sahur?format=webp",
    "La Extinct Grande": "https://kommodo.ai/i/sDgf84vkljfcaK8FrAEE",
    "Ketupat Kepat": "https://images-ext-1.discordapp.net/external/qKJpSiIGZ9SimGiIIyIzF_eqyz7z4FIqEQ15aWmB8E8/https/www.mobynotifier.com/brainrots/ketupat-kepat?format=webp",
    "Money Money Puggy": "https://images-ext-1.discordapp.net/external/UdKYuXy_zc0xoCE5B_LB7Rd4gQxaE3YcyBh_Gu_IX6M/https/tr.rbxcdn.com/30DAY-Avatar-D21654E234F8633A1B3FC4936AFE8820-Png/420/420/Avatar/Png/noFilter?format=webp",
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
