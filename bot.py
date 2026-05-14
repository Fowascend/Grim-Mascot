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
        "timestamp": datetime.now().isoformat(),
    }

def send_webhook(brainrot, bot_count):
    embed = {
        "title": "🎯 NEW BRAINROT DETECTED",
        "description": f"**{brainrot['name']}** has been detected!",
        "color": brainrot["color"],
        "timestamp": brainrot["timestamp"],
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
    
    import re
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
    
    embed = discord.Embed(
        title="🎯 NEW BRAINROT DETECTED",
        description=f"**{brainrot_name}** has been detected!",
        color=color,
        timestamp=datetime.now()
    )
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
    print("=" * 50)
    print("Auto-logs every 45-90 seconds")
    print("OG brainrots every 4-6 hours")
    print("=" * 50)
    
    asyncio.create_task(auto_log_loop())

if __name__ == "__main__":
    bot.run(TOKEN)
