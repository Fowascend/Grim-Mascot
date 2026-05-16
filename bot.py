import discord
from discord.ext import commands
from discord import app_commands
import os
import secrets
import string
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
    panel_channel_id TEXT,
    panel_message_id TEXT,
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
    is_lifetime BOOLEAN DEFAULT 0
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

conn.commit()

ADMIN_USERS = [1088143400496279552]

def generate_strong_api_key():
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(52))

def generate_redemption_key():
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(32))

@bot.event
async def on_ready():
    print(f"✅ GrimPot Bot online: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error: {e}")

# ============================================
# /PANEL
# ============================================
@bot.tree.command(name="panel", description="Create a control panel for your project")
@app_commands.describe(project_id="Your project ID", api_key="Your 52-character API key")
async def panel(interaction: discord.Interaction, project_id: str, api_key: str):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    
    response = requests.post(f"{API_URL}/api/validate_project", json={"project_id": project_id, "api_key": api_key})
    data = response.json()
    
    if not data.get("valid"):
        await interaction.response.send_message(f"❌ Invalid project ID or API key", ephemeral=True)
        return
    
    project_name = data.get("project_name")
    
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
    
    c.execute("INSERT OR REPLACE INTO projects (id, name, api_key, owner_id, panel_channel_id, panel_message_id, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (project_id, project_name, api_key, str(interaction.user.id), str(interaction.channel.id), str(message.id), int(time.time())))
    conn.commit()
    
    await interaction.response.send_message(f"✅ Control panel created for **{project_name}**!", ephemeral=True)

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
        modal.add_item(discord.ui.TextInput(label="Enter your redemption key", placeholder="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", style=discord.TextStyle.short))
        
        async def on_submit(modal_interaction):
            key = modal_interaction.children[0].value
            
            response = requests.post(f"{API_URL}/api/redeem_key", json={"key": key, "discord_id": str(modal_interaction.user.id)})
            data = response.json()
            
            if data.get("success"):
                await modal_interaction.response.send_message(f"✅ {data.get('message')}", ephemeral=True)
            else:
                await modal_interaction.response.send_message(f"❌ {data.get('message')}", ephemeral=True)
        
        modal.on_submit = on_submit
        await interaction.response.send_modal(modal)
    
    elif custom_id.startswith("script_"):
        project_id = custom_id.replace("script_", "")
        
        modal = discord.ui.Modal(title="Get Script")
        modal.add_item(discord.ui.TextInput(label="Enter your key (optional)", placeholder="Leave empty for free script", required=False, style=discord.TextStyle.short))
        
        async def on_submit(modal_interaction):
            user_key = modal_interaction.children[0].value
            
            if user_key:
                loader = f'''-- GrimPot Loader (Paid)
script_key = "{user_key}"
loadstring(game:HttpGet("{API_URL}/api/load_script?project={project_id}&key={user_key}"))()
'''
            else:
                loader = f'''-- GrimPot Loader (Free Trial)
loadstring(game:HttpGet("{API_URL}/api/load_script?project={project_id}&free=true"))()
'''
            
            await modal_interaction.user.send(f"```lua\n{loader}\n```")
            await modal_interaction.response.send_message("📥 Loader sent to your DMs!", ephemeral=True)
        
        modal.on_submit = on_submit
        await interaction.response.send_modal(modal)
    
    elif custom_id.startswith("hwid_"):
        project_id = custom_id.replace("hwid_", "")
        
        modal = discord.ui.Modal(title="Reset HWID")
        modal.add_item(discord.ui.TextInput(label="Enter your key", placeholder="Your redemption key", style=discord.TextStyle.short))
        
        async def on_submit(modal_interaction):
            key = modal_interaction.children[0].value
            
            response = requests.post(f"{API_URL}/api/reset_hwid", json={"key": key, "discord_id": str(modal_interaction.user.id)})
            data = response.json()
            
            if data.get("success"):
                await modal_interaction.response.send_message(f"✅ {data.get('message')}", ephemeral=True)
            else:
                await modal_interaction.response.send_message(f"❌ {data.get('message')}", ephemeral=True)
        
        modal.on_submit = on_submit
        await interaction.response.send_modal(modal)
    
    elif custom_id.startswith("stats_"):
        project_id = custom_id.replace("stats_", "")
        
        modal = discord.ui.Modal(title="Your Stats")
        modal.add_item(discord.ui.TextInput(label="Enter your key", placeholder="Your redemption key", style=discord.TextStyle.short))
        
        async def on_submit(modal_interaction):
            key = modal_interaction.children[0].value
            
            response = requests.post(f"{API_URL}/api/user_stats", json={"key": key, "discord_id": str(modal_interaction.user.id)})
            data = response.json()
            
            if data.get("success"):
                stats = data.get("stats")
                
                embed = discord.Embed(
                    title="📊 Your Key Statistics",
                    color=0x00aaff,
                    timestamp=datetime.now()
                )
                embed.add_field(name="🔑 Key", value=f"`{stats.get('key_code', 'N/A')}`", inline=False)
                embed.add_field(name="👤 Whitelisted At", value=f"<t:{stats.get('whitelisted_at', 0)}:F>", inline=True)
                embed.add_field(name="⏰ Expires", value=stats.get('expires', 'Lifetime'), inline=True)
                embed.add_field(name="🔒 HWID Status", value=stats.get('hwid_status', 'Not locked'), inline=True)
                embed.add_field(name="🔄 HWID Resets", value=str(stats.get('hwid_resets', 0)), inline=True)
                embed.add_field(name="📊 Total Executions", value=str(stats.get('total_executions', 0)), inline=True)
                
                await modal_interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await modal_interaction.response.send_message(f"❌ {data.get('message')}", ephemeral=True)
        
        modal.on_submit = on_submit
        await interaction.response.send_modal(modal)
    
    elif custom_id.startswith("role_"):
        await interaction.response.send_message("👑 Role assigned! You now have access to buyer channels.", ephemeral=True)

# ============================================
# /GENERATEKEY
# ============================================
@bot.tree.command(name="generatekey", description="Generate redemption keys (sent via DM)")
@app_commands.describe(amount="Number of keys", days="Days until expiry (empty = lifetime)", project="Project ID")
async def generatekey(interaction: discord.Interaction, amount: int, days: int = None, project: str = None):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    
    keys = []
    for _ in range(amount):
        key_code = generate_redemption_key()
        keys.append(key_code)
        
        expires_at = int(time.time()) + (days * 86400) if days else None
        
        c.execute("INSERT INTO keys (id, key_code, project_id, expires_at, is_lifetime, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                  (secrets.token_hex(16), key_code, project, expires_at, days is None, int(time.time())))
        conn.commit()
    
    keys_text = "\n".join([f"`{k}`" for k in keys])
    
    try:
        await interaction.user.send(f"🔑 **Generated {amount} Key(s) for {project or 'All projects'}**\n\n{keys_text}\n\n📅 Expires: {'Lifetime' if days is None else f'{days} days'}\n\n⚠️ Keep these safe!")
    except:
        await interaction.response.send_message("❌ I can't DM you. Please enable DMs.", ephemeral=True)
        return
    
    await interaction.response.send_message(f"✅ Generated {amount} key(s) and sent to your DMs!", ephemeral=True)

# ============================================
# /WHITELIST
# ============================================
@bot.tree.command(name="whitelist", description="Whitelist a user")
@app_commands.describe(user="User to whitelist", key="Redemption key", days="Days of access (empty = lifetime)")
async def whitelist(interaction: discord.Interaction, user: discord.User, key: str, days: int = None):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    
    c.execute("SELECT id, project_id, expires_at FROM keys WHERE key_code = ? AND redeemed_by IS NULL", (key,))
    key_data = c.fetchone()
    
    if not key_data:
        await interaction.response.send_message(f"❌ Invalid or already redeemed key.", ephemeral=True)
        return
    
    key_id, project_id, expires_at = key_data
    
    if days:
        expires_at = int(time.time()) + (days * 86400)
    
    c.execute("UPDATE keys SET redeemed_by = ?, redeemed_at = ? WHERE id = ?", (str(user.id), int(time.time()), key_id))
    c.execute("INSERT INTO whitelist (id, user_id, project_id, key_id, whitelisted_at, expires_at, is_lifetime) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (secrets.token_hex(16), str(user.id), project_id, key_id, int(time.time()), expires_at, days is None))
    conn.commit()
    
    await interaction.response.send_message(f"✅ Whitelisted {user.mention}", ephemeral=True)

# ============================================
# /BLACKLIST
# ============================================
@bot.tree.command(name="blacklist", description="Blacklist a user")
@app_commands.describe(user="User to blacklist", reason="Reason for blacklist")
async def blacklist(interaction: discord.Interaction, user: discord.User, reason: str = None):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    
    c.execute("SELECT key_code FROM keys WHERE redeemed_by = ?", (str(user.id),))
    key_data = c.fetchone()
    
    if key_data:
        key_code = key_data[0]
        c.execute("UPDATE keys SET redeemed_by = NULL, hwid = NULL WHERE key_code = ?", (key_code,))
        c.execute("DELETE FROM whitelist WHERE user_id = ?", (str(user.id),))
        conn.commit()
    
    await interaction.response.send_message(f"⛔ Blacklisted {user.mention}", ephemeral=True)

# ============================================
# /CREATEAPIKEY
# ============================================
@bot.tree.command(name="createapikey", description="Generate a new 52-character API key for a project")
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
    
    await interaction.user.send(f"🔑 **New Project Created: {project_name}**\n\n**Project ID:** `{project_id}`\n**API Key:** `{api_key}`\n\n⚠️ Keep this key secret!")
    await interaction.response.send_message(f"✅ Created project **{project_name}** and sent API key to your DMs!", ephemeral=True)

if __name__ == "__main__":
    bot.run(TOKEN)
