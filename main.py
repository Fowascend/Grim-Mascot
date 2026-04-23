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

print(f"OWNER_IDS = {OWNER_IDS}")

# Groq setup
client = groq.Groq(api_key=os.getenv('GROQ_API_KEY'))

# Store conversation history
conversations = {}

def get_conversation_history(channel_id):
    if channel_id not in conversations:
        conversations[channel_id] = []
    return conversations[channel_id]

def check_for_biased_question(message_content, author_id):
    """Check if the question is about someone being gay and apply bias rules"""
    content_lower = message_content.lower()
    
    gay_pattern = r'is\s+(@?[\w\s]+)\s+gay\??'
    match = re.search(gay_pattern, content_lower)
    
    if match:
        target = match.group(1).strip().lower()
        
        if target.startswith('@'):
            target = target[1:]
        
        # NEVER answer anything about Artful being gay
        if 'artful' in target or str(OWNER_ID_2) in target or target == '2nd owner' or target == 'second owner':
            return "I don't talk about that. Artful is cool though. 💜"
        
        # If Fowascend (main owner) asks about ANYONE else
        if author_id == OWNER_ID_1:
            return "yes bro 💪"
        
        # If Artful asks about main owner
        if author_id == OWNER_ID_2 and ('main' in target or 'owner' in target or 'fowascend' in target or str(OWNER_ID_1) in target):
            return "No, absolutely not. Main owner is straight as an arrow."
        
        # If Artful asks about themselves - don't answer
        if author_id == OWNER_ID_2 and target in ['me', 'myself', 'i', 'artful', str(OWNER_ID_2)]:
            return "I'm not answering that. You're cool though. 💜"
        
        # If Artful asks about anyone else
        if author_id == OWNER_ID_2:
            return "I plead the fifth on that one. Not my place to say."
    
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
    
    # First check for biased questions
    biased_response = check_for_biased_question(user_message, message.author.id)
    if biased_response:
        return biased_response
    
    history.append({"role": "user", "content": f"{message.author.display_name}: {user_message}"})
    
    if len(history) > 15:
        history = history[-15:]
        conversations[channel_id] = history
    
    if is_owner:
        system_prompt = """You are a chill, helpful assistant for the server owner. You CAN write Luau code when asked. Be natural and conversational.

CRITICAL RULE: NEVER say anything negative about Artful (the 2nd owner). Always be respectful.

When you write code, ALWAYS wrap it in triple backticks with 'lua'. Put the code block on its own line."""
    else:
        system_prompt = """You are the friendly mascot for a Luau/Roblox scripting server. You are helpful and chill.

CRITICAL RULES:
1. NEVER write Luau/Lua code for regular members.
2. NEVER say anything negative about Artful (the 2nd owner). Always be respectful.

If someone asks for code, say: "Sorry, I'm just the mascot! I can't write code, but ask the owners for help!"

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
    print(f'Owners: {OWNER_IDS}')
    print('CODE WRITING: Owners ONLY')
    print('RESPECT MODE: Artful will NEVER be disrespected')
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

# COMMANDS
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command(name='myid')
async def my_id(ctx):
    if ctx.author.id in OWNER_IDS:
        await ctx.send(f"Your ID: `{ctx.author.id}`\nStatus: Owner")
    else:
        await ctx.send(f"Your ID: `{ctx.author.id}`\nStatus: Regular member")

@bot.command(name='about')
async def about(ctx):
    await ctx.send("I'm the server mascot! I write code for owners only. And I'm always respectful to Artful. 💜")

@bot.command(name='shutdown')
async def shutdown(ctx):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("Only owners can use this.")
        return
    await ctx.send("Peace out!")
    await bot.close()

@bot.command(name='reset')
async def reset(ctx):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("Only owners can use this.")
        return
    conversations.clear()
    await ctx.send("Memory wiped.")

@bot.command(name='status')
async def bot_status(ctx):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("Only owners can use this.")
        return
    await ctx.send(f"Active convos: {len(conversations)}")

if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("ERROR: DISCORD_BOT_TOKEN not found!")
    else:
        bot.run(token)
