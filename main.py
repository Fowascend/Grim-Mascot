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

OWNER_IDS = [
    int(os.getenv('OWNER_ID_1')),
    int(os.getenv('OWNER_ID_2'))
]

# Initialize Groq client (FREE!)
client = groq.Groq(api_key=os.getenv('GROQ_API_KEY'))

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
        print(f"Groq error: {e}")
        return "Oops, my brain glitched! Give me a sec 😅"

def is_owner(ctx):
    return ctx.author.id in OWNER_IDS

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Owners: {OWNER_IDS}')
    await bot.change_presence(activity=discord.Game(name="@ me to chat!"))

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    bot_mentioned = bot.user in message.mentions
    casual_call = any(phrase in message.content.lower() for phrase in ['hey bot', 'hi bot', 'mascot'])
    
    if bot_mentioned or casual_call:
        async with message.channel.typing():
            clean_content = message.content.replace(f'<@{bot.user.id}>', '').replace(f'<@!{bot.user.id}>', '').strip()
            if not clean_content and casual_call:
                clean_content = "hello"
            
            response = await get_ai_response(message, clean_content)
            await message.reply(response, mention_author=False)
    
    await bot.process_commands(message)

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Latency: {round(bot.latency * 1000)}ms")

@bot.command(name='about')
async def about_bot(ctx):
    await ctx.send("🎮 I'm your Luau scripting server mascot! I'm here to cheer you on! 🔥")

@bot.command(name='shutdown')
@commands.check(is_owner)
async def shutdown(ctx):
    await ctx.send("👋 Going offline!")
    await bot.close()

@bot.command(name='reset')
@commands.check(is_owner)
async def reset_conversations(ctx):
    channel_id = ctx.channel.id
    if channel_id in conversations:
        conversations[channel_id] = []
    await ctx.send("✨ My memory has been reset!")

@bot.command(name='botstatus')
@commands.check(is_owner)
async def bot_status(ctx):
    active_channels = len(conversations)
    await ctx.send(f"📊 Bot Status - Active channels: {active_channels}")

@shutdown.error
@reset_conversations.error
@bot_status.error
async def owner_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("❌ Sorry, only server owners can use that command!")

if __name__ == "__main__":
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))
