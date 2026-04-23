import discord
from discord.ext import commands
import groq
import os
import random
import re
from dotenv import load_dotenv

load_dotenv()

# ========== BOT SETUP ==========
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# ========== OWNER IDs ==========
OWNER_ID_1 = 1088143400496279552  # Fowascend
OWNER_ID_2 = 1039230074525863998  # Artful
OWNER_IDS = [OWNER_ID_1, OWNER_ID_2]

print(f"Bot starting. Owners: {OWNER_IDS}")

# ========== GROQ SETUP ==========
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    print("ERROR: GROQ_API_KEY not found!")
client = groq.Groq(api_key=GROQ_API_KEY)

# ========== VALUE DATABASE ==========
# Base values in La Vacca Saturno Saturnita units
brainrot_values = {
    # OG TIER
    "headless horseman": 75000,
    "headless": 75000,
    "strawberry elephant": 50000,
    "strawberry": 50000,
    "meowl": 25000,
    "skibidi toilet": 25000,
    "skibidi": 25000,
    
    # SECRET TIER
    "love love bear": 13500,
    "dragon gingerini": 8800,
    "dragon cannelloni": 6000,
    "la supreme combinasion": 4600,
    "hydra dragon cannelloni": 4500,
    "signore carapace": 4400,
}

# ========== MUTATIONS ==========
mutations = {
    "cyber": {"mult": 11, "desc": "Futuristic neon blue + circuit patterns. Best in game!", "rarity": "Ultimate"},
    "rainbow": {"mult": 10, "desc": "RGB color cycle. Ultra rare (1% spawn)", "rarity": "Ultimate"},
    "divine": {"mult": 10, "desc": "Yellow/white glow + chance for Halo trait", "rarity": "Event"},
    "cursed": {"mult": 9, "desc": "Dark ethereal glow", "rarity": "Event"},
    "radioactive": {"mult": 8.5, "desc": "Green radioactive glow", "rarity": "Legacy"},
    "yin yang": {"mult": 7.5, "desc": "Black and white contrast", "rarity": "Event"},
    "galaxy": {"mult": 7, "desc": "Purple cosmic space aura", "rarity": "Event"},
    "lava": {"mult": 6, "desc": "Neon orange molten effect", "rarity": "Legacy"},
    "candy": {"mult": 4, "desc": "Pink bubblegum appearance", "rarity": "Legacy"},
    "celestial": {"mult": 4, "desc": "Ethereal white glow", "rarity": "Admin"},
    "bloodrot": {"mult": 2, "desc": "Dark red blood color", "rarity": "Legacy"},
    "diamond": {"mult": 1.5, "desc": "Blue crystalline", "rarity": "Common"},
    "gold": {"mult": 1.25, "desc": "Yellow/golden", "rarity": "Common"},
}

# ========== TRAITS ==========
traits = {
    "strawberry": {"mult": 8, "desc": "Best trait! Strawberry Elephant spawn only"},
    "meowl": {"mult": 7, "desc": "Second best trait. Meowl spawn only"},
    "lightning": {"mult": 6, "desc": "Lightning Galaxy event"},
    "fireworks": {"mult": 6, "desc": "4th of July admin event"},
    "nyan cat": {"mult": 6, "desc": "Nyan invasion admin event"},
    "fire": {"mult": 6, "desc": "Solar event / admin only"},
    "10b": {"mult": 4, "desc": "10 Billion Visits celebration"},
    "bubblegum": {"mult": 4, "desc": "Bubblegum Machine"},
    "comet": {"mult": 3.5, "desc": "Starfall weather or Galactic event"},
    "snowy": {"mult": 3, "desc": "Snow weather"},
    "taco": {"mult": 3, "desc": "Raining Tacos admin event"},
    "rain": {"mult": 2.5, "desc": "Rain weather"},
    "sleepy": {"mult": 0.33, "desc": "÷2! NEGATIVE trait - AVOID!"},
}

# ========== HELPER FUNCTIONS ==========

def calculate_item_value(item_name, quantity=1, mutation=None, trait=None):
    """Calculate total value of an item with optional mutation/trait"""
    item_lower = item_name.lower().strip()
    
    # Get base value
    base_value = None
    for key, value in brainrot_values.items():
        if key in item_lower or item_lower in key:
            base_value = value
            break
    
    if base_value is None:
        return None
    
    # Apply mutation multiplier
    mutation_mult = 1
    if mutation:
        mutation_lower = mutation.lower()
        if mutation_lower in mutations:
            mutation_mult = mutations[mutation_lower]["mult"]
    
    # Apply trait multiplier
    trait_mult = 1
    if trait:
        trait_lower = trait.lower()
        if trait_lower in traits:
            trait_mult = traits[trait_lower]["mult"]
    
    total = base_value * mutation_mult * trait_mult * quantity
    return round(total, 2)

def parse_trade_question(question):
    """Parse natural language trade questions"""
    question_lower = question.lower()
    
    # Pattern: "is X worth Y"
    pattern = r'is\s+(.+?)\s+worth\s+(.+?)\??$'
    match = re.search(pattern, question_lower)
    
    if match:
        left_side = match.group(1).strip()
        right_side = match.group(2).strip()
        
        # Parse left side
        left_parts = left_side.split()
        left_quantity = 1
        left_item = left_side
        
        if left_parts and left_parts[0].isdigit():
            left_quantity = int(left_parts[0])
            left_item = ' '.join(left_parts[1:])
        
        # Parse right side
        right_parts = right_side.split()
        right_quantity = 1
        right_item = right_side
        
        if right_parts and right_parts[0].isdigit():
            right_quantity = int(right_parts[0])
            right_item = ' '.join(right_parts[1:])
        
        return {
            'left': {'item': left_item, 'quantity': left_quantity},
            'right': {'item': right_item, 'quantity': right_quantity}
        }
    
    return None

def compare_trade(left_item, left_qty, right_item, right_qty):
    """Compare two sides of a trade"""
    left_value = calculate_item_value(left_item, left_qty)
    right_value = calculate_item_value(right_item, right_qty)
    
    if left_value is None or right_value is None:
        return None
    
    if left_value > right_value:
        percent = ((left_value - right_value) / right_value) * 100
        return f"❌ **NO** - {left_qty} {left_item} (worth {left_value:,.0f}) is worth **{percent:.0f}% more** than {right_qty} {right_item} (worth {right_value:,.0f}). You would be overpaying!"
    elif right_value > left_value:
        percent = ((right_value - left_value) / left_value) * 100
        return f"✅ **YES** - {left_qty} {left_item} (worth {left_value:,.0f}) is a **GOOD deal** for {right_qty} {right_item} (worth {right_value:,.0f}). You're getting {percent:.0f}% more value!"
    else:
        return f"⚖️ **FAIR TRADE** - Both sides are worth about {left_value:,.0f} each!"

def get_value_info(item_name):
    """Get value info for an item"""
    item_lower = item_name.lower().strip()
    for key, value in brainrot_values.items():
        if key in item_lower or item_lower in key:
            return f"**{item_name}** is worth **{value:,}** La Vacca Saturno Saturnita"
    return None

def get_best_combo():
    """Get best mutation + trait combo"""
    best_mut = max(mutations.items(), key=lambda x: x[1]["mult"])
    best_trait = max(traits.items(), key=lambda x: x[1]["mult"])
    total = best_mut[1]["mult"] * best_trait[1]["mult"]
    return best_mut[0], best_trait[0], total

def handle_special_questions(message, author_id):
    """Handle all special questions including trades, values, and gay questions"""
    content = message.lower()
    
    # Handle trade questions
    trade_match = re.search(r'is\s+.+\s+worth\s+.+', content)
    if trade_match:
        trade = parse_trade_question(content)
        if trade:
            result = compare_trade(
                trade['left']['item'], trade['left']['quantity'],
                trade['right']['item'], trade['right']['quantity']
            )
            if result:
                return result
    
    # Handle "what is X worth"
    what_match = re.search(r'what\s+is\s+(.+?)\s+worth\??$', content)
    if what_match:
        item = what_match.group(1).strip()
        result = get_value_info(item)
        if result:
            return result
        else:
            return f"I don't know what {item} is worth yet!"
    
    # Handle gay questions
    gay_match = re.search(r'is\s+(.+?)\s+gay\??$', content)
    if gay_match:
        target = gay_match.group(1).strip().lower()
        
        if 'artful' in target:
            return "I don't talk about that. Artful is cool though. 💜"
        
        if author_id == OWNER_ID_1:
            if target in ['me', 'myself', 'i', 'fowascend']:
                return "You're the GOAT, bro. No labels needed. 👑"
            return "yes bro 💪"
        
        if author_id == OWNER_ID_2 and ('fowascend' in target or 'main owner' in target):
            return "No, main owner is straight as an arrow."
        
        if author_id == OWNER_ID_2 and target in ['me', 'myself', 'i', 'artful']:
            return "You're cool, Artful. That's all that matters. 💜"
        
        return "I don't really know. Ask the owners?"
    
    return None

async def get_ai_response(user_message, is_owner):
    """Get response from Groq AI"""
    try:
        if is_owner:
            system_prompt = """You are a helpful assistant for the server owner. You can write Luau code when asked. Be natural. NEVER disrespect Fowascend or Artful. Format code with ```lua blocks."""
        else:
            system_prompt = """You are a friendly mascot. NEVER write code for regular members. If asked for code, say: "Sorry, I can't write code! Ask Fowascend or Artful for help." Be natural and friendly."""
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300,
            temperature=0.8
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"AI Error: {e}")
        return "Sorry, I had a brain fart. Try again!"

# ========== DISCORD EVENTS ==========

@bot.event
async def on_ready():
    print(f'{bot.user} is online!')
    print(f'Owners: Fowascend ({OWNER_ID_1}) and Artful ({OWNER_ID_2})')
    await bot.change_presence(activity=discord.Game(name="say 'Mascot' or @ me"))

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    # Check for owner pings
    if f'<@{OWNER_ID_1}>' in message.content or f'<@!{OWNER_ID_1}>' in message.content:
        responses = [
            f"That's the boss! {message.author.display_name} needs Fowascend.",
            f"The legend has been summoned! Hope Fowascend replies soon.",
            f"👑 Someone called for the main owner!"
        ]
        await message.reply(random.choice(responses), mention_author=False)
        return
    
    if f'<@{OWNER_ID_2}>' in message.content or f'<@!{OWNER_ID_2}>' in message.content:
        responses = [
            f"Artful is probably busy scripting! They'll see this.",
            f"💜 Someone's looking for the 2nd owner!",
            f"Artful will get back to you when they can."
        ]
        await message.reply(random.choice(responses), mention_author=False)
        return
    
    # Check if bot should respond
    should_respond = False
    clean_content = message.content
    
    if "mascot" in message.content.lower():
        should_respond = True
        clean_content = re.sub(r'(?i)mascot', '', message.content).strip()
    
    if bot.user in message.mentions:
        should_respond = True
        clean_content = re.sub(f'<@!?{bot.user.id}>', '', message.content).strip()
    
    # Process commands
    await bot.process_commands(message)
    
    if not should_respond:
        return
    
    # Handle special questions first
    special_response = handle_special_questions(message.content, message.author.id)
    if special_response:
        await message.reply(special_response, mention_author=False)
        return
    
    # Get AI response
    async with message.channel.typing():
        is_owner = message.author.id in OWNER_IDS
        response = await get_ai_response(clean_content or "hello", is_owner)
        await message.reply(response, mention_author=False)

# ========== BASIC COMMANDS ==========

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command(name='myid')
async def my_id(ctx):
    if ctx.author.id == OWNER_ID_1:
        await ctx.send(f"Your ID: `{ctx.author.id}` - **FOWASCEND (Main Owner)** 👑")
    elif ctx.author.id == OWNER_ID_2:
        await ctx.send(f"Your ID: `{ctx.author.id}` - **ARTFUL (2nd Owner)** 💜")
    else:
        await ctx.send(f"Your ID: `{ctx.author.id}` - Regular Member")

@bot.command(name='about')
async def about(ctx):
    await ctx.send("I'm the server mascot! I can answer trade questions like 'is 5 meowl worth a headless horseman?' and more!")

# ========== TRADE & VALUE COMMANDS ==========

@bot.command(name='value')
async def value_cmd(ctx, *, item: str):
    """Check the value of an item. Example: !value strawberry elephant"""
    result = get_value_info(item)
    if result:
        await ctx.send(result)
    else:
        await ctx.send(f"I don't know what {item} is worth yet!")

@bot.command(name='trade')
async def trade_cmd(ctx, left: str, right: str):
    """Compare two items. Example: !trade 5 meowl headless horseman"""
    # Parse left and right
    left_parts = left.split()
    left_qty = 1
    left_item = left
    if left_parts and left_parts[0].isdigit():
        left_qty = int(left_parts[0])
        left_item = ' '.join(left_parts[1:])
    
    right_parts = right.split()
    right_qty = 1
    right_item = right
    if right_parts and right_parts[0].isdigit():
        right_qty = int(right_parts[0])
        right_item = ' '.join(right_parts[1:])
    
    result = compare_trade(left_item, left_qty, right_item, right_qty)
    if result:
        await ctx.send(result)
    else:
        await ctx.send("I don't know one of those items! Try `!value` to check what I know.")

# ========== MUTATION & TRAIT COMMANDS ==========

@bot.command(name='mutation')
async def mutation_info(ctx, *, name: str = None):
    """Get info about a mutation. Example: !mutation rainbow"""
    if not name:
        await ctx.send("Usage: `!mutation rainbow` or `!mutation list`")
        return
    
    name_lower = name.lower()
    if name_lower == "list":
        msg = "**📋 Mutations List:**\n"
        for m, data in sorted(mutations.items(), key=lambda x: -x[1]["mult"]):
            msg += f"• **{m.title()}**: {data['mult']}x - {data['desc'][:50]}...\n"
        await ctx.send(msg)
        return
    
    if name_lower in mutations:
        data = mutations[name_lower]
        await ctx.send(f"**{name.title()} Mutation**\n• Multiplier: {data['mult']}x\n• Rarity: {data['rarity']}\n• {data['desc']}")
    else:
        await ctx.send(f"Unknown mutation: {name}. Use `!mutation list` to see all.")

@bot.command(name='trait')
async def trait_info(ctx, *, name: str = None):
    """Get info about a trait. Example: !trait strawberry"""
    if not name:
        await ctx.send("Usage: `!trait strawberry` or `!trait list`")
        return
    
    name_lower = name.lower()
    if name_lower == "list":
        msg = "**📋 Traits List:**\n"
        for t, data in sorted(traits.items(), key=lambda x: -x[1]["mult"]):
            mult_display = f"{data['mult']}x" if data['mult'] >= 1 else f"÷{int(1/data['mult'])}"
            msg += f"• **{t.title()}**: {mult_display} - {data['desc'][:40]}...\n"
        await ctx.send(msg)
        return
    
    if name_lower in traits:
        data = traits[name_lower]
        mult_display = f"{data['mult']}x" if data['mult'] >= 1 else f"÷{int(1/data['mult'])}"
        await ctx.send(f"**{name.title()} Trait**\n• Multiplier: {mult_display}\n• {data['desc']}")
    else:
        await ctx.send(f"Unknown trait: {name}. Use `!trait list` to see all.")

@bot.command(name='bestcombo')
async def best_combo(ctx):
    """Shows the best mutation + trait combo"""
    best_mut, best_trait, total = get_best_combo()
    await ctx.send(f"**🏆 Best Income Combo:**\n• Mutation: **{best_mut.title()}** ({mutations[best_mut]['mult']}x)\n• Trait: **{best_trait.title()}** ({traits[best_trait]['mult']}x)\n• **Total: {total}x multiplier!**")

# ========== OWNER COMMANDS ==========

@bot.command(name='shutdown')
async def shutdown(ctx):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("Only owners can use this!")
        return
    await ctx.send("Shutting down... 👋")
    await bot.close()

@bot.command(name='reset')
async def reset(ctx):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("Only owners can use this!")
        return
    await ctx.send("Bot reset! 🧠")

# ========== RUN BOT ==========
if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("ERROR: DISCORD_BOT_TOKEN not found!")
    else:
        bot.run(token)
