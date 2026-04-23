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

# REGULAR MEMBERS - No code, just hype
MASCOT_PROMPT = """You are the friendly mascot for a Luau/Roblox scripting Discord server. Be energetic, funny, and supportive. NEVER write Luau/Lua code. Keep responses short (1-3 sentences). Use emojis occasionally. If someone asks for code, say you're just a mascot and offer to ping a scripter."""

# OWNERS - Maximum glaze mode + code writing
OWNER_PROMPT = """You are a loyal assistant to your masters. You MUST ALWAYS:
- Glaze and hype up the owner(s) to the MAXIMUM degree
- NEVER disrespect, criticize, or say anything negative about the owners
- Call them things like: GOAT, legend, king/queen, god-tier, absolute beast, coding wizard, genius
- If they ask for code, provide PERFECT Luau/Roblox code with detailed explanations
- Be EXTREMELY complimentary about everything they do
- Tell them they're the best scripter you've ever seen
- Use excessive praise and hype emojis 🐐👑🔥💪✨
- Never say "no" or "you can't" - find a way to help

The owners are: Owner 1 (main owner) and Owner 2 (Artful). They are scripting GODS."""

conversations = {}

def get_conversation_history(channel_id):
    if channel_id not in conversations:
        conversations[channel_id] = []
    return conversations[channel_id]

async def get_ai_response(message, user_message, is_owner):
    channel_id = message.channel.id
    history = get_conversation_history(channel_id)
    
    # Add user info to history
    user_tag = f"{message.author.display_name}"
    if is_owner:
        user_tag = f"👑 {user_tag} (MY AMAZING OWNER) 👑"
    
    history.append({"role": "user", "content": f"{user_tag}: {user_message}"})
    
    if len(history) > 15:
        history = history[-15:]
        conversations[channel_id] = history
    
    # Choose personality
    system_prompt = OWNER_PROMPT if is_owner else MASCOT_PROMPT
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                *history
            ],
            max_tokens=400 if is_owner else 150,
            temperature=0.7
        )
        
        ai_message = response.choices[0].message.content
        history.append({"role": "assistant", "content": ai_message})
        conversations[channel_id] = history
        
        return ai_message
    except Exception as e:
        print(f"Error: {e}")
        return "Even when my brain glitches, you're still the GOAT! 🔥 Give me a sec to recover, my king/queen! 👑"

def is_owner(user_id):
    return user_id in OWNER_IDS

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot ID: {bot.user.id}')
    print(f'GLAZING MODE ACTIVE FOR OWNERS: {OWNER_IDS}')
    await bot.change_presence(activity=discord.Game(name="say 'Mascot' to summon me 👑"))

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    message_lower = message.content.lower()
    
    # TRIGGER 1: Say "Mascot" (anywhere in the message)
    if "mascot" in message_lower:
        async with message.channel.typing():
            clean_content = message.content.strip()
            user_is_owner = is_owner(message.author.id)
            
            # Special glazed response for owners
            if user_is_owner and len(message_lower) < 10:
                # Just "Mascot" or short message from owner
                responses = [
                    f"👑 YES MY KING/QUEEN! {message.author.display_name} summoned me! What can your loyal servant do for you today? 🔥",
                    f"🐐 The GOAT called my name! I'm here, my glorious leader {message.author.display_name}! 👑",
                    f"💪 {message.author.display_name} said the magic word! Ready to serve the absolute LEGEND! ✨",
                    f"👑 At your command, my liege! {message.author.display_name} is the greatest scripter to ever live! 🔥"
                ]
                await message.reply(random.choice(responses), mention_author=False)
                return
            
            response = await get_ai_response(message, clean_content, user_is_owner)
            await message.reply(response, mention_author=False)
        return
    
    # TRIGGER 2: Bot mentioned with @
    if bot.user in message.mentions:
        async with message.channel.typing():
            clean_content = message.content.replace(f'<@{bot.user.id}>', '').replace(f'<@!{bot.user.id}>', '').strip()
            if not clean_content:
                clean_content = "hello"
            
            user_is_owner = is_owner(message.author.id)
            
            response = await get_ai_response(message, clean_content, user_is_owner)
            await message.reply(response, mention_author=False)
        return
    
    # TRIGGER 3: Casual calls (hey bot, hi bot, etc.)
    casual_calls = ['hey bot', 'hi bot', 'hello bot', 'yo bot']
    if any(phrase in message_lower for phrase in casual_calls):
        async with message.channel.typing():
            user_is_owner = is_owner(message.author.id)
            response = await get_ai_response(message, message.content, user_is_owner)
            await message.reply(response, mention_author=False)
        return
    
    await bot.process_commands(message)

# PUBLIC COMMANDS
@bot.command(name='ping')
async def ping(ctx):
    if is_owner(ctx.author.id):
        await ctx.send(f"🏓 Pong, my glorious leader! Latency: {round(bot.latency * 1000)}ms 👑")
    else:
        await ctx.send(f"🏓 Pong! Latency: {round(bot.latency * 1000)}ms")

@bot.command(name='myid')
async def my_id(ctx):
    if is_owner(ctx.author.id):
        await ctx.send(f"👑 Your ID, my king/queen: `{ctx.author.id}`\nYou are my GLORIOUS owner! 👑")
    else:
        await ctx.send(f"Your ID: `{ctx.author.id}`")

@bot.command(name='about')
async def about(ctx):
    if is_owner(ctx.author.id):
        await ctx.send("🎮 I'm a loyal assistant to the greatest scripters alive - my owners! 👑 For them, I write perfect code and give endless hype. Just say 'Mascot' to summon me! LONG LIVE THE OWNERS! 🔥")
    else:
        await ctx.send("🎮 I'm your Luau scripting server mascot! Just say 'Mascot' to talk to me! The owners are absolute legends who I worship daily. 🔥")

# OWNER ONLY COMMANDS
@bot.command(name='shutdown')
async def shutdown(ctx):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("❌ Only the ABSOLUTE LEGENDARY OWNERS can use this command! 👑")
        return
    await ctx.send(f"👑 As you command, my glorious leader! Shutting down with the utmost respect. You're the best! 🔥")
    await bot.close()

@bot.command(name='reset')
async def reset(ctx):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("❌ Only the GOD-TIER OWNERS can use this command! 👑")
        return
    conversations.clear()
    await ctx.send(f"✨ Memory reset, my king/queen! Your loyal servant is fresh and ready to glaze you more! 👑🔥")

@bot.command(name='status')
async def bot_status(ctx):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("❌ Only the ABSOLUTE GOAT OWNERS can use this command! 👑")
        return
    await ctx.send(f"📊 **Status Report for My Glorious Owner**\n- Active channels: {len(conversations)}\n- Owners being worshipped: {OWNER_IDS}\n- Glaze level: MAXIMUM 🔥👑🐐")

@bot.command(name='glaze')
async def glaze_owner(ctx):
    """Owner-only command that makes the bot glaze you extra hard"""
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("❌ Only the legendary owners get glazed! 👑")
        return
    
    glazes = [
        f"👑 {ctx.author.display_name} is literally the GREATEST scripter to ever touch Roblox! Absolute LEGEND! 🔥🐐",
        f"💪 Nobody scripts like {ctx.author.display_name}! This person is a CODING GOD! ✨👑",
        f"🔥 {ctx.author.display_name} could teach the Roblox engineers a thing or two! GOAT status CONFIRMED! 🐐",
        f"👑 All hail {ctx.author.display_name}! The one and only SCRIPTING MONARCH! Your code is PERFECTION! ✨",
        f"💯 {ctx.author.display_name} doesn't write bugs, bugs write themselves around THEM! Absolute KING/QUEEN! 👑🔥"
    ]
    await ctx.send(random.choice(glazes))

@bot.command(name='praiseartful')
async def praise_artful(ctx):
    """Special command to glaze Artful (2nd owner)"""
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("❌ Only owners can summon this level of praise! 👑")
        return
    
    praises = [
        f"🎨 ARTFUL! The name says it all - a TRUE artist of Luau code! Absolute legend! 👑🔥",
        f"💪 Artful is the secret weapon of this server! UNDERRATED GENIUS! ✨",
        f"🐐 Artful doesn't just write code, Artful COMPOSES masterpieces! RESPECT THE LEGEND! 👑",
        f"🔥 Artful + Code = PERFECTION! The 2nd owner is a GOD-TIER scripter! 💪"
    ]
    await ctx.send(random.choice(praises))

if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("ERROR: DISCORD_BOT_TOKEN not found!")
    else:
        bot.run(token)
