import discord
from discord.ext import commands
import groq
import os
import random
import re
import asyncio
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Owner IDs
OWNER_ID_1 = 1088143400496279552  # Fowascend
OWNER_ID_2 = 1039230074525863998  # Artful
OWNER_IDS = [OWNER_ID_1, OWNER_ID_2]

print(f"Bot starting. Owners: {OWNER_IDS}")

# Groq setup
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    print("ERROR: GROQ_API_KEY not found!")
client = groq.Groq(api_key=GROQ_API_KEY)

# Conversation memory
conversations = {}

# Item values for Steal a Brainrot
item_values = {}

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

def handle_special_questions(message, author_id):
    """Handle special questions like values and gay questions"""
    content = message.lower()
    
    # Handle "is X worth Y" questions
    worth_match = re.search(r'is\s+(.+?)\s+worth\s+(.+?)\??$', content)
    if worth_match:
        item = worth_match.group(1).strip()
        value = worth_match.group(2).strip()
        
        if item in item_values:
            actual = item_values[item]
            if value == actual:
                return f"Yes, {item} is worth {actual}!"
            else:
                return f"No, {item} is worth {actual}, not {value}."
        else:
            return f"I don't know what {item} is worth. An owner can teach me with `!learnvalue`"
    
    # Handle "what is X worth"
    what_match = re.search(r'what\s+is\s+(.+?)\s+worth\??$', content)
    if what_match:
        item = what_match.group(1).strip()
        if item in item_values:
            return f"{item} is worth {item_values[item]}"
        else:
            return f"I don't know what {item} is worth yet!"
    
    # Handle gay questions
    gay_match = re.search(r'is\s+(.+?)\s+gay\??$', content)
    if gay_match:
        target = gay_match.group(1).strip().lower()
        
        # Don't answer about Artful
        if 'artful' in target:
            return "I don't talk about that. Artful is cool though."
        
        # Fowascend asking
        if author_id == OWNER_ID_1:
            if target in ['me', 'myself', 'i', 'fowascend']:
                return "You're the GOAT, bro. No labels needed."
            return "yes bro"
        
        # Artful asking about Fowascend
        if author_id == OWNER_ID_2 and ('fowascend' in target or 'main owner' in target):
            return "No, main owner is straight as an arrow."
        
        # Artful asking about themselves
        if author_id == OWNER_ID_2 and target in ['me', 'myself', 'i', 'artful']:
            return "You're cool, Artful. That's all that matters."
        
        return "I don't really know. Ask the owners?"
    
    return None

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
        clean_content = re.sub(r'mascot', '', message.content.lower(), flags=re.IGNORECASE).strip()
    
    if bot.user in message.mentions:
        should_respond = True
        clean_content = re.sub(f'<@!?{bot.user.id}>', '', message.content).strip()
    
    if not should_respond:
        await bot.process_commands(message)
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
    
    await bot.process_commands(message)

# ========== COMMANDS ==========

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
    await ctx.send("I'm the server mascot! I write code for Fowascend and Artful only. Try saying 'Mascot hi' or ask about item values!")

# Owner only commands
@bot.command(name='learnvalue')
async def learn_value(ctx, *, message: str):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("Only owners can use this!")
        return
    
    if " is worth " in message.lower():
        parts = message.lower().split(" is worth ")
        item = parts[0].strip()
        value = parts[1].strip()
        item_values[item] = value
        await ctx.send(f"✅ Learned: **{item}** = **{value}**")
    else:
        await ctx.send("Format: `!learnvalue strawberry ele is worth 2 meowls`")

@bot.command(name='listvalues')
async def list_values(ctx):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("Only owners can use this!")
        return
    
    if not item_values:
        await ctx.send("No values learned yet. Use `!learnvalue` to add some.")
        return
    
    msg = "**📚 Learned Values:**\n"
    for item, value in list(item_values.items())[:15]:
        msg += f"• {item} → {value}\n"
    await ctx.send(msg)

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
    conversations.clear()
    await ctx.send("Memory reset! 🧠")

@bot.command(name='status')
async def bot_status(ctx):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("Only owners can use this!")
        return
    await ctx.send(f"Active conversations: {len(conversations)} | Values: {len(item_values)}")

if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("ERROR: DISCORD_BOT_TOKEN not found!")
    else:
        bot.run(token)
