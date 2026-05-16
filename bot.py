import discord
from discord.ext import commands
from discord import app_commands
import os
import secrets
import time
import sqlite3
import requests
from datetime import datetime

TOKEN = os.environ.get("DISCORD_TOKEN")
API_URL = os.environ.get("API_URL", "http://localhost:5000")

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
    created_at INTEGER
)''')

c.execute('''CREATE TABLE IF NOT EXISTS whitelist (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    project_id TEXT,
    key_id TEXT,
    whitelisted_at INTEGER,
    expires_at INTEGER,
    is_lifetime BOOLEAN DEFAULT 0
)''')

conn.commit()

ADMIN_USERS = [1088143400496279552]  # Your Discord ID

def generate_key():
    return secrets.token_hex(16).upper()

def generate_api_key():
    return secrets.token_hex(26)

@bot.event
async def on_ready():
    print(f"✅ GrimPot Bot online: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error: {e}")

# ============================================
# CONTROL PANEL COMMAND (Creates embed with buttons)
# ============================================
@bot.tree.command(name="panel", description="Create the control panel in this channel")
async def panel(interaction: discord.Interaction):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="🎮 GrimPot Control Panel",
        description="This control panel is for the project: **GrimPot Licensing**\n\nIf you're a buyer, click on the buttons below to redeem your key, get the script or manage your HWID.",
        color=0x00aaff,
        timestamp=datetime.now()
    )
    embed.set_footer(text="GrimPot • Premium License System")
    
    view = discord.ui.View(timeout=None)
    
    view.add_item(discord.ui.Button(label="🎫 Redeem Key", style=discord.ButtonStyle.primary, custom_id="redeem_key"))
    view.add_item(discord.ui.Button(label="📥 Get Script", style=discord.ButtonStyle.success, custom_id="get_script"))
    view.add_item(discord.ui.Button(label="👑 Get Role", style=discord.ButtonStyle.secondary, custom_id="get_role"))
    view.add_item(discord.ui.Button(label="🔄 Reset HWID", style=discord.ButtonStyle.danger, custom_id="reset_hwid"))
    view.add_item(discord.ui.Button(label="📊 Get Stats", style=discord.ButtonStyle.secondary, custom_id="get_stats"))
    
    await interaction.response.send_message(embed=embed, view=view)

# ============================================
# BUTTON HANDLERS
# ============================================
@bot.event
async def on_interaction(interaction: discord.Interaction):
    if not interaction.type == discord.InteractionType.component:
        return
    
    custom_id = interaction.data.get("custom_id")
    
    if custom_id == "redeem_key":
        modal = discord.ui.Modal(title="Redeem Key")
        modal.add_item(discord.ui.TextInput(label="Enter your key", placeholder="GRIM-XXXX-XXXX", style=discord.TextStyle.short))
        
        async def on_submit(modal_interaction):
            key = modal_interaction.children[0].value
            
            # Validate key with API
            response = requests.post(f"{API_URL}/api/validate", json={"key": key, "discord_id": str(modal_interaction.user.id)})
            data = response.json()
            
            if data.get("code") == "VALID":
                await modal_interaction.response.send_message(f"✅ Key redeemed successfully! You now have access.", ephemeral=True)
            else:
                await modal_interaction.response.send_message(f"❌ {data.get('message', 'Invalid key')}", ephemeral=True)
        
        modal.on_submit = on_submit
        await interaction.response.send_modal(modal)
    
    elif custom_id == "get_script":
        await interaction.response.send_message("📥 Check your DMs for the loader script!", ephemeral=True)
        
        loader_script = f'''
-- GrimPot Loader
local key = "YOUR_KEY_HERE"
local hwid = game:GetService("RbxAnalyticsService"):GetDeviceId()

local response = syn and syn.request or request or http_request
local data = response({{
    Url = "{API_URL}/api/validate",
    Method = "POST",
    Headers = {{["Content-Type"] = "application/json"}},
    Body = game:GetService("HttpService"):JSONEncode({{key = key, hwid = hwid}})
}})

local result = game:GetService("HttpService"):JSONDecode(data.Body)
if result.code == "VALID" then
    print("✅ GrimPot: Key valid!")
    loadstring(result.script)()
else
    warn("❌ GrimPot: " .. result.message)
end
'''
        await interaction.user.send(f"```lua\n{loader_script}\n```")
    
    elif custom_id == "get_role":
        await interaction.response.send_message("👑 Role assigned! You now have access to buyer channels.", ephemeral=True)
        # Add role logic here
    
    elif custom_id == "reset_hwid":
        await interaction.response.send_message("🔄 HWID reset requested. Please provide your key:", ephemeral=True)
        # HWID reset logic
    
    elif custom_id == "get_stats":
        await interaction.response.send_message("📊 Fetching your stats...", ephemeral=True)
        # Stats logic

# ============================================
# /GENERATEKEY - DMs the keys
# ============================================
@bot.tree.command(name="generatekey", description="Generate keys (sent via DM)")
@app_commands.describe(amount="Number of keys", days="Days until expiry (empty = lifetime)")
async def generatekey(interaction: discord.Interaction, amount: int, days: int = None):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    
    keys = []
    for _ in range(amount):
        key_code = generate_key()
        keys.append(key_code)
        
        # Store in database
        c.execute("INSERT INTO keys (id, key_code, expires_at, is_lifetime, created_at) VALUES (?, ?, ?, ?, ?)",
                  (secrets.token_hex(16), key_code, 
                   int(time.time()) + (days * 86400) if days else None,
                   days is None, int(time.time())))
        conn.commit()
    
    # Send keys via DM
    keys_text = "\n".join([f"`{k}`" for k in keys])
    try:
        await interaction.user.send(f"🔑 **Generated {amount} Key(s)**\n\n{keys_text}\n\n⚠️ Keep these safe! Do not share publicly.")
    except:
        await interaction.response.send_message("❌ I can't DM you. Please enable DMs from server members.", ephemeral=True)
        return
    
    await interaction.response.send_message(f"✅ Generated {amount} key(s) and sent them to your DMs!", ephemeral=True)

# ============================================
# /WHITELIST - Silent, no embed
# ============================================
@bot.tree.command(name="whitelist", description="Whitelist a user (silent)")
@app_commands.describe(user="User to whitelist", days="Days of access (empty = lifetime)")
async def whitelist(interaction: discord.Interaction, user: discord.User, days: int = None):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    
    # Get an unused key
    c.execute("SELECT key_code FROM keys WHERE redeemed_by IS NULL LIMIT 1")
    key_data = c.fetchone()
    
    if not key_data:
        await interaction.response.send_message(f"❌ No available keys. Generate some with /generatekey first.", ephemeral=True)
        return
    
    key_code = key_data[0]
    
    # Mark key as redeemed
    c.execute("UPDATE keys SET redeemed_by = ? WHERE key_code = ?", (str(user.id), key_code))
    c.execute("INSERT INTO whitelist (id, user_id, key_id, expires_at, is_lifetime, whitelisted_at) VALUES (?, ?, ?, ?, ?, ?)",
              (secrets.token_hex(16), str(user.id), key_code,
               int(time.time()) + (days * 86400) if days else None,
               days is None, int(time.time())))
    conn.commit()
    
    # Silent response (no embed, just a simple message)
    await interaction.response.send_message(f"✅ Whitelisted {user.mention}", ephemeral=True)

# ============================================
# /BLACKLIST - Silent, no embed
# ============================================
@bot.tree.command(name="blacklist", description="Blacklist a user (silent)")
@app_commands.describe(user="User to blacklist", reason="Reason for blacklist")
async def blacklist(interaction: discord.Interaction, user: discord.User, reason: str = None):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    
    # Find user's key
    c.execute("SELECT key_code FROM keys WHERE redeemed_by = ?", (str(user.id),))
    key_data = c.fetchone()
    
    if key_data:
        key_code = key_data[0]
        c.execute("UPDATE keys SET redeemed_by = NULL WHERE key_code = ?", (key_code,))
        c.execute("DELETE FROM whitelist WHERE user_id = ?", (str(user.id),))
        conn.commit()
    
    await interaction.response.send_message(f"⛔ Blacklisted {user.mention}", ephemeral=True)

# ============================================
# /CREATEPROJECT - Creates a new project with API key
# ============================================
@bot.tree.command(name="createproject", description="Create a new project")
@app_commands.describe(name="Project name")
async def createproject(interaction: discord.Interaction, name: str):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    
    project_id = secrets.token_hex(16)
    api_key = generate_api_key()
    
    c.execute("INSERT INTO projects (id, name, api_key, owner_id, created_at) VALUES (?, ?, ?, ?, ?)",
              (project_id, name, api_key, str(interaction.user.id), int(time.time())))
    conn.commit()
    
    # Send API key via DM
    try:
        await interaction.user.send(f"🔑 **New Project Created: {name}**\n\n**API Key:** `{api_key}`\n\n⚠️ Keep this key secret! It controls your entire project.")
    except:
        pass
    
    await interaction.response.send_message(f"✅ Created project **{name}** and sent API key to your DMs!", ephemeral=True)

# ============================================
# /APIINFO - Show your API key
# ============================================
@bot.tree.command(name="apiinfo", description="Get your project API key")
async def apiinfo(interaction: discord.Interaction):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    
    c.execute("SELECT name, api_key FROM projects WHERE owner_id = ?", (str(interaction.user.id),))
    projects = c.fetchall()
    
    if not projects:
        await interaction.response.send_message("No projects found. Create one with /createproject", ephemeral=True)
        return
    
    info = "\n".join([f"**{p[0]}**: `{p[1]}`" for p in projects])
    await interaction.user.send(f"🔑 **Your API Keys**\n\n{info}\n\n⚠️ Keep these safe!")
    await interaction.response.send_message("✅ Sent API keys to your DMs!", ephemeral=True)

if __name__ == "__main__":
    bot.run(TOKEN)
