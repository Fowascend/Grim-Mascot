import discord
from discord.ext import commands
import groq
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Get owner IDs - handle them carefully
OWNER_IDS = []

owner_id_1 = os.getenv('OWNER_ID_1')
owner_id_2 = os.getenv('OWNER_ID_2')

if owner_id_1:
    OWNER_IDS.append(int(owner_id_1))
if owner_id_2:
    OWNER_IDS.append(int(owner_id_2))

print(f"OWNER_IDS = {OWNER_IDS}")

# Groq setup
groq_api_key = os.getenv('GROQ_API_KEY')
client = groq.Groq(api_key=groq_api_key)

SYSTEM_PROMPT = """You are the friendly mascot for a Luau/Roblox scripting Discord server. Be energetic, funny, and supportive. NEVER write Luau/Lua code. Keep responses short (1-3 sentences). Use emojis occasionally."""

conversations = {}

def get_conversation_history(channel_id):
    if channel_id not in conversations:
        conversations[channel_id] = []
    return conversations[channel_id]

async def get_ai_response(message, user_message):
    channel_id = message.channel.id
    history = get_conversation_history(channel_id)
    
    history.append({"role": "user", "content": f"{message.author.display_name}: {user_message}"})
    
    if len(history) > 10:
        history = history[-10:]
        conversations[channel_id] = history
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
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
        print(f"Error: {e}")
        return "Oops, my brain glitched! Give me a sec 😅"

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'My Bot ID: {bot.user.id}')
    print(f'Expected Owners: {OWNER_IDS}')
    await bot.change_presence(activity=discord.Game(name="!ping | @ me"))

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    # Check if bot is mentioned
    if bot.user in message.mentions:
        async with message.channel.typing():
            clean_content = message.content.replace(f'<@{bot.user.id}>', '').replace(f'<@!{bot.user.id}>', '').strip()
            if not clean_content:
                clean_content = "hello"
            response = await get_ai_response(message, clean_content)
            await message.reply(response, mention_author=False)
    
    await bot.process_commands(message)

# PUBLIC COMMANDS (anyone can use)
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Latency: {round(bot.latency * 1000)}ms")

@bot.command(name='myid')
async def my_id(ctx):
    await ctx.send(f"Your ID: `{ctx.author.id}`")

@bot.command(name='about')
async def about(ctx):
    await ctx.send("🎮 I'm your Luau scripting server mascot! I'm here to cheer you on! 🔥")

# OWNER ONLY COMMANDS
@bot.command(name='shutdown')
async def shutdown(ctx):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("❌ Only the server owner can use this command!")
        return
    await ctx.send("👋 Going offline!")
    await bot.close()

@bot.command(name='reset')
async def reset(ctx):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("❌ Only the server owner can use this command!")
        return
    conversations.clear()
    await ctx.send("✨ My memory has been reset!")

@bot.command(name='status')
async def bot_status(ctx):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("❌ Only the server owner can use this command!")
        return
    await ctx.send(f"📊 Active channels: {len(conversations)}")

if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("ERROR: DISCORD_BOT_TOKEN not found!")
    else:
        bot.run(token)
