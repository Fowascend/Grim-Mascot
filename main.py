import discord
from discord.ext import commands
import groq
import os
import random
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Get owner IDs
OWNER_IDS = []
owner_id_1 = os.getenv('OWNER_ID_1')
owner_id_2 = os.getenv('OWNER_ID_2')

if owner_id_1:
    OWNER_IDS.append(int(owner_id_1))
if owner_id_2:
    OWNER_IDS.append(int(owner_id_2))

print(f"OWNER_IDS = {OWNER_IDS}")

# Groq setup
client = groq.Groq(api_key=os.getenv('GROQ_API_KEY'))

# REGULAR MEMBERS - Friendly mascot
MASCOT_PROMPT = """You are the friendly mascot for a Luau/Roblox scripting Discord server. Be helpful, chill, and supportive. NEVER write Luau/Lua code. Keep responses natural and not too long. Don't overdo emojis. If someone asks for code, politely say you're just a mascot and suggest they ask a scripter."""

# OWNERS - Helpful assistant (glaze only when asked for validation)
OWNER_PROMPT = """You are a helpful assistant for the server owner. You can write Luau/Roblox code when asked.

IMPORTANT RULES:
- Be normal and conversational. Don't randomly hype or glaze.
- ONLY give compliments or praise if the user directly asks for validation like:
  * "am I amazing?"
  * "tell me I'm good"
  * "praise me"
  * "say something nice about me"
  * "am I doing well?"
  * "glaze me"
- Otherwise, just answer normally like a helpful coding assistant.
- When asked for validation, give a genuine, nice compliment.
- Provide clean Luau code when requested.
- Keep it natural, not over-the-top.
- Use very few emojis."""

conversations = {}

def get_conversation_history(channel_id):
    if channel_id not in conversations:
        conversations[channel_id] = []
    return conversations[channel_id]

async def get_ai_response(message, user_message, is_owner):
    channel_id = message.channel.id
    history = get_conversation_history(channel_id)
    
    history.append({"role": "user", "content": f"{message.author.display_name}: {user_message}"})
    
    if len(history) > 15:
        history = history[-15:]
        conversations[channel_id] = history
    
    system_prompt = OWNER_PROMPT if is_owner else MASCOT_PROMPT
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                *history
            ],
            max_tokens=400 if is_owner else 200,
            temperature=0.7
        )
        
        ai_message = response.choices[0].message.content
        history.append({"role": "assistant", "content": ai_message})
        conversations[channel_id] = history
        
        return ai_message
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, my brain glitched. Try again?"

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
    is_owner_text = "Yes, you're an owner" if ctx.author.id in OWNER_IDS else "No, you're a regular member"
    await ctx.send(f"Your ID: `{ctx.author.id}`\nOwner status: {is_owner_text}")

@bot.command(name='about')
async def about(ctx):
    await ctx.send("I'm the server mascot. I can chat normally, and for owners I can help write Luau code. If you want a compliment, just ask for it.")

# OWNER ONLY COMMANDS
@bot.command(name='shutdown')
async def shutdown(ctx):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("Only server owners can use this command.")
        return
    await ctx.send("Shutting down...")
    await bot.close()

@bot.command(name='reset')
async def reset(ctx):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("Only server owners can use this command.")
        return
    conversations.clear()
    await ctx.send("Memory reset.")

@bot.command(name='status')
async def bot_status(ctx):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("Only server owners can use this command.")
        return
    await ctx.send(f"Active conversations: {len(conversations)}")

@bot.command(name='glaze')
async def glaze_command(ctx):
    """Owner-only: Makes the bot compliment you"""
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("Only server owners can use this command.")
        return
    
    compliments = [
        f"You're doing good work, {ctx.author.display_name}.",
        f"{ctx.author.display_name}, you're actually pretty solid at this.",
        f"Not gonna lie, {ctx.author.display_name}, you know your stuff.",
        f"{ctx.author.display_name} has been killing it lately.",
        f"Keep it up, {ctx.author.display_name}. You're doing fine."
    ]
    await ctx.send(random.choice(compliments))

if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("ERROR: DISCORD_BOT_TOKEN not found!")
    else:
        bot.run(token)
