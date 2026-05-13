import requests
import random
import time
import discord
from discord.ext import commands
from datetime import datetime

# Discord Bot Token (set this in your environment variables)
TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your bot token

# Webhook URL for automatic logs
WEBHOOK_URL = "https://discord.com/api/webhooks/1503105638581014658/PLv94o-ZNO0S2PW86-M5um5wQpRg6VMtYjhxFMizrVIAnXaUOB6UByJZBsbIUosyM0E2"

# Allowed user ID (only this user can use !log command)
ALLOWED_USER_ID = 1088143400496279552

# Setup Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Brainrot images database
BRAINROT_IMAGES = {
    "strawberryelephant": "https://images-ext-1.discordapp.net/external/US96Fw9oYQepR3lMLiwvK5bCumw_MtsXnGuvai3J33Q/https/www.mobynotifier.com/brainrots/strawberry-elephant?format=webp",
    "meowl": "https://images-ext-1.discordapp.net/external/KcQAQmvkYOC_oWDKmGgCqeIYmWZZcv3zJzZzFvv6sg4/https/www.mobynotifier.com/brainrots/meowl?format=webp",
    "headlesshorseman": "https://images-ext-1.discordapp.net/external/LE0akzzR9pYt7FhWFoqw-KThhupou_t7srI97a47rvI/https/plain-wnam-prod-public.komododecks.com/202605/12/XSdcRajJXsJ65DXdOGjG/image.webp?format=webp",
    "skibiditoilet": "https://static.wikia.nocookie.net/stealabr/images/3/34/Skibidi_toilet.png",
    "johnpork": "https://images-ext-1.discordapp.net/external/9RK6VrcVNa3MCIaPmbeBuM_LRpYQfstoVkuoCvZnPog/https/plain-wnam-prod-public.komododecks.com/202605/12/iFxMpUBEbXpzxIVyyL7i/image.webp?format=webp",
    "griffin": "https://images-ext-1.discordapp.net/external/ZSJZbm-Z5QoufhGcLRDrLCOfaty8stL_HtDM55WYgaw/%3Fcb%3D20260417151951/https/static.wikia.nocookie.net/stealabr/images/f/f8/Griffin.png/revision/latest/scale-to-width-down/1000?format=webp",
    "dragoncannelloni": "https://images-ext-1.discordapp.net/external/X4PlwMzgXd5GkP_hOPxTjThl4yNvY5mGUhiV1iOnHb0/https/www.mobynotifier.com/brainrots/dragon-cannelloni?format=webp",
    "burguroandfryuro": "https://images-ext-1.discordapp.net/external/qVX50l18q9QN8JHBQ5uJq5KvRz5KsHiZv6J7BjhK0cQ/https/www.mobynotifier.com/brainrots/burguro-and-fryuro?format=webp",
    "capitanomoby": "https://images-ext-1.discordapp.net/external/k7fodKUVV7Tr3fLaxkyXXgGUKpuj0fS05fyglkhIM20/https/www.mobynotifier.com/brainrots/capitano-moby?format=webp",
    "loveLoveBear": "https://static.wikia.nocookie.net/stealabr/images/b/bf/Love_Love_Bear.png",
    "cerberus": "https://images-ext-1.discordapp.net/external/NPtLqSPSBZtctUNyMptN6edlsdvC-9nhE7uJUppe5lo/https/www.mobynotifier.com/brainrots/cerberus?format=webp",
    "celestialpegasus": "https://images-ext-1.discordapp.net/external/uQV0Gtw56MrBLMrPHNJHsEL3GHEtQtPtqFd7IC-FxxM/https/www.mobynotifier.com/brainrots/celestial-pegasus?format=webp",
    "lasupremecombinasion": "https://images-ext-1.discordapp.net/external/KQBRtzBT3aoWc6WTjvoOhl2Tf64FvbWhyFW4VWbQGhQ/https/www.mobynotifier.com/brainrots/la-secret-combinasion?format=webp",
    "fragramaandchocrama": "https://images-ext-1.discordapp.net/external/Kln9a8QqTAqtPxqLDid23oNYIC5hYoxb2Wh8Jo1qG60/%3Fcb%3D20251109011733/https/static.wikia.nocookie.net/stealabr/images/5/56/Fragrama.png/revision/latest?format=webp",
    "lacasaboo": "https://images-ext-1.discordapp.net/external/quqyy1a6ddzWi8EeljigfhNgezGLFYhD2LpWiSRMu4g/%3Fcb%3D20260505011532/https/static.wikia.nocookie.net/stealabr/images/d/de/Casa_Booo.png/revision/latest?format=webp",
    "cashorcard": "https://images-ext-1.discordapp.net/external/3--q-u9qc6iESRoNzi3nj5F8aOR0ThZ_FvPHINXrBw4/%3Fcb%3D20260428161300/https/static.wikia.nocookie.net/stealabr/images/2/21/Cash_or_Card.png/revision/latest/scale-to-width-down/1000?format=webp",
    "garamaandmadundung": "https://images-ext-1.discordapp.net/external/2fNC1UlBAVbJ5IAr5FyaGz6zOlkB9ZvNI--rRx1rMgM/https/www.mobynotifier.com/brainrots/garama-and-madundung?format=webp",
    "ketchuruandmasturu": "https://images-ext-1.discordapp.net/external/iQod62CSYiki-EmgWXXxftaw9imnESM72GPrs82fP1M/https/www.mobynotifier.com/brainrots/ketchuru-and-musturu?format=webp",
    "spaghettitualetti": "https://images-ext-1.discordapp.net/external/yoOCxZMRDwqYzFcsYPY5GX2WY2wK4FvGgqB72P1VCV8/https/www.mobynotifier.com/brainrots/spaghetti-tualetti?format=webp",
    "esoksekolah": "https://images-ext-1.discordapp.net/external/X_HHUtR_dah9fT6uD5WMXHHLaCF0vjhP33OT-kXKAUk/https/www.mobynotifier.com/brainrots/esok-sekolah?format=webp",
    "laextinctgrande": "https://kommodo.ai/i/sDgf84vkljfcaK8FrAEE",
    "losbros": "https://media.discordapp.net/attachments/1502036958036099174/1503879521735282799/los-bros.png",
    "ketupatkepat": "https://images-ext-1.discordapp.net/external/qKJpSiIGZ9SimGiIIyIzF_eqyz7z4FIqEQ15aWmB8E8/https/www.mobynotifier.com/brainrots/ketupat-kepat?format=webp",
    "tangtangkeletang": "https://images-ext-1.discordapp.net/external/4qWYUdmCoa0zhqxH2MKwV7Or5U9Xif8yw-AB_Gy5Lig/https/www.mobynotifier.com/brainrots/tang-tang-keletang?format=webp",
    "tictacsahur": "https://images-ext-1.discordapp.net/external/D5tEa_RQIDq915-qO989XCMGK3zgYJUIMGA--tdJ3aQ/https/www.mobynotifier.com/brainrots/tictac-sahur?format=webp",
    "foxinilanternini": "https://static.wikia.nocookie.net/stealabr/images/4/41/Foxini_Lanternini.png",
    "roseyandteddy": "https://static.wikia.nocookie.net/stealabr/images/9/9b/Rosey_and_Teddy.png",
    "tralaledon": "https://images-ext-1.discordapp.net/external/_bBDdfMFPbTdCGnkfiz3yzvtNwqz0P4iVOnTlxFfaME/%3Fcb%3D20250909171639/https/static.wikia.nocookie.net/stealabr/images/7/79/Brr_Brr_Patapem.png/revision/latest?format=webp",
    "spookyandpumpky": "https://static.wikia.nocookie.net/stealabr/images/d/d6/Spookypumpky.png/revision/latest?cb=20251012023638",
    "loscombinasionas": "https://images-ext-1.discordapp.net/external/e8NoB0fRt0X0W7aHmWJIQwC2IXb_dHLlEzY4lqhYjSc/https/www.mobynotifier.com/brainrots/los-combinasionas?format=webp",
    "loshotspotsitos": "https://images-ext-1.discordapp.net/external/MsbU8Cx2x5x0Uqz0KiKgYQXeugojQ7SQBjg0uY8Doh0/%3Fcb%3D20251226204212/https/static.wikia.nocookie.net/stealabr/images/6/69/Loshotspotsitos.png/revision/latest?format=webp",
    "moneymoneypuggy": "https://images-ext-1.discordapp.net/external/UdKYuXy_zc0xoCE5B_LB7Rd4gQxaE3YcyBh_Gu_IX6M/https/tr.rbxcdn.com/30DAY-Avatar-D21654E234F8633A1B3FC4936AFE8820-Png/420/420/Avatar/Png/noFilter?format=webp",
    "lospuggies": "https://images-ext-1.discordapp.net/external/xSRo3cOgaMz_3bOvc-uxwnvdHvBbEI91-5o129qDE1A/%3Fcb%3D20251109012744/https/static.wikia.nocookie.net/stealabr/images/c/c8/LosPuggies2.png/revision/latest?format=webp",
    "nuclearodinosauro": "https://images-ext-1.discordapp.net/external/wO_VfzWxp76PImVCn4peFiARwLyzlEbzI8SqaKEtXio/%3Fcb%3D20260328003025/https/static.wikia.nocookie.net/stealabr/images/b/b5/Nuclearo_Dinossauro.png/revision/latest/scale-to-width-down/1000?format=webp",
    "hydradragoncannelloni": "https://images-ext-1.discordapp.net/external/xfvoBJm_MpWzP2D-q90AcpQ4EJnYcfyV763moAfMtYc/https/steal-a-brainrot.wiki/wp-content/uploads/2026/01/Steal-A-Brainrot-Wiki-HYDRA-DRAGON-Icon-.png?format=webp",
    "dragonGingerini": "https://images-ext-1.discordapp.net/external/3puIUz4htLMUuD3hL5u4N9tIlLdxj2Gi2AVuJgtei9o/https/freebrainrots.com/assets/images/brainrots/roitems/dragon-gingerini.png?format=webp",
    "cookiandmilki": "https://steal-a-brainrot.wiki/wp-content/uploads/2025/11/Steal-a-Brainrot-Wiki-Cooki-and-Milki-Icon-300x300.png",
}

MUTATIONS = [
    {"name": "Normal", "mod": 0.0, "chance": 60},
    {"name": "Gold", "mod": 0.25, "chance": 15},
    {"name": "Diamond", "mod": 0.5, "chance": 10},
    {"name": "Candy", "mod": 3.0, "chance": 3},
    {"name": "Lava", "mod": 5.0, "chance": 3},
    {"name": "Galaxy", "mod": 6.0, "chance": 3},
    {"name": "Yin Yang", "mod": 6.5, "chance": 2},
    {"name": "Radioactive", "mod": 7.5, "chance": 1.5},
    {"name": "Cursed", "mod": 8.0, "chance": 1},
    {"name": "Rainbow", "mod": 9.0, "chance": 0.8},
    {"name": "Divine", "mod": 9.0, "chance": 0.8},
    {"name": "Cyber", "mod": 10.0, "chance": 0.5},
]

TRAITS = [
    {"name": "None", "mod": 0.0, "chance": 85},
    {"name": "Strawberry", "mod": 8.0, "chance": 3},
    {"name": "Meowl", "mod": 7.0, "chance": 3},
    {"name": "Is Calling", "mod": 7.5, "chance": 1},
    {"name": "Galactic", "mod": 3.0, "chance": 2},
    {"name": "Fireworks", "mod": 5.0, "chance": 2},
    {"name": "Lightning", "mod": 5.0, "chance": 2},
    {"name": "Spider", "mod": 3.5, "chance": 2},
]

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

def send_webhook(brainrot_name, mutation, trait, income, bot_count):
    formatted = format_income(income)
    color = get_color(income)
    tier = get_tier(income)
    
    display_name = brainrot_name
    if mutation != "Normal":
        display_name = f"{mutation} {display_name}"
    if trait != "None":
        display_name = f"{display_name} ({trait})"
    
    # Get image URL (convert name to key format)
    key = brainrot_name.lower().replace(" ", "").replace("and", "").replace("&", "")
    image_url = BRAINROT_IMAGES.get(key, "https://i.imgur.com/placeholder.png")
    
    embed = {
        "title": "🎯 NEW BRAINROT DETECTED",
        "description": f"**{display_name}** has been detected!",
        "color": color,
        "timestamp": datetime.now().isoformat(),
        "thumbnail": {"url": image_url},
        "fields": [
            {"name": "🧬 Mutation", "value": mutation, "inline": True},
            {"name": "✨ Trait", "value": trait, "inline": True},
            {"name": "💰 Income", "value": f"{formatted}/s", "inline": True},
            {"name": "🏆 Tier", "value": tier, "inline": True},
            {"name": "🤖 Active Bots", "value": f"{bot_count:,}", "inline": True},
        ],
        "footer": {"text": f"Lazy AJ • Brainrot Detection"},
    }
    
    try:
        requests.post(WEBHOOK_URL, json={"embeds": [embed], "username": "Lazy AJ"})
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

# Automatic log loop (same as before)
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

async def auto_log_loop():
    global last_og_time, next_og_interval
    while True:
        now = time.time()
        is_og_time = (now - last_og_time) >= next_og_interval
        
        if is_og_time:
            interval = 1
            last_og_time = now
            next_og_interval = random.randint(14400, 21600)
        else:
            interval = random.randint(30, 60)
        
        await asyncio.sleep(interval)
        
        if is_og_time:
            og_brainrots = ["Strawberry Elephant", "Meowl", "Headless Horseman", "Skibidi Toilet", "John Pork", "Griffin"]
            brainrot_name = random.choice(og_brainrots)
            mutation = "Normal"
            trait = "None"
            income = {"Strawberry Elephant": 750, "Meowl": 600, "Headless Horseman": 550, "Skibidi Toilet": 450, "John Pork": 500, "Griffin": 400}[brainrot_name]
        else:
            brainrot_name = random.choice(list(BRAINROT_IMAGES.keys())).title()
            mutation = random.choice([m["name"] for m in MUTATIONS])
            trait = random.choice([t["name"] for t in TRAITS])
            if random.random() < 0.7:
                trait = "None"
            # Get base income (approximate)
            base_income = random.randint(15, 750)
            if brainrot_name in ["Strawberry Elephant"]:
                base_income = 750
            elif brainrot_name in ["Meowl"]:
                base_income = 600
            elif brainrot_name in ["Headless Horseman", "John Pork"]:
                base_income = 550
            elif brainrot_name in ["Skibidi Toilet"]:
                base_income = 450
            elif brainrot_name in ["Griffin"]:
                base_income = 400
            else:
                base_income = random.randint(15, 300)
            
            mutation_mod = next((m["mod"] for m in MUTATIONS if m["name"] == mutation), 0)
            trait_mod = next((t["mod"] for t in TRAITS if t["name"] == trait), 0)
            income = base_income * (1 + mutation_mod + trait_mod)
        
        current_bots = update_bot_count()
        send_webhook(brainrot_name, mutation, trait, income, current_bots)

# Discord command
@bot.command(name="log")
async def manual_log(ctx, *, args: str = None):
    # Check if user is allowed
    if ctx.author.id != ALLOWED_USER_ID:
        await ctx.send("❌ You don't have permission to use this command.", delete_after=5)
        return
    
    if not args:
        await ctx.send("❌ Usage: `!log Brainrot:Griffin ping:yes price:23B`\nExample: `!log Brainrot:Strawberry Elephant ping:yes price:750M`")
        return
    
    # Parse arguments
    import re
    brainrot_match = re.search(r'Brainrot:([^ ]+)', args, re.IGNORECASE)
    ping_match = re.search(r'ping:(\S+)', args, re.IGNORECASE)
    price_match = re.search(r'price:(\S+)', args, re.IGNORECASE)
    
    if not brainrot_match:
        await ctx.send("❌ Please specify a brainrot: `Brainrot:Name`")
        return
    
    brainrot_name = brainrot_match.group(1).strip()
    ping = ping_match.group(1).lower() == "yes" if ping_match else False
    price_str = price_match.group(1) if price_match else "100M"
    
    # Parse price (e.g., "23B", "750M", "100")
    import re
    price_match_num = re.search(r'([\d.]+)([BMK]?)', price_str.upper())
    if not price_match_num:
        await ctx.send("❌ Invalid price format. Use like: 23B, 750M, 100")
        return
    
    price_value = float(price_match_num.group(1))
    price_unit = price_match_num.group(2)
    
    if price_unit == 'B':
        income = price_value * 1000
    elif price_unit == 'K':
        income = price_value / 1000
    else:
        income = price_value  # Assume millions
    
    # Get image URL
    key = brainrot_name.lower().replace(" ", "").replace("and", "").replace("&", "")
    image_url = BRAINROT_IMAGES.get(key, "https://i.imgur.com/placeholder.png")
    
    # Determine tier and color
    tier = get_tier(income)
    color = get_color(income)
    formatted_income = format_income(income)
    
    # Create embed
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
    embed.add_field(name="🤖 Active Bots", value=f"{bot_count:,}", inline=True)
    embed.set_footer(text="Lazy AJ • Manual Detection")
    
    # Send message with or without ping
    content = "@everyone" if ping else None
    await ctx.send(content=content, embed=embed)
    
    # Also send to webhook
    send_webhook(brainrot_name, "Normal", "None", income, bot_count)
    
    await ctx.send(f"✅ Logged **{brainrot_name}** with {formatted_income}/s!", delete_after=3)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    print(f"✅ Allowed user ID: {ALLOWED_USER_ID}")
    print("✅ Type !log Brainrot:Griffin ping:yes price:23B to use")
    bot.loop.create_task(auto_log_loop())

# Run the bot
if __name__ == "__main__":
    import asyncio
    bot.run(TOKEN)
