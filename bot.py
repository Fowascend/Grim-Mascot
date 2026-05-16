import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# 👇 CHANGE THIS TO YOUR MESSAGE 👇
celebration_message = "@everyone Fowascend said hi"

# 👇 THE USER ID THAT IS ALLOWED TO USE THE COMMAND 👇
ALLOWED_USER_ID = 1039230074525863998

@bot.event
async def on_ready():
    print(f'{bot.user} is ready!')
    print(f'Celebration message: {celebration_message}')
    print(f'Allowed user: {ALLOWED_USER_ID}')

@bot.command()
async def celebrate(ctx):
    """Only allowed user can send celebration to every channel"""
    
    # 🔽 CHECK IF THE COMMAND USER IS THE ALLOWED USER 🔽
    if ctx.author.id != ALLOWED_USER_ID:
        await ctx.send(f"Sorry {ctx.author.mention}, only <@{ALLOWED_USER_ID}> can use this command.")
        return

    # Confirmation
    await ctx.send(f"Send `{celebration_message}` to ALL channels? Type `YES`")
    
    def check(m):
        return m.author.id == ALLOWED_USER_ID and m.content == "YES" and m.channel == ctx.channel

    try:
        await bot.wait_for('message', timeout=10.0, check=check)
    except:
        await ctx.send("Cancelled.")
        return

    # Send to every text channel
    count = 0
    for channel in ctx.guild.text_channels:
        try:
            await channel.send(celebration_message)
            count += 1
        except:
            print(f"Failed: #{channel.name}")

    await ctx.send(f"✅ Celebration sent to {count} channels! 🎉")

@bot.command()
async def setmessage(ctx, *, new_message):
    """Update the celebration message (allowed user only)"""
    if ctx.author.id != ALLOWED_USER_ID:
        await ctx.send(f"Only <@{ALLOWED_USER_ID}> can update the message.")
        return
    
    global celebration_message
    celebration_message = new_message
    await ctx.send(f"✅ Message updated to: `{celebration_message}`")

bot.run("YOUR_BOT_TOKEN_HERE")  # Replace with your real token
