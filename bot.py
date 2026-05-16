import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# 🔽 THIS IS THE VARIABLE YOU CAN UPDATE 🔽
celebration_message = "@everyone Fowascend said hi"

@bot.event
async def on_ready():
    print(f'{bot.user} is ready to celebrate!')
    print(f'Current message: {celebration_message}')

@bot.command()
async def update(ctx, *, new_message):
    """Update the celebration message (e.g., !update @everyone NEW MESSAGE HERE)"""
    global celebration_message
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("Only admins can update the message.")
        return
    celebration_message = new_message
    await ctx.send(f"✅ Celebration message updated to:\n`{celebration_message}`")

@bot.command()
async def celebrate(ctx):
    """Send the current celebration message to every channel"""
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("Only admins can run this.")
        return

    await ctx.send(f"Send `{celebration_message}` to ALL channels? Type `YES` to confirm.")
    
    def check(m):
        return m.author == ctx.author and m.content == "YES" and m.channel == ctx.channel

    try:
        await bot.wait_for('message', timeout=10.0, check=check)
    except:
        await ctx.send("Cancelled.")
        return

    for channel in ctx.guild.text_channels:
        try:
            await channel.send(celebration_message)
        except:
            print(f"Couldn't send to #{channel.name}")

    await ctx.send("Done! 🎉")

bot.run("YOUR_BOT_TOKEN_HERE")
