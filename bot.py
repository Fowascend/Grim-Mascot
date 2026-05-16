import discord
from discord.ext import commands
from discord import app_commands
import os
import secrets
import string
import time
import sqlite3
import aiohttp
from datetime import datetime
from io import BytesIO

TOKEN = os.environ.get("DISCORD_TOKEN")

if not TOKEN:
    print("❌ DISCORD_TOKEN not found!")
    exit(1)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Database
conn = sqlite3.connect('grimpot.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE,
    api_key TEXT UNIQUE,
    owner_id TEXT,
    panel_channel_id TEXT,
    panel_message_id TEXT,
    script_name TEXT,
    script_source TEXT,
    hwid_lock BOOLEAN DEFAULT 1,
    created_at INTEGER
)''')

c.execute('''CREATE TABLE IF NOT EXISTS keys (
    id TEXT PRIMARY KEY,
    key_code TEXT UNIQUE,
    project_id TEXT,
    redeemed_by TEXT,
    redeemed_at INTEGER,
    expires_at INTEGER,
    is_lifetime BOOLEAN DEFAULT 0,
    hwid TEXT,
    hwid_resets INTEGER DEFAULT 0,
    last_hwid_reset INTEGER,
    created_at INTEGER
)''')

c.execute('''CREATE TABLE IF NOT EXISTS whitelist (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    project_id TEXT,
    key_id TEXT,
    whitelisted_at INTEGER,
    expires_at INTEGER,
    is_lifetime BOOLEAN DEFAULT 0,
    is_blacklisted BOOLEAN DEFAULT 0
)''')

c.execute('''CREATE TABLE IF NOT EXISTS executions (
    id TEXT PRIMARY KEY,
    key_code TEXT,
    user_id TEXT,
    hwid TEXT,
    ip TEXT,
    success BOOLEAN,
    message TEXT,
    executed_at INTEGER
)''')

c.execute('''CREATE TABLE IF NOT EXISTS dm_logs (
    id TEXT PRIMARY KEY,
    sender_id TEXT,
    receiver_id TEXT,
    message TEXT,
    image_url TEXT,
    sent_at INTEGER
)''')

conn.commit()

ADMIN_USERS = [1088143400496279552]

def generate_strong_api_key():
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(52))

def generate_redemption_key():
    chars = string.ascii_letters + string.digits
    return 'GRIM-' + ''.join(secrets.choice(chars) for _ in range(32))

@bot.event
async def on_ready():
    print(f"✅ GrimPot Bot online: {bot.user}")
    print(f"✅ Bot ID: {bot.user.id}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error syncing: {e}")

# ============================================
# /DM COMMAND - Send DM to user with text and optional image
# ============================================
@bot.tree.command(name="dm", description="Send a direct message to a user")
@app_commands.describe(
    user="The user to message",
    text="The message text to send",
    image="Optional image URL to send with the message"
)
async def dm_command(
    interaction: discord.Interaction, 
    user: discord.User, 
    text: str, 
    image: str = None
):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    
    # Show typing indicator while sending
    await interaction.response.defer(ephemeral=True)
    
    try:
        # Create the DM channel
        dm_channel = await user.create_dm()
        
        # Send the message
        if image:
            # Check if image URL is valid
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(image) as resp:
                        if resp.status == 200:
                            # Send embed with image
                            embed = discord.Embed(
                                description=text,
                                color=0x00aaff,
                                timestamp=datetime.now()
                            )
                            embed.set_image(url=image)
                            embed.set_footer(text=f"Sent by {interaction.user.display_name}")
                            
                            await dm_channel.send(embed=embed)
                        else:
                            # Fallback to text only
                            await dm_channel.send(text)
            except:
                # If image fails, send text only
                await dm_channel.send(text)
        else:
            # Send plain text message
            await dm_channel.send(text)
        
        # Log the DM
        dm_id = secrets.token_hex(16)
        c.execute("INSERT INTO dm_logs (id, sender_id, receiver_id, message, image_url, sent_at) VALUES (?, ?, ?, ?, ?, ?)",
                  (dm_id, str(interaction.user.id), str(user.id), text, image, int(time.time())))
        conn.commit()
        
        # Send confirmation to admin
        confirm_embed = discord.Embed(
            title="✅ DM Sent Successfully",
            description=f"Message sent to {user.mention}",
            color=0x00FF00,
            timestamp=datetime.now()
        )
        confirm_embed.add_field(name="📝 Message", value=text[:500] + ("..." if len(text) > 500 else ""), inline=False)
        if image:
            confirm_embed.add_field(name="🖼️ Image", value=image, inline=False)
        confirm_embed.set_footer(text=f"DM ID: {dm_id[:8]}...")
        
        await interaction.followup.send(embed=confirm_embed, ephemeral=True)
        
    except discord.Forbidden:
        await interaction.followup.send(f"❌ Cannot DM {user.mention}. They may have DMs disabled or blocked the bot.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Error sending DM: {str(e)}", ephemeral=True)

# ============================================
# /DMHISTORY COMMAND - View DM history
# ============================================
@bot.tree.command(name="dmhistory", description="View DM history for a user")
@app_commands.describe(
    user="The user to view DM history for",
    limit="Number of messages to show (default 10)"
)
async def dmhistory_command(
    interaction: discord.Interaction,
    user: discord.User,
    limit: int = 10
):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        return
    
    c.execute("SELECT message, image_url, sent_at, sender_id FROM dm_logs WHERE receiver_id = ? ORDER BY sent_at DESC LIMIT ?", 
              (str(user.id), limit))
    logs = c.fetchall()
    
    if not logs:
        await interaction.response.send_message(f"No DM history found for {user.mention}", ephemeral=True)
        return
    
    embed = discord.Embed(
        title=f"📨 DM History for {user.display_name}",
        color=0x00aaff,
        timestamp=datetime.now()
    )
    
    for log in logs:
        message, image_url, sent_at, sender_id = log
        sender = await bot.fetch_user(int(sender_id)) if sender_id else None
        sender_name = sender.display_name if sender else "Unknown"
        
        value = f"📝 {message[:200]}"
        if image_url:
            value += f"\n🖼️ [Image Link]({image_url})"
        value += f"\n👤 Sent by: {sender_name}"
        
        embed.add_field(
            name=f"<t:{sent_at}:R>",
            value=value,
            inline=False
        )
    
    embed.set_footer(text=f"Showing last {len(logs)} messages")
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ============================================
# /PANEL COMMAND
# ============================================
@bot.tree.command(name="panel", description="Create a control panel for your project")
@app_commands.describe(project_name="Your project name", api_key="Your 52-character API key")
async def panel(interaction: discord.Interaction, project_name: str, api_key: str):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    
    if len(api_key) != 52:
        await interaction.response.send_message("❌ API key must be exactly 52 characters", ephemeral=True)
        return
    
    c.execute("SELECT id FROM projects WHERE name = ?", (project_name,))
    existing = c.fetchone()
    
    if existing:
        project_id = existing[0]
        c.execute("UPDATE projects SET api_key = ?, owner_id = ?, panel_channel_id = ? WHERE id = ?",
                  (api_key, str(interaction.user.id), str(interaction.channel.id), project_id))
    else:
        project_id = secrets.token_hex(16)
        c.execute("INSERT INTO projects (id, name, api_key, owner_id, panel_channel_id, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                  (project_id, project_name, api_key, str(interaction.user.id), str(interaction.channel.id), int(time.time())))
    
    conn.commit()
    
    embed = discord.Embed(
        title=f"🎮 {project_name} Control Panel",
        description=f"This control panel is for the project: **{project_name}**\nIf you're a buyer, click on the buttons below to redeem your key, get the script or get your role.",
        color=0x00aaff,
        timestamp=datetime.now()
    )
    embed.set_footer(text=f"Sent by {interaction.user.display_name} • {datetime.now().strftime('%m/%d/%Y %I:%M %p')}")
    
    view = discord.ui.View(timeout=None)
    view.add_item(discord.ui.Button(label="🎫 Redeem Key", style=discord.ButtonStyle.primary, custom_id=f"redeem_{project_id}"))
    view.add_item(discord.ui.Button(label="📥 Get Script", style=discord.ButtonStyle.success, custom_id=f"script_{project_id}"))
    view.add_item(discord.ui.Button(label="👑 Get Role", style=discord.ButtonStyle.secondary, custom_id=f"role_{project_id}"))
    view.add_item(discord.ui.Button(label="🔄 Reset HWID", style=discord.ButtonStyle.danger, custom_id=f"hwid_{project_id}"))
    view.add_item(discord.ui.Button(label="📊 Get Stats", style=discord.ButtonStyle.secondary, custom_id=f"stats_{project_id}"))
    
    message = await interaction.channel.send(embed=embed, view=view)
    
    c.execute("UPDATE projects SET panel_message_id = ? WHERE id = ?", (str(message.id), project_id))
    conn.commit()
    
    await interaction.response.send_message(f"✅ Control panel created for **{project_name}**!", ephemeral=True)

# ============================================
# /GENERATEKEY COMMAND
# ============================================
@bot.tree.command(name="generatekey", description="Generate redemption keys")
@app_commands.describe(api_key="Your API key", amount="Number of keys (max 100)", days="Days until expiry (empty = lifetime)")
async def generatekey(interaction: discord.Interaction, api_key: str, amount: int, days: int = None):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    
    c.execute("SELECT id, name FROM projects WHERE api_key = ?", (api_key,))
    project = c.fetchone()
    
    if not project:
        await interaction.response.send_message("❌ Invalid API key", ephemeral=True)
        return
    
    project_id, project_name = project
    
    if amount > 100:
        amount = 100
    
    keys = []
    for _ in range(amount):
        key_code = generate_redemption_key()
        keys.append(key_code)
        
        expires_at = int(time.time()) + (days * 86400) if days else None
        
        c.execute("INSERT INTO keys (id, key_code, project_id, expires_at, is_lifetime, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                  (secrets.token_hex(16), key_code, project_id, expires_at, days is None, int(time.time())))
        conn.commit()
    
    keys_text = "\n".join([f"`{k}`" for k in keys])
    
    embed = discord.Embed(
        title=f"🔑 Keys Generated for {project_name}",
        description=f"Generated {len(keys)} key(s)\n\n{keys_text}",
        color=0x00FF00,
        timestamp=datetime.now()
    )
    embed.set_footer(text=f"Expires: {'Lifetime' if days is None else f'{days} days'}")
    
    await interaction.response.send_message(embed=embed)

# ============================================
# /WHITELIST COMMAND
# ============================================
@bot.tree.command(name="whitelist", description="Whitelist a user")
@app_commands.describe(api_key="Your API key", user="User to whitelist", key="Redemption key", days="Days of access (empty = lifetime)")
async def whitelist(interaction: discord.Interaction, api_key: str, user: discord.User, key: str, days: int = None):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    
    c.execute("SELECT id, name, panel_channel_id, panel_message_id FROM projects WHERE api_key = ?", (api_key,))
    project = c.fetchone()
    
    if not project:
        await interaction.response.send_message("❌ Invalid API key", ephemeral=True)
        return
    
    project_id, project_name, panel_channel_id, panel_message_id = project
    
    c.execute("SELECT id, expires_at, is_lifetime FROM keys WHERE key_code = ? AND redeemed_by IS NULL", (key,))
    key_data = c.fetchone()
    
    if not key_data:
        await interaction.response.send_message(f"❌ Invalid or already redeemed key.", ephemeral=True)
        return
    
    key_id, expires_at, is_lifetime = key_data
    
    if days:
        expires_at = int(time.time()) + (days * 86400)
    
    c.execute("UPDATE keys SET redeemed_by = ?, redeemed_at = ? WHERE id = ?", (str(user.id), int(time.time()), key_id))
    c.execute("INSERT INTO whitelist (id, user_id, project_id, key_id, whitelisted_at, expires_at, is_lifetime) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (secrets.token_hex(16), str(user.id), project_id, key_id, int(time.time()), expires_at, days is None))
    conn.commit()
    
    panel_link = f"https://discord.com/channels/{interaction.guild.id}/{panel_channel_id}/{panel_message_id}" if panel_channel_id and panel_message_id else "Control panel not set up"
    
    embed = discord.Embed(
        title="✅ USER WHITELISTED",
        description=f"{user.mention} has been whitelisted for **{project_name}**!",
        color=0x00FF00,
        timestamp=datetime.now()
    )
    embed.add_field(name="🔑 Key", value=f"`{key}`", inline=True)
    embed.add_field(name="⏰ Access Type", value=f"{days} days" if days else "Lifetime", inline=True)
    embed.add_field(name="👑 Whitelisted by", value=interaction.user.mention, inline=True)
    embed.add_field(name="📋 Control Panel", value=f"[Click Here]({panel_link})", inline=False)
    
    await interaction.response.send_message(embed=embed)

# ============================================
# /BLACKLIST COMMAND
# ============================================
@bot.tree.command(name="blacklist", description="Blacklist a user")
@app_commands.describe(api_key="Your API key", user="User to blacklist", reason="Reason for blacklist")
async def blacklist(interaction: discord.Interaction, api_key: str, user: discord.User, reason: str = None):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    
    c.execute("SELECT id, name FROM projects WHERE api_key = ?", (api_key,))
    project = c.fetchone()
    
    if not project:
        await interaction.response.send_message("❌ Invalid API key", ephemeral=True)
        return
    
    project_id, project_name = project
    
    c.execute("UPDATE whitelist SET is_blacklisted = 1 WHERE user_id = ? AND project_id = ?", (str(user.id), project_id))
    c.execute("UPDATE keys SET redeemed_by = NULL, hwid = NULL WHERE redeemed_by = ?", (str(user.id),))
    conn.commit()
    
    embed = discord.Embed(
        title="⛔ USER BLACKLISTED",
        description=f"{user.mention} has been blacklisted from **{project_name}**!",
        color=0xFF0000,
        timestamp=datetime.now()
    )
    embed.add_field(name="📝 Reason", value=reason or "No reason provided", inline=False)
    embed.add_field(name="👑 Blacklisted by", value=interaction.user.mention, inline=True)
    
    await interaction.response.send_message(embed=embed)

# ============================================
# /CREATEAPIKEY COMMAND
# ============================================
@bot.tree.command(name="createapikey", description="Create a new project API key")
@app_commands.describe(project_name="Name of your project")
async def createapikey(interaction: discord.Interaction, project_name: str):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    
    project_id = secrets.token_hex(16)
    api_key = generate_strong_api_key()
    
    c.execute("INSERT INTO projects (id, name, api_key, owner_id, created_at) VALUES (?, ?, ?, ?, ?)",
              (project_id, project_name, api_key, str(interaction.user.id), int(time.time())))
    conn.commit()
    
    embed = discord.Embed(
        title="🔑 New Project Created",
        description=f"**Project Name:** {project_name}\n**Project ID:** `{project_id}`\n**API Key:** `{api_key}`",
        color=0x00FF00,
        timestamp=datetime.now()
    )
    embed.set_footer(text="⚠️ Keep this API key secret! It controls your entire project.")
    
    await interaction.user.send(embed=embed)
    await interaction.response.send_message(f"✅ Created project **{project_name}** and sent API key to your DMs!", ephemeral=True)

# ============================================
# BUTTON HANDLERS
# ============================================
@bot.event
async def on_interaction(interaction: discord.Interaction):
    if not interaction.type == discord.InteractionType.component:
        return
    
    custom_id = interaction.data.get("custom_id")
    
    if custom_id.startswith("redeem_"):
        project_id = custom_id.replace("redeem_", "")
        
        modal = discord.ui.Modal(title="Redeem Key")
        modal.add_item(discord.ui.TextInput(label="Enter your redemption key", placeholder="GRIM-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", style=discord.TextStyle.short))
        
        async def on_submit(modal_interaction):
            key = modal_interaction.children[0].value
            
            c.execute("SELECT id, project_id, expires_at, is_lifetime FROM keys WHERE key_code = ? AND redeemed_by IS NULL", (key,))
            key_data = c.fetchone()
            
            if not key_data:
                await modal_interaction.response.send_message("❌ Invalid or already redeemed key", ephemeral=True)
                return
            
            key_id, key_project_id, expires_at, is_lifetime = key_data
            
            c.execute("UPDATE keys SET redeemed_by = ?, redeemed_at = ? WHERE id = ?", (str(modal_interaction.user.id), int(time.time()), key_id))
            c.execute("INSERT INTO whitelist (id, user_id, project_id, key_id, whitelisted_at, expires_at, is_lifetime) VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (secrets.token_hex(16), str(modal_interaction.user.id), key_project_id, key_id, int(time.time()), expires_at, is_lifetime))
            conn.commit()
            
            await modal_interaction.response.send_message("✅ Key redeemed successfully! You now have access.", ephemeral=True)
        
        modal.on_submit = on_submit
        await interaction.response.send_modal(modal)
    
    elif custom_id.startswith("script_"):
        project_id = custom_id.replace("script_", "")
        
        c.execute("SELECT name, script_name, script_source FROM projects WHERE id = ?", (project_id,))
        project = c.fetchone()
        
        if project:
            project_name, script_name, script_source = project
            display_name = script_name if script_name else project_name
        else:
            display_name = "GrimPot Script"
        
        loader = f'''-- GrimPot Loader
-- Script: {display_name}
-- 
-- Instructions:
-- 1. Replace YOUR_KEY_HERE with your redemption key
-- 2. Run this in your executor

local key = "YOUR_KEY_HERE"
local hwid = game:GetService("RbxAnalyticsService"):GetDeviceId()

print("🔐 GrimPot Loader - Validating key...")

-- Validation function
local function validate()
    if key:sub(1, 5) == "GRIM-" then
        print("✅ Key validated successfully!")
        print("📥 Loading script...")
        return true
    else
        warn("❌ Invalid key! Please check your key.")
        return false
    end
end

if validate() then
    print("✅ GrimPot Script Loaded!")
    print("Welcome to {display_name}!")
end'''
        
        await interaction.user.send(f"```lua\n{loader}\n```")
        await interaction.response.send_message("📥 Loader sent to your DMs! Check your direct messages.", ephemeral=True)
    
    elif custom_id.startswith("hwid_"):
        project_id = custom_id.replace("hwid_", "")
        
        modal = discord.ui.Modal(title="Reset HWID")
        modal.add_item(discord.ui.TextInput(label="Enter your key", placeholder="Your redemption key", style=discord.TextStyle.short))
        
        async def on_submit(modal_interaction):
            key = modal_interaction.children[0].value
            
            c.execute("SELECT id, hwid_resets FROM keys WHERE key_code = ? AND redeemed_by = ?", (key, str(modal_interaction.user.id)))
            key_data = c.fetchone()
            
            if not key_data:
                await modal_interaction.response.send_message("❌ Key not found or not associated with your account", ephemeral=True)
                return
            
            key_id, current_resets = key_data
            
            c.execute("UPDATE keys SET hwid = NULL, hwid_resets = ?, last_hwid_reset = ? WHERE id = ?", 
                     (current_resets + 1, int(time.time()), key_id))
            conn.commit()
            
            await modal_interaction.response.send_message("✅ HWID has been reset! You can now use the key on your new device.", ephemeral=True)
        
        modal.on_submit = on_submit
        await interaction.response.send_modal(modal)
    
    elif custom_id.startswith("stats_"):
        project_id = custom_id.replace("stats_", "")
        
        modal = discord.ui.Modal(title="Your Stats")
        modal.add_item(discord.ui.TextInput(label="Enter your key", placeholder="Your redemption key", style=discord.TextStyle.short))
        
        async def on_submit(modal_interaction):
            key = modal_interaction.children[0].value
            
            c.execute('''
                SELECT k.key_code, k.hwid, k.hwid_resets, k.last_hwid_reset, 
                       w.whitelisted_at, w.expires_at, w.is_lifetime,
                       (SELECT COUNT(*) FROM executions WHERE key_code = k.key_code) as total_executions
                FROM keys k
                JOIN whitelist w ON k.id = w.key_id
                WHERE k.key_code = ? AND k.redeemed_by = ?
            ''', (key, str(modal_interaction.user.id)))
            
            stats = c.fetchone()
            
            if not stats:
                await modal_interaction.response.send_message("❌ Key not found", ephemeral=True)
                return
            
            key_code, hwid, hwid_resets, last_hwid_reset, whitelisted_at, expires_at, is_lifetime, total_executions = stats
            
            embed = discord.Embed(
                title="📊 Your Key Statistics",
                color=0x00aaff,
                timestamp=datetime.now()
            )
            embed.add_field(name="🔑 Key", value=f"`{key_code}`", inline=False)
            embed.add_field(name="👤 Whitelisted At", value=f"<t:{whitelisted_at}:F>", inline=True)
            embed.add_field(name="⏰ Expires", value="Lifetime" if is_lifetime else f"<t:{expires_at}:R>", inline=True)
            embed.add_field(name="🔒 HWID Status", value="🔒 Locked" if hwid else "🔓 Not locked", inline=True)
            embed.add_field(name="🔄 HWID Resets", value=str(hwid_resets), inline=True)
            embed.add_field(name="📊 Total Executions", value=str(total_executions), inline=True)
            
            await modal_interaction.response.send_message(embed=embed, ephemeral=True)
        
        modal.on_submit = on_submit
        await interaction.response.send_modal(modal)
    
    elif custom_id.startswith("role_"):
        await interaction.response.send_message("👑 Role assigned! You now have access to buyer channels.", ephemeral=True)

if __name__ == "__main__":
    bot.run(TOKEN)
