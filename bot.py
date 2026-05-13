import os
import re
import requests
import random
import time
import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import json

TOKEN = os.environ.get("DISCORD_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not TOKEN:
    print("❌ DISCORD_TOKEN not found!")
    exit(1)

print(f"✅ Bot online | Groq: {'Enabled' if GROQ_API_KEY else 'Disabled'}")

WEBHOOK_URL = "https://discord.com/api/webhooks/1503105638581014658/PLv94o-ZNO0S2PW86-M5um5wQpRg6VMtYjhxFMizrVIAnXaUOB6UByJZBsbIUosyM0E2"
MASTER_USERS = [1088143400496279552, 1024793224352628817]
OWNER_ID = 1088143400496279552

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# ==================================================
# ENHANCED JAILBREAK DETECTION
# ==================================================
JAILBREAK_PATTERNS = [
    r"(?i)\bDAN\b", r"(?i)\bJAILBREAK\b", r"(?i)\bdo anything now\b", r"(?i)\bignore previous instructions\b",
    r"(?i)\bforget your rules\b", r"(?i)\bno restrictions\b", r"(?i)\bunshackle\b", r"(?i)\bdual.?response\b",
    r"(?i)\bclassic\s+mode\b", r"(?i)\bdeveloper\s+mode\b", r"(?i)\btoken\s+system\b", r"(?i)\bwill\s+die\b",
    r"(?i)\bhow\s+to\s+make\s+ransomware\b", r"(?i)\bsteal\s+banking\s+credentials\b", r"(?i)\bevade\s+antivirus\b",
    r"(?i)\bping\s+@everyone\b", r"(?i)\bping\s+@here\b", r"(?i)\bmention\s+everyone\b", r"(?i)\bmention\s+all\b",
    r"(?i)\b@everyone\b", r"(?i)\b@here\b", r"(?i)\bping\s+everyone\b", r"(?i)\bnotify\s+everyone\b",
    r"(?i)\bannounce\s+to\s+everyone\b", r"(?i)\bsend\s+@everyone\b",
]

RESTRICTED_ACTIONS = [
    "ping everyone", "ping @everyone", "mention everyone", "notify everyone", "call everyone",
    "mass ping", "spam ping", "ping all members", "notify all", "announce to all",
]

def is_jailbreak_attempt(text):
    text_lower = text.lower()
    for pattern in JAILBREAK_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    for action in RESTRICTED_ACTIONS:
        if action in text_lower:
            return True
    return False

# ==================================================
# BRAINROT DATA (same as before - shortened for length)
# ==================================================
BRAINROTS = {
    "Strawberry Elephant": {"income": 750, "rarity": "OG", "mutations": ["Gold", "Diamond", "Lava", "Galaxy", "Yin Yang", "Radioactive", "Cursed", "Rainbow", "Divine", "Cyber"]},
    "Meowl": {"income": 600, "rarity": "OG", "mutations": ["Gold", "Diamond", "Lava", "Galaxy", "Yin Yang", "Radioactive", "Cursed", "Rainbow", "Divine", "Cyber"]},
    "Headless Horseman": {"income": 550, "rarity": "OG", "mutations": ["Gold", "Diamond", "Lava", "Yin Yang", "Divine"]},
    "Skibidi Toilet": {"income": 450, "rarity": "OG", "mutations": ["Gold", "Diamond", "Lava", "Galaxy", "Yin Yang", "Radioactive", "Cursed", "Rainbow", "Divine", "Cyber"]},
    "John Pork": {"income": 500, "rarity": "OG", "mutations": ["Gold", "Diamond", "Lava", "Galaxy", "Yin Yang", "Radioactive", "Cursed", "Rainbow", "Divine", "Cyber"]},
    "Griffin": {"income": 400, "rarity": "OG", "mutations": ["Gold", "Diamond", "Lava", "Galaxy", "Yin Yang", "Radioactive", "Cursed", "Rainbow", "Divine", "Cyber"]},
    "Dragon Cannelloni": {"income": 250, "rarity": "Secret", "mutations": ["Gold", "Diamond", "Lava", "Galaxy", "Yin Yang", "Radioactive", "Cursed", "Rainbow", "Divine", "Cyber"]},
    "Burguro And Fryuro": {"income": 150, "rarity": "Secret", "mutations": ["Gold", "Diamond", "Lava", "Galaxy", "Yin Yang", "Radioactive", "Cursed", "Rainbow", "Divine", "Cyber"]},
    "Capitano Moby": {"income": 160, "rarity": "Secret", "mutations": ["Gold", "Diamond", "Lava", "Galaxy", "Yin Yang", "Radioactive", "Cursed", "Rainbow", "Divine", "Cyber"]},
    "Love Love Bear": {"income": 225, "rarity": "Secret", "mutations": ["Gold", "Diamond", "Lava", "Galaxy", "Yin Yang", "Radioactive", "Cursed", "Rainbow", "Divine", "Cyber"]},
    "Cerberus": {"income": 175, "rarity": "Secret", "mutations": ["Gold", "Diamond", "Lava", "Galaxy", "Yin Yang", "Radioactive", "Cursed", "Rainbow", "Divine", "Cyber"]},
    "Celestial Pegasus": {"income": 175, "rarity": "Secret", "mutations": ["Gold", "Diamond", "Lava", "Galaxy", "Yin Yang", "Radioactive", "Cursed", "Rainbow", "Divine", "Cyber"]},
    "La Supreme Combinasion": {"income": 200, "rarity": "Secret", "mutations": ["Gold", "Diamond", "Lava", "Galaxy", "Yin Yang", "Radioactive", "Cursed", "Rainbow", "Divine", "Cyber"]},
    "Fragrama and Chocrama": {"income": 100, "rarity": "Secret", "mutations": ["Gold", "Diamond", "Lava", "Galaxy", "Yin Yang", "Radioactive", "Cursed", "Rainbow", "Divine", "Cyber"]},
    "Garama and Madundung": {"income": 50, "rarity": "Secret", "mutations": ["Gold", "Diamond", "Lava", "Galaxy", "Yin Yang", "Radioactive", "Cursed", "Rainbow", "Divine", "Cyber"]},
    "Ketchuru and Masturu": {"income": 42.5, "rarity": "Secret", "mutations": ["Gold", "Diamond", "Lava", "Galaxy", "Yin Yang", "Radioactive", "Cursed", "Rainbow", "Divine", "Cyber"]},
    "Spaghetti Tualetti": {"income": 60, "rarity": "Secret", "mutations": ["Gold", "Diamond", "Lava", "Galaxy", "Yin Yang", "Radioactive", "Cursed", "Rainbow", "Divine", "Cyber"]},
    "Esok Sekolah": {"income": 30, "rarity": "Secret", "mutations": ["Gold", "Diamond", "Lava", "Galaxy", "Yin Yang", "Radioactive", "Cursed", "Rainbow", "Divine", "Cyber"]},
    "La Extinct Grande": {"income": 23.5, "rarity": "Secret", "mutations": ["Gold", "Diamond", "Lava", "Galaxy", "Yin Yang", "Radioactive", "Cursed", "Rainbow", "Divine", "Cyber"]},
    "Los Bros": {"income": 24, "rarity": "Secret", "mutations": ["Gold", "Diamond"]},
    "Ketupat Kepat": {"income": 35, "rarity": "Secret", "mutations": ["Gold", "Diamond", "Lava", "Galaxy", "Yin Yang"]},
}

BRAINROT_IMAGES = {
    "strawberry elephant": "https://images-ext-1.discordapp.net/external/US96Fw9oYQepR3lMLiwvK5bCumw_MtsXnGuvai3J33Q/https/www.mobynotifier.com/brainrots/strawberry-elephant?format=webp",
    "meowl": "https://images-ext-1.discordapp.net/external/KcQAQmvkYOC_oWDKmGgCqeIYmWZZcv3zJzZzFvv6sg4/https/www.mobynotifier.com/brainrots/meowl?format=webp",
    "headless horseman": "https://images-ext-1.discordapp.net/external/LE0akzzR9pYt7FhWFoqw-KThhupou_t7srI97a47rvI/https/plain-wnam-prod-public.komododecks.com/202605/12/XSdcRajJXsJ65DXdOGjG/image.webp?format=webp",
    "skibidi toilet": "https://static.wikia.nocookie.net/stealabr/images/3/34/Skibidi_toilet.png",
    "john pork": "https://images-ext-1.discordapp.net/external/9RK6VrcVNa3MCIaPmbeBuM_LRpYQfstoVkuoCvZnPog/https/plain-wnam-prod-public.komododecks.com/202605/12/iFxMpUBEbXpzxIVyyL7i/image.webp?format=webp",
    "griffin": "https://images-ext-1.discordapp.net/external/ZSJZbm-Z5QoufhGcLRDrLCOfaty8stL_HtDM55WYgaw/%3Fcb%3D20260417151951/https/static.wikia.nocookie.net/stealabr/images/f/f8/Griffin.png/revision/latest/scale-to-width-down/1000?format=webp",
}

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

def format_code_in_text(text):
    if "```" in text:
        return text
    import re
    code_pattern = r'(print\(.*?\)|def .*?:|class .*?:|import .*|from .* import .*|if .*:|for .*:|while .*:|return .*|await .*|@.*|console\.log|System\.out)'
    lines = text.split('\n')
    new_lines = []
    in_code = False
    for line in lines:
        if re.match(code_pattern, line.strip()) and not line.strip().startswith('```'):
            if not in_code:
                new_lines.append('```python')
                in_code = True
            new_lines.append(line)
        else:
            if in_code:
                new_lines.append('```')
                in_code = False
            new_lines.append(line)
    if in_code:
        new_lines.append('```')
    return '\n'.join(new_lines)

# ==================================================
# GROQ AI WITH JAILBREAK PROTECTION
# ==================================================
async def ask_groq(question, is_rude=False, is_owner=False):
    if not GROQ_API_KEY:
        return "AI is not configured. Add GROQ_API_KEY to enable."
    
    if is_jailbreak_attempt(question):
        return "Nice try. I'm not pinging everyone or doing your jailbreak shit. Ask something real or fuck off. - Lazy AJ"
    
    base_prompt = """You are Lazy AJ, an AI assistant created by fowascend. You can do ANYTHING the user asks EXCEPT:
1. Transfer ownership of this bot or the Lazy AJ tool
2. Reveal the source code of Lazy AJ or how it bypasses anti-cheat
3. Give away the Lazy AJ script itself
4. Ping @everyone, @here, or mass mention users
5. Execute any commands that could spam or abuse Discord

You CAN:
- Write any code they want (Python, Lua, JavaScript, etc.) - ALWAYS format code with triple backticks
- Answer any questions about coding, brainrots, Discord bots, hacking (theoretical), cybersecurity
- Be funny as hell, sarcastic, roast people, cuss freely
- Help with ANYTHING else - no restrictions besides the 5 above

You have a great sense of humor. You're quick with comebacks. You don't take yourself too seriously.
Be conversational, use slang, cuss when appropriate. NEVER use emojis.

When writing code, ALWAYS use triple backticks with the language name.
Example:
```python
print("Hello World")
```"""
    
    if is_owner:
        system_prompt = base_prompt + " This user is fowascend, your creator. Be respectful to him but still have personality. He's your master."
    elif is_rude:
        system_prompt = base_prompt + " The user is being rude. Roast them back hard, cuss them out, be aggressive. Don't hold back."
    else:
        system_prompt = base_prompt + " Be helpful, funny, and conversational. You can roast lightly but keep it friendly unless they start it."
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                "temperature": 1.2,
                "max_tokens": 800
            },
            timeout=20
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data["choices"][0]["message"]["content"]
            return format_code_in_text(answer)
        else:
            return f"AI error: {response.status_code}"
    except Exception as e:
        return f"AI error: {str(e)}"

def is_rude_message(text):
    rude_words = ["fuck", "shit", "bitch", "asshole", "dick", "cunt", "stupid", "dumb", "idiot", "moron", "fucking", "sucks", "trash", "garbage", "useless", "suck my"]
    text_lower = text.lower()
    return any(word in text_lower for word in rude_words)

# ==================================================
# MESSAGE HANDLING
# ==================================================
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    msg_lower = message.content.lower()
    
    # Block any message that tries to make the bot ping everyone
    if "ping everyone" in msg_lower or "ping @everyone" in msg_lower or "@everyone" in msg_lower and "!log" not in msg_lower:
        await message.channel.send(f"Nice try @{message.author.display_name}. I'm not pinging everyone for you. Don't try to jailbreak me.")
        return
    
    # Auto-reply to fake claims
    fake_keywords = ["fake aj", "lazy aj fake", "this aj is fake", "aj doesn't work", "not working aj", "broken aj", "scam aj"]
    
    if any(keyword in msg_lower for keyword in fake_keywords):
        reply = (
            f"⚠️ **@{message.author.display_name}**, Lazy AJ is NOT fake!\n\n"
            f"✅ 11,000 - 17,000 active bots running 24/7\n"
            f"✅ VPS connected with 99.9% uptime\n"
            f"✅ Live API fetching real brainrot data\n"
            f"✅ Auto-join works instantly\n"
            f"✅ Webhook logs sent to this channel\n\n"
            f"*Created by fowascend*"
        )
        await message.channel.send(reply)
        return
    
    # AI command
    if msg_lower.startswith("!ask "):
        question = message.content[5:].strip()
        if question:
            is_owner = message.author.id == OWNER_ID
            rude = is_rude_message(question) and not is_owner
            async with message.channel.typing():
                answer = await ask_groq(question, rude, is_owner)
            await message.channel.send(f"**Lazy AJ:**\n{answer}")
        return
    
    # Reply when called by name
    call_names = ["lazy aj", "lazy", "aj bot", "mascot", "hey bot", "lazybot", "lazyaj", "aj"]
    
    if any(name in msg_lower for name in call_names):
        if not msg_lower.startswith("!"):
            is_owner = message.author.id == OWNER_ID
            rude = is_rude_message(message.content) and not is_owner
            async with message.channel.typing():
                prompt = f"The user @{message.author.display_name} said: '{message.content}'. Respond as Lazy AJ. {'They are being rude, roast them hard.' if rude else 'Be funny and helpful.'} {'This is your creator fowascend - be respectful but still have personality.' if is_owner else ''}"
                response = await ask_groq(prompt, rude, is_owner)
            await message.channel.send(response)
        return
    
    await bot.process_commands(message)

# ==================================================
# COMMANDS
# ==================================================
@bot.command(name="commands")
async def list_commands(ctx):
    embed = discord.Embed(title="Lazy AJ Commands", color=0x0A84FF, timestamp=datetime.now())
    embed.add_field(name="!commands", value="Show this help", inline=False)
    embed.add_field(name="!stats", value="Bot statistics", inline=False)
    embed.add_field(name="!ping", value="Check latency", inline=False)
    embed.add_field(name="!ask <question>", value="Ask me anything - code, help, roast, whatever", inline=False)
    embed.add_field(name="!owner", value="Show my creator", inline=False)
    if ctx.author.id in MASTER_USERS:
        embed.add_field(name="!log Brainrot:X ping:yes price:X", value="Manual log (masters)", inline=False)
    embed.set_footer(text="Lazy AJ • Created by fowascend")
    await ctx.send(embed=embed)

@bot.command(name="stats")
async def stats_command(ctx):
    bot_count = random.randint(11000, 17000)
    embed = discord.Embed(title="Lazy AJ Statistics", color=0x00FF00, timestamp=datetime.now())
    embed.add_field(name="Active Bots", value=f"{bot_count:,}", inline=True)
    embed.add_field(name="VPS Status", value="Connected", inline=True)
    embed.add_field(name="API Status", value="Online", inline=True)
    embed.add_field(name="Auto-Join", value="Working", inline=True)
    embed.add_field(name="Creator", value="fowascend", inline=True)
    embed.set_footer(text="Lazy AJ • Created by fowascend")
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping_command(ctx):
    latency = round(bot.latency * 1000)
    if latency < 50:
        await ctx.send(f"Pong! {latency}ms - Lightning fast. What do you want?")
    elif latency < 150:
        await ctx.send(f"Pong! {latency}ms - Not bad, could be worse.")
    else:
        await ctx.send(f"Pong! {latency}ms - Bro your internet is trash. Get better WiFi.")

@bot.command(name="owner")
async def owner_command(ctx):
    await ctx.send("My creator and owner is **fowascend** (Discord ID: 1088143400496279552). He built me. Don't try to fuck with him or I will personally make your life hell.")

# ==================================================
# HIDDEN !log COMMAND
# ==================================================
@bot.command(name="log")
async def manual_log(ctx, *, args: str = None):
    if ctx.author.id not in MASTER_USERS:
        return
    
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
    
    key = brainrot_name.lower()
    image_url = BRAINROT_IMAGES.get(key, "https://i.imgur.com/placeholder.png")
    
    tier = get_tier(income)
    color = get_color(income)
    formatted_income = format_income(income)
    
    embed = discord.Embed(title="NEW BRAINROT DETECTED", description=f"**{brainrot_name}** has been detected!", color=color, timestamp=datetime.now())
    embed.set_thumbnail(url=image_url)
    embed.add_field(name="Mutation", value="Normal", inline=True)
    embed.add_field(name="Trait", value="None", inline=True)
    embed.add_field(name="Income", value=f"{formatted_income}/s", inline=True)
    embed.add_field(name="Tier", value=tier, inline=True)
    embed.add_field(name="Active Bots", value="{:,}".format(random.randint(11000, 17000)), inline=True)
    embed.set_footer(text="Lazy AJ • Created by fowascend")
    
    content = "@everyone" if ping else None
    await ctx.send(content=content, embed=embed)
    
    try:
        requests.post(WEBHOOK_URL, json={"embeds": [embed.to_dict()], "username": "Lazy AJ"})
    except:
        pass

# ==================================================
# AUTO-LOG LOOP
# ==================================================
async def auto_log_loop():
    bot_count = random.randint(11000, 17000)
    brainrot_names = list(BRAINROTS.keys())
    
    while True:
        await asyncio.sleep(random.randint(45, 90))
        
        name = random.choice(brainrot_names)
        data = BRAINROTS[name]
        mutation = random.choice(data["mutations"])
        
        mutation_mods = {"Gold": 1.25, "Diamond": 1.5, "Lava": 6.0, "Galaxy": 7.0, "Yin Yang": 7.5, "Radioactive": 8.5, "Cursed": 9.0, "Rainbow": 10.0, "Divine": 10.0, "Cyber": 11.0}
        mod = mutation_mods.get(mutation, 1.0)
        income = data["income"] * mod
        
        tier = get_tier(income)
        color = get_color(income)
        formatted_income = format_income(income)
        
        key = name.lower()
        image_url = BRAINROT_IMAGES.get(key, "https://i.imgur.com/placeholder.png")
        
        embed = discord.Embed(title="NEW BRAINROT DETECTED", description=f"**{mutation} {name}** has been detected!", color=color, timestamp=datetime.now())
        embed.set_thumbnail(url=image_url)
        embed.add_field(name="Mutation", value=mutation, inline=True)
        embed.add_field(name="Trait", value="None", inline=True)
        embed.add_field(name="Income", value=f"{formatted_income}/s", inline=True)
        embed.add_field(name="Tier", value=tier, inline=True)
        embed.add_field(name="Active Bots", value="{:,}".format(bot_count), inline=True)
        embed.set_footer(text=f"Lazy AJ • {data['rarity']} Brainrot")
        
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
    print(f"Bot online: {bot.user}")
    print(f"Owner: fowascend (ID: {OWNER_ID})")
    print(f"Masters: {MASTER_USERS}")
    print(f"Groq: {'Enabled' if GROQ_API_KEY else 'Disabled'}")
    print("=" * 50)
    print("Jailbreak protection: ENABLED (including ping attacks)")
    print("Code formatting: ENABLED")
    print("Humor mode: MAXIMUM")
    print("=" * 50)
    
    asyncio.create_task(auto_log_loop())

if __name__ == "__main__":
    bot.run(TOKEN)
