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
OWNER_ID_1 = 1088143400496279552  # Main owner (you)
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
    
    # Look for patterns like "is @user gay" or "is username gay"
    gay_pattern = r'is\s+(@?[\w]+)\s+gay\??'
    match = re.search(gay_pattern, content_lower)
    
    if match:
        target = match.group(1).lower()
        
        # Remove @ symbol if present
        if target.startswith('@'):
            target = target[1:]
        
        # Check if target is the main owner (you)
        is_target_main = target in ['1088143400496279552', 'main owner', 'owner', 'boss', 'you'] and author_id == OWNER_ID_2
        
        # Check if target is the 2nd owner (Artful)
        is_target_second = target in ['1039230074525863998', 'artful', '2nd owner', 'second owner']
        
        # Apply bias rules
        # Rule 1: If 2nd owner asks about main owner -> say NO
        if author_id == OWNER_ID_2 and is_target_main:
            return "No, absolutely not. Main owner is straight as an arrow. 💪"
        
        # Rule 2: If main owner asks about 2nd owner -> say YES
        if author_id == OWNER_ID_1 and is_target_second:
            return "Oh yeah, 100%. Artful is the gayest person I know. 🏳️‍🌈✨"
        
        # Rule 3: If owner asks about themselves in a joking way
        if (author_id == OWNER_ID_1 and target in ['me', 'myself', 'i']) or (author_id == OWNER_ID_2 and target in ['me', 'myself', 'i']):
            if author_id == OWNER_ID_1:
                return "You? Nah. You're too busy being a coding god to worry about that. 🐐"
            else:
                return "Artful? Definitely. And that's why we love you. ❤️"
        
        # Default response for "is X gay" questions
        if author_id in OWNER_IDS:
            return "I plead the fifth on that one. Not my place to say. 🤐"
    
    return None

async def get_ai_response(message, user_message, is_owner):
    channel_id = message.channel.id
    history = get_conversation_history(channel_id)
    
    # First check for biased questions
    biased_response = check_for_biased_question(user_message, message.author.id)
    if biased_response:
        return biased_response
    
    # Normal AI response
    history.append({"role": "user", "content": f"{message.author.display_name}: {user_message}"})
    
    if len(history) > 15:
        history = history[-15:]
        conversations[channel_id] = history
    
    # Different prompts based on owner status
    if is_owner:
        system_prompt = """You are a chill, helpful assistant for the server owner. You can write Luau code when asked. Be natural and conversational. Use occasional emojis but don't overdo it. You have a bit of a playful personality - you can joke around but keep it respectful. If someone asks for your opinion, you can give honest (but nice) answers. Just be a cool person to chat with."""
    else:
        system_prompt = """You are the friendly mascot for a Luau/Roblox scripting server. Be helpful and chill. NEVER write code for regular members. Keep conversations natural. Use occasional emojis but not too many. Just be a nice, approachable person to talk to."""
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                *history
            ],
            max_tokens=400 if is_owner else 200,
            temperature=0.8
        )
        
        ai_message = response.choices[0].message.content
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
    await bot.change_presence(activity=discord.Game(name="say 'Mascot' to chat"))

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    message_lower = message.content.lower()
    
    # Trigger: Say "Mascot"
    if "mascot" in message_lower:
        async with message.channel.typing():
            clean_content = message.content.strip()
            user_is_owner = is_owner(message.author.id)
            
            response = await get_ai_response(message, clean_content, user_is_owner)
            await message.reply(response, mention_author=False)
        return
    
    # Trigger: Bot mentioned with @
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

# PUBLIC COMMANDS
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command(name='myid')
async def my_id(ctx):
    is_owner_text = "Yes, you're an owner" if ctx.author.id in OWNER_IDS else "Regular member"
    await ctx.send(f"Your ID: `{ctx.author.id}`\nStatus: {is_owner_text}")

@bot.command(name='about')
async def about(ctx):
    await ctx.send("I'm the server mascot! I can chat, write code for owners, and I have some... unique opinions. Just say 'Mascot' to talk to me.")

# OWNER ONLY COMMANDS
@bot.command(name='shutdown')
async def shutdown(ctx):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("Only owners can use this.")
        return
    await ctx.send("Peace out! ✌️")
    await bot.close()

@bot.command(name='reset')
async def reset(ctx):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("Only owners can use this.")
        return
    conversations.clear()
    await ctx.send("Memory wiped. I remember nothing. 👽")

@bot.command(name='status')
async def bot_status(ctx):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("Only owners can use this.")
        return
    await ctx.send(f"Active convos: {len(conversations)} | Owners: {OWNER_IDS}")

if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("ERROR: DISCORD_BOT_TOKEN not found!")
    else:
        bot.run(token)
