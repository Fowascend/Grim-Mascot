import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} is ready to celebrate!')

@bot.command()
async def celebrate(ctx):
    """Sends '@everyone Fowascend said hi' to every text channel (admins only)"""
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("Only admins can run this.")
        return

    # Confirm once
    await ctx.send("Sending celebration to ALL channels. Type `YES` to confirm.")
    def check(m):
        return m.author == ctx.author and m.content == "YES" and m.channel == ctx.channel

    try:
        await bot.wait_for('message', timeout=10.0, check=check)
    except:
        await ctx.send("Cancelled.")
        return

    # Send to every text channel
    for channel in ctx.guild.text_channels:
        try:
            await channel.send("@everyone Fowascend said hi")
        except:
            print(f"Couldn't send to #{channel.name}")

    await ctx.send("Done! 🎉")

bot.run("YOUR_BOT_TOKEN_HERE")
