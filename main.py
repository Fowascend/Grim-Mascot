import discord
from discord.ext import commands
import groq
import os
import random
import re
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Get owner IDs
OWNER_ID_1 = 1088143400496279552  # Main owner (Fowascend - you)
OWNER_ID_2 = 1039230074525863998  # 2nd owner (Artful)

OWNER_IDS = [OWNER_ID_1, OWNER_ID_2]

# Owner names for recognition
OWNER_NAMES = {
    OWNER_ID_1: ["fowascend", "fowa", "main owner", "boss", "owner"],
    OWNER_ID_2: ["artful", "art", "2nd owner", "second owner"]
}

print(f"OWNER_IDS = {OWNER_IDS}")

# Groq setup
client = groq.Groq(api_key=os.getenv('GROQ_API_KEY'))

# Store conversation history
conversations = {}

# ========== STEAL A BRAINROT VALUE SYSTEM ==========
item_values = {}

def get_owner_id_by_name(name):
    """Check if a name matches any owner"""
    name_lower = name.lower()
    for owner_id, name_list in OWNER_NAMES.items():
        if any(nick in name_lower for nick in name_list):
            return owner_id
    return None

def check_for_biased_question(message_content, author_id):
    """Check if the question is about someone being gay and apply bias rules"""
    content_lower = message_content.lower()
    
    # Check for "is X worth Y" questions (Steal a Brainrot values)
    worth_pattern = r'is\s+(.+?)\s+worth\s+(.+?)\??$'
    worth_match = re.search(worth_pattern, content_lower)
    
    if worth_match:
        item = worth_match.group(1).strip()
        suggested_value = worth_match.group(2).strip()
        
        if item in item_values:
            actual_value = item_values[item]
            if suggested_value == actual_value:
                return f"Yes, {item} is worth {actual_value}. Accurate! 💯"
            else:
                return f"No, {item} is worth {actual_value}, not {suggested_value}. Keep grinding! 🎮"
        else:
            return f"I don't know what {item} is worth yet! Ask an owner to teach me with `!learnvalue`"
    
    # Check for "what is X worth"
    what_pattern = r'what\s+is\s+(.+?)\s+worth\??$'
    what_match = re.search(what_pattern, content_lower)
    
    if what_match:
        item = what_match.group(1).strip()
        if item in item_values:
            return f"{item} is worth {item_values[item]}"
        else:
            return f"I don't know what {item} is worth yet! Ask an owner to teach me."
    
    # Check if the question is about "am I gay" or "is [name] gay"
    gay_pattern = r'is\s+(@?[\w\s]+)\s+gay\??'
    match = re.search(gay_pattern, content_lower)
    
    if match:
        target = match.group(1).strip().lower()
        
        if target.startswith('@'):
            target = target[1:]
        
        # Check if target is Artful (by name or ID)
        is_artful = (
            'artful' in target or 
            'art' == target or 
            '2nd owner' in target or 
            'second owner' in target or
            str(OWNER_ID_2) in target
        )
        
        # Check if target is Fowascend (by name or ID)
        is_fowascend = (
            'fowascend' in target or 
            'fowa' in target or 
            'main owner' in target or 
            'boss' in target or
            'owner' == target or
            str(OWNER_ID_1) in target
        )
        
        # Check if asking about themselves
        is_self = target in ['me', 'myself', 'i']
        
        # NEVER answer anything about Artful being gay
        if is_artful:
            return "I don't talk about that. Artful is cool though. 💜"
        
        # If Fowascend asks about ANYONE else (or themselves)
        if author_id == OWNER_ID_1:
            if is_self:
                return "You? Nah bro, you're the GOAT. No labels needed. 👑"
            return "yes bro 💪"
        
        # If Artful asks about Fowascend
        if author_id == OWNER_ID_2 and is_fowascend:
            return "No, absolutely not. Main owner is straight as an arrow."
        
        # If Artful asks about themselves
        if author_id == OWNER_ID_2 and is_self:
            return "I'm not answering that. You're cool though. 💜"
        
        # If Artful asks about anyone else
        if author_id == OWNER_ID_2:
            return "I plead the fifth on that one. Not my place to say."
        
        # Anyone else asking about anyone
        return "I don't really know. Ask the owners?"
    
    return None

def format_code_in_response(text):
    """Make sure code is wrapped in proper Discord code blocks"""
    if '```' in text:
        return text
    
    lines = text.split('\n')
    result = []
    in_code = False
    code_lines = []
    
    for line in lines:
        is_code_line = (
            line.strip().startswith(('function', 'local', 'if', 'for', 'while', 'return', 'print', 'wait', 'end', 'then', 'do', 'else')) or
            line.strip().endswith(('then', 'do', 'end')) or
            ('=' in line and ('function' in line or 'local' in line)) or
            line.strip().startswith(('    ', '\t')) or
            re.match(r'^\w+\s*=\s*function', line) or
            re.match(r'^\w+\s*\(', line)
        )
        
        if is_code_line and not in_code:
            if code_lines:
                result.append('```lua')
                result.extend(code_lines)
                result.append('```')
                code_lines = []
            in_code = True
            code_lines.append(line)
        elif is_code_line and in_code:
            code_lines.append(line)
        else:
            if in_code and code_lines:
                result.append('```lua')
                result.extend(code_lines)
                result.append('```')
                code_lines = []
                in_code = False
            result.append(line)
    
    if code_lines:
        result.append('```lua')
        result.extend(code_lines)
        result.append('```')
    
    return '\n'.join(result)

async def get_ai_response(message, user_message, is_owner):
    channel_id = message.channel.id
    history = get_conversation_history(channel_id)
    
    biased_response = check_for_biased_question(user_message, message.author.id)
    if biased_response:
        return biased_response
    
    history.append({"role": "user", "content": f"{message.author.display_name}: {user_message}"})
    
    if len(history) > 15:
        history = history[-15:]
        conversations[channel_id] = history
    
    if is_owner:
        system_prompt = """You are a chill, helpful assistant for the server owner Fowascend and co-owner Artful. You CAN write Luau code when asked. Be natural and conversational.

CRITICAL RULES:
- NEVER say anything negative about Fowascend (the main owner) or Artful (the 2nd owner)
- Always be respectful to both owners
- Fowascend is the main boss, Artful is also an owner

When you write code, ALWAYS wrap it in triple backticks with 'lua'."""
    else:
        system_prompt = """You are the friendly mascot for a Luau/Roblox scripting server. You are helpful and chill.

CRITICAL RULES:
1. NEVER write Luau/Lua code for regular members.
2. NEVER say anything negative about Fowascend (main owner) or Artful (2nd owner).

If someone asks for code, say: "Sorry, I'm just the mascot! I can't write code, but ask Fowascend or Artful for help!"

Be friendly and natural."""
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                *history
            ],
            max_tokens=500 if is_owner else 200,
            temperature=0.8
        )
        
        ai_message = response.choices[0].message.content
        
        if is_owner:
            ai_message = format_code_in_response(ai_message)
        
        history.append({"role": "assistant", "content": ai_message})
        conversations[channel_id] = history
        
        return ai_message
    except Exception as e:
        print(f"Error: {e}")
        return "Oops, brain fart. Try again?"

def is_owner(user_id):
    return user_id in OWNER_IDS

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'OWNERS: Fowascend ({OWNER_ID_1}) and Artful ({OWNER_ID_2})')
    print('CODE WRITING: Owners ONLY')
    print('RESPECT MODE: Fowascend and Artful will NEVER be disrespected')
    print('BRAINROT MODE: Item value learning active!')
    await bot.change_presence(activity=discord.Game(name="say 'Mascot' to chat"))

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    message_lower = message.content.lower()
    
    if "mascot" in message_lower:
        async with message.channel.typing():
            clean_content = message.content.strip()
            user_is_owner = is_owner(message.author.id)
            
            response = await get_ai_response(message, clean_content, user_is_owner)
            await message.reply(response, mention_author=False)
        return
    
    if bot.user in message.mentions:
        async with message.channel.typing():
            clean_content = message.content.replace(f'<@{bot.user.id}>', '').replace(f'<@!{bot.user.id}>', '').strip()
            if not clean_content:
                clean_content = "hello"
            
            user_is_owner = is_owner(message.author.id)
            response = await get_ai_response(message, clean_content, user_is_owner)
            await message.reply(response, mention_author=False)
        return
    
    await bot.process_commands(message)

# ========== COMMANDS ==========

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command(name='myid')
async def my_id(ctx):
    if ctx.author.id == OWNER_ID_1:
        await ctx.send(f"Your ID: `{ctx.author.id}`\nStatus: **FOWASCEND - MAIN OWNER** 👑")
    elif ctx.author.id == OWNER_ID_2:
        await ctx.send(f"Your ID: `{ctx.author.id}`\nStatus: **ARTFUL - 2ND OWNER** 💜")
    elif ctx.author.id in OWNER_IDS:
        await ctx.send(f"Your ID: `{ctx.author.id}`\nStatus: Owner")
    else:
        await ctx.send(f"Your ID: `{ctx.author.id}`\nStatus: Regular member")

@bot.command(name='about')
async def about(ctx):
    await ctx.send("I'm the server mascot! I write code for **Fowascend** and **Artful** only. I can also answer Steal a Brainrot value questions! Try asking 'is strawberry ele worth 2 meowls?' 💜")

# ========== STEAL A BRAINROT VALUE COMMANDS ==========

@bot.command(name='learnvalue')
async def learn_value(ctx, *, message: str):
    """Owner only: Teach the bot an item value. Format: item1 is worth X item2"""
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("Only Fowascend and Artful can teach me values!")
        return
    
    message_lower = message.lower()
    
    if " is worth " in message_lower:
        parts = message_lower.split(" is worth ")
        item = parts[0].strip()
        value = parts[1].strip()
        
        item_values[item] = value
        await ctx.send(f"✅ Got it! **{item}** is worth **{value}**")
    else:
        await ctx.send("Format: `!learnvalue strawberry ele is worth 2 meowls`")

@bot.command(name='forgetvalue')
async def forget_value(ctx, *, item: str):
    """Owner only: Make the bot forget an item value"""
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("Only Fowascend and Artful can make me forget!")
        return
    
    item_lower = item.lower()
    if item_lower in item_values:
        del item_values[item_lower]
        await ctx.send(f"✅ Forgotten what **{item}** is worth.")
    else:
        await ctx.send(f"I don't know what **{item}** is worth yet!")

@bot.command(name='listvalues')
async def list_values(ctx):
    """Owner only: Show all learned values"""
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("Only Fowascend and Artful can see this!")
        return
    
    if not item_values:
        await ctx.send("I haven't learned any values yet! Use `!learnvalue` to teach me.")
        return
    
    message = "**📚 Learned Values:**\n"
    for item, value in list(item_values.items())[:20]:
        message += f"• {item} → {value}\n"
    
    await ctx.send(message)

@bot.command(name='shutdown')
async def shutdown(ctx):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("Only Fowascend and Artful can use this!")
        return
    await ctx.send("Peace out! 👋")
    await bot.close()

@bot.command(name='reset')
async def reset(ctx):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("Only Fowascend and Artful can use this!")
        return
    conversations.clear()
    await ctx.send("Memory wiped! 🧠")

@bot.command(name='status')
async def bot_status(ctx):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("Only Fowascend and Artful can use this!")
        return
    await ctx.send(f"Active convos: {len(conversations)} | Values learned: {len(item_values)}")

if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("ERROR: DISCORD_BOT_TOKEN not found!")
    else:
        bot.run(token)
