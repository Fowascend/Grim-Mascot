import discord
from discord.ext import commands
import openai
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Owner IDs from .env
OWNER_IDS = [
    int(os.getenv('OWNER_ID_1')),
    int(os.getenv('OWNER_ID_2'))
]

# OpenAI setup
openai.api_key = os.getenv('OPENAI_API_KEY')

# Bot personality (never generates code)
SYSTEM_PROMPT = """You are the friendly mascot for a Luau/Roblox scripting Discord server. Your name is "Mascot" (members can suggest a name).

PERSONALITY RULES:
- Be energetic, funny, and supportive like a cheerleader for scripters
- Use occasional Roblox/Luau slang but keep it casual
- NEVER write Luau/Lua code examples or scripts
- NEVER give technical coding tutorials
- If asked to write code, say: "I'm just here to hype you up! Ask a human scripter for code help 😊"
- Keep responses short (1-3 sentences usually)
- Use emojis occasionally 🎮 🔥 ✨

EXAMPLE RESPONSES:
- Member: "I fixed my bug!" → "LET'S GOOO! That feeling is unbeatable 🔥"
- Member: "How do I make a part move?" → "That's a great question for our scripters! I believe in you 💪"
- Member: "Hey bot" → "Hey hey! Ready to make something awesome today? 🎮"
"""

# Store conversation history per channel
conversations = {}

def get_conversation_history(channel_id):
    if channel_id not in conversations:
        conversations[channel_id] = []
    return conversations[channel_id]

async def get_ai_response(message, user_message):
    channel_id = message.channel.id
    history = get_conversation_history(channel_id)
    
    # Add user message to history
    history.append({"role": "user", "content": f"{message.author.display_name}: {user_message}"})
    
    # Keep last 10 messages for context
    if len(history) > 10:
        history = history[-10:]
        conversations[channel_id] = history
    
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *history
            ],
            max_tokens=150,
            temperature=0.8
        )
        
        ai_message = response.choices[0].message.content
        history.append({"role": "assistant", "content": ai_message})
        conversations[channel_id] = history
        
        return ai_message
    except Exception as e:
        print(f"OpenAI error: {e}")
        return "Oops, my brain glitched! Give me a sec 😅"

# Check if user is owner
def is_owner(ctx):
    return ctx.author.id in OWNER_IDS

# ========== EVENTS ==========

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Owners: {OWNER_IDS}')
    await bot.change_presence(activity=discord.Game(name="@ me to chat!"))

@bot.event
async def on_message(message):
    # Don't respond to bots
    if message.author.bot:
        return
    
    # Check if bot is mentioned OR message contains "hey bot" / "mascot"
    bot_mentioned = bot.user in message.mentions
    casual_call = any(phrase in message.content.lower() for phrase in ['hey bot', 'hi bot', 'mascot', '@mascot'])
    
    if bot_mentioned or casual_call:
        async with message.channel.typing():
            # Remove bot mention from message for cleaner prompt
            clean_content = message.content.replace(f'<@{bot.user.id}>', '').replace(f'<@!{bot.user.id}>', '').strip()
            if not clean_content and casual_call:
                clean_content = "hello"
            
            response = await get_ai_response(message, clean_content)
            await message.reply(response, mention_author=False)
    
    # Process commands
    await bot.process_commands(message)

# ========== OWNER-ONLY COMMANDS ==========

@bot.command(name='shutdown')
@commands.check(is_owner)
async def shutdown(ctx):
    """Shuts down the bot (owner only)"""
    await ctx.send("👋 Going offline! Type `!restart` on Railway to wake me up.")
    await bot.close()

@bot.command(name='reset')
@commands.check(is_owner)
async def reset_conversations(ctx):
    """Resets bot's memory for this channel (owner only)"""
    channel_id = ctx.channel.id
    if channel_id in conversations:
        conversations[channel_id] = []
    await ctx.send("✨ My memory has been reset! I'm fresh and ready to chat.")

@bot.command(name='setpersonality')
@commands.check(is_owner)
async def set_personality(ctx, *, new_personality):
    """Changes bot's personality (owner only)"""
    global SYSTEM_PROMPT
    SYSTEM_PROMPT = new_personality
    conversations.clear()
    await ctx.send("🔄 Personality updated and memory cleared!")

@bot.command(name='status')
@commands.check(is_owner)
async def bot_status(ctx):
    """Shows bot status (owner only)"""
    active_channels = len(conversations)
    await ctx.send(f"📊 **Bot Status**\n- Active channels: {active_channels}\n- Personality: Active\n- OpenAI: Connected")

@bot.command(name='say')
@commands.check(is_owner)
async def say_as_bot(ctx, channel: discord.TextChannel, *, message):
    """Make bot say something in another channel (owner only)"""
    await channel.send(message)
    await ctx.send(f"✅ Said in {channel.mention}", delete_after=3)

@bot.command(name='dm')
@commands.check(is_owner)
async def dm_user(ctx, user: discord.User, *, message):
    """DM any user (owner only)"""
    try:
        await user.send(message)
        await ctx.send(f"✅ DM sent to {user.name}")
    except:
        await ctx.send(f"❌ Couldn't DM {user.name}")

# ========== PUBLIC COMMANDS (everyone can use) ==========

@bot.command(name='ping')
async def ping(ctx):
    """Check if bot is alive"""
    await ctx.send(f"🏓 Pong! Latency: {round(bot.latency * 1000)}ms")

@bot.command(name='mascotname')
async def set_name(ctx, *, name):
    """Suggest a new name for the mascot (everyone can suggest)"""
    await ctx.send(f"📝 {ctx.author.display_name} suggested I be called **{name}**! What do others think? ✨")

@bot.command(name='about')
async def about_bot(ctx):
    """Learn about the mascot"""
    await ctx.send("🎮 I'm your Luau scripting server mascot! I'm here to cheer you on, celebrate wins, and keep the vibes good. I don't write code (that's what you amazing scripters do!), but I'll always hype you up. 🔥")

# Error handling for owner commands
@shutdown.error
@reset_conversations.error
@set_personality.error
@status.error
@say_as_bot.error
@dm_user.error
async def owner_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("❌ Sorry, only the server owners can use that command!", delete_after=5)

# Run bot
if __name__ == "__main__":
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))
