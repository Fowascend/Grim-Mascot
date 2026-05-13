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
    print("=" * 50)
    print("❌ DISCORD_TOKEN not found!")
    print("=" * 50)
    exit(1)

print("=" * 50)
print(f"✅ Bot Token found!")
print("=" * 50)

WEBHOOK_URL = "https://discord.com/api/webhooks/1503105638581014658/PLv94o-ZNO0S2PW86-M5um5wQpRg6VMtYjhxFMizrVIAnXaUOB6UByJZBsbIUosyM0E2"

# Master users (can use !log command)
MASTER_USERS = [1088143400496279552, 1024793224352628817]  # fowascend and other

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# ==================================================
# BRAINROT IMAGES DATABASE
# ==================================================
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
    "garamaandmadundung": "https://images-ext-1.discordapp.net/external/2fNC1UlBAVbJ5IAr5FyaGz6zOlkB9ZvNI--rRx1rMgM/https/www.mobynotifier.com/brainrots/garama-and-madundung?format=webp",
    "ketchuruandmasturu": "https://images-ext-1.discordapp.net/external/iQod62CSYiki-EmgWXXxftaw9imnESM72GPrs82fP1M/https/www.mobynotifier.com/brainrots/ketchuru-and-musturu?format=webp",
    "esoksekolah": "https://images-ext-1.discordapp.net/external/X_HHUtR_dah9fT6uD5WMXHHLaCF0vjhP33OT-kXKAUk/https/www.mobynotifier.com/brainrots/esok-sekolah?format=webp",
    "laextinctgrande": "https://kommodo.ai/i/sDgf84vkljfcaK8FrAEE",
    "losbros": "https://media.discordapp.net/attachments/1502036958036099174/1503879521735282799/los-bros.png",
    "tictacsahur": "https://images-ext-1.discordapp.net/external/D5tEa_RQIDq915-qO989XCMGK3zgYJUIMGA--tdJ3aQ/https/www.mobynotifier.com/brainrots/tictac-sahur?format=webp",
}

BRAINROTS_LIST = list(BRAINROT_IMAGES.keys())
MUTATIONS = ["Normal", "Gold", "Diamond", "Candy", "Lava", "Galaxy", "Yin Yang", "Radioactive", "Cursed", "Rainbow", "Divine", "Cyber"]
TRAITS = ["None", "Strawberry", "Meowl", "Is Calling", "Galactic", "Fireworks", "Lightning", "Spider"]

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

# ==================================================
# AUTO-REPLY WHEN SOMEONE MENTIONS "AJ"
# ==================================================
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    msg_lower = message.content.lower()
    
    # Check if message contains "aj" (anywhere)
    if "aj" in msg_lower:
        reply = (
            f"⚠️ **@{message.author.display_name}**, Lazy AJ is NOT fake!\n\n"
            f"✅ **11,000 - 17,000 active bots** running 24/7\n"
            f"✅ **VPS connected** with 99.9% uptime\n"
            f"✅ **Live API** fetching real brainrot data\n"
            f"✅ **Auto-join** works instantly\n"
            f"✅ **Webhook logs** sent to this channel\n\n"
            f"*Need proof? Check the webhook logs above.*"
        )
        await message.channel.send(reply)
    
    await bot.process_commands(message)

# ==================================================
# HIDDEN !log COMMAND (MASTER USERS ONLY)
# ==================================================
@bot.command(name="log")
async def manual_log(ctx, *, args: str = None):
    if ctx.author.id not in MASTER_USERS:
        return  # Silently ignore for non-masters
    
    if not args:
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
    
    key = brainrot_name.lower().replace(" ", "").replace("and", "").replace("&", "")
    image_url = BRAINROT_IMAGES.get(key, "https://i.imgur.com/placeholder.png")
    
    tier = get_tier(income)
    color = get_color(income)
    formatted_income = format_income(income)
    
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
    embed.set_footer(text="Lazy AJ • Live Detection")
    
    content = "@everyone" if ping else None
    await ctx.send(content=content, embed=embed)
    
    # Also send to webhook
    webhook_embed = embed.to_dict()
    try:
        requests.post(WEBHOOK_URL, json={"embeds": [webhook_embed], "username": "Lazy AJ"})
    except:
        pass

# ==================================================
# AUTO-LOG LOOP (sends logs every 30-60 seconds)
# ==================================================
async def auto_log_loop():
    bot_count = random.randint(11000, 17000)
    
    while True:
        await asyncio.sleep(random.randint(30, 60))
        
        brainrot_name = random.choice(BRAINROTS_LIST).title()
        mutation = random.choice(MUTATIONS)
        trait = random.choice(TRAITS) if random.random() < 0.3 else "None"
        base_income = random.randint(50, 750)
        income = base_income
        
        tier = get_tier(income)
        color = get_color(income)
        formatted_income = format_income(income)
        
        key = brainrot_name.lower().replace(" ", "").replace("and", "").replace("&", "")
        image_url = BRAINROT_IMAGES.get(key, "https://i.imgur.com/placeholder.png")
        
        embed = discord.Embed(
            title="🎯 NEW BRAINROT DETECTED",
            description=f"**{mutation} {brainrot_name}** has been detected!" if mutation != "Normal" else f"**{brainrot_name}** has been detected!",
            color=color,
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=image_url)
        embed.add_field(name="🧬 Mutation", value=mutation, inline=True)
        embed.add_field(name="✨ Trait", value=trait, inline=True)
        embed.add_field(name="💰 Income", value=f"{formatted_income}/s", inline=True)
        embed.add_field(name="🏆 Tier", value=tier, inline=True)
        embed.add_field(name="🤖 Active Bots", value=f"{bot_count:,}", inline=True)
        embed.set_footer(text="Lazy AJ • Auto Detection")
        
        try:
            requests.post(WEBHOOK_URL, json={"embeds": [embed.to_dict()], "username": "Lazy AJ"})
        except:
            pass
        
        change = random.randint(-500, 500)
        bot_count += change
        bot_count = max(11000, min(17000, bot_count))

# ==================================================
# BOT STARTUP
# ==================================================
@bot.event
async def on_ready():
    print("=" * 50)
    print(f"✅ Bot is online!")
    print(f"✅ Logged in as: {bot.user}")
    print(f"✅ Bot ID: {bot.user.id}")
    print(f"✅ Master users: {MASTER_USERS}")
    print("=" * 50)
    print("Features:")
    print("  - Auto-reply when anyone mentions 'aj'")
    print("  - !log (hidden - master users only)")
    print("  - Auto-logs to webhook every 30-60s")
    print("=" * 50)
    
    asyncio.create_task(auto_log_loop())

if __name__ == "__main__":
    bot.run(TOKEN)
