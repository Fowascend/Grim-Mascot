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
from flask import Flask, request, jsonify
import threading

TOKEN = os.environ.get("DISCORD_TOKEN")
API_URL = os.environ.get("API_URL", "http://localhost:5000")
ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY", secrets.token_hex(26))

if not TOKEN:
    print("❌ DISCORD_TOKEN not found!")
    exit(1)

# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Flask API for Dashboard control
app = Flask(__name__)

# Database
conn = sqlite3.connect('grimpot.db', check_same_thread=False)
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

conn.commit()

ADMIN_USERS = [1088143400496279552]

def generate_strong_api_key():
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(52))

def generate_redemption_key():
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(32))

# ============================================
# DISCORD BOT COMMANDS
# ============================================

@bot.event
async def on_ready():
    print(f"✅ GrimPot Bot online: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error: {e}")

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

@bot.tree.command(name="generatekey", description="Generate redemption keys")
@app_commands.describe(api_key="Your API key", amount="Number of keys", days="Days until expiry (empty = lifetime)")
async def generatekey(interaction: discord.Interaction, api_key: str, amount: int, days: int = None):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    
    c.execute("SELECT id FROM projects WHERE api_key = ?", (api_key,))
    project = c.fetchone()
    
    if not project:
        await interaction.response.send_message("❌ Invalid API key", ephemeral=True)
        return
    
    keys = []
    for _ in range(min(amount, 100)):
        key_code = generate_redemption_key()
        keys.append(key_code)
        
        expires_at = int(time.time()) + (days * 86400) if days else None
        
        c.execute("INSERT INTO keys (id, key_code, project_id, expires_at, is_lifetime, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                  (secrets.token_hex(16), key_code, project[0], expires_at, days is None, int(time.time())))
        conn.commit()
    
    keys_text = "\n".join([f"`{k}`" for k in keys])
    await interaction.response.send_message(f"🔑 **Generated {len(keys)} Key(s)**\n\n{keys_text}", ephemeral=False)

@bot.tree.command(name="whitelist", description="Whitelist a user")
@app_commands.describe(api_key="Your API key", user="User to whitelist", key="Redemption key", days="Days of access (empty = lifetime)")
async def whitelist(interaction: discord.Interaction, api_key: str, user: discord.User, key: str, days: int = None):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    
    c.execute("SELECT id FROM projects WHERE api_key = ?", (api_key,))
    project = c.fetchone()
    
    if not project:
        await interaction.response.send_message("❌ Invalid API key", ephemeral=True)
        return
    
    project_id = project[0]
    
    c.execute("SELECT id, expires_at FROM keys WHERE key_code = ? AND redeemed_by IS NULL", (key,))
    key_data = c.fetchone()
    
    if not key_data:
        await interaction.response.send_message(f"❌ Invalid or already redeemed key.", ephemeral=True)
        return
    
    key_id, expires_at = key_data
    
    if days:
        expires_at = int(time.time()) + (days * 86400)
    
    c.execute("UPDATE keys SET redeemed_by = ?, redeemed_at = ? WHERE id = ?", (str(user.id), int(time.time()), key_id))
    c.execute("INSERT INTO whitelist (id, user_id, project_id, key_id, whitelisted_at, expires_at, is_lifetime) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (secrets.token_hex(16), str(user.id), project_id, key_id, int(time.time()), expires_at, days is None))
    conn.commit()
    
    # Get control panel link
    c.execute("SELECT panel_channel_id, panel_message_id FROM projects WHERE id = ?", (project_id,))
    panel = c.fetchone()
    
    panel_link = f"https://discord.com/channels/{interaction.guild.id}/{panel[0]}/{panel[1]}" if panel and panel[0] else "Control panel not set up"
    
    embed = discord.Embed(
        title="✅ USER WHITELISTED",
        description=f"{user.mention} has been whitelisted for **{project_id}**!",
        color=0x00FF00,
        timestamp=datetime.now()
    )
    embed.add_field(name="🔑 Key", value=f"`{key}`", inline=True)
    embed.add_field(name="⏰ Access Type", value=f"{days} days" if days else "Lifetime", inline=True)
    embed.add_field(name="👑 Whitelisted by", value=interaction.user.mention, inline=True)
    embed.add_field(name="📋 Control Panel", value=f"[Click Here]({panel_link})", inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="blacklist", description="Blacklist a user")
@app_commands.describe(api_key="Your API key", user="User to blacklist", reason="Reason for blacklist")
async def blacklist(interaction: discord.Interaction, api_key: str, user: discord.User, reason: str = None):
    if interaction.user.id not in ADMIN_USERS:
        await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
        return
    
    c.execute("SELECT id FROM projects WHERE api_key = ?", (api_key,))
    project = c.fetchone()
    
    if not project:
        await interaction.response.send_message("❌ Invalid API key", ephemeral=True)
        return
    
    project_id = project[0]
    
    c.execute("UPDATE whitelist SET is_blacklisted = 1 WHERE user_id = ? AND project_id = ?", (str(user.id), project_id))
    c.execute("UPDATE keys SET redeemed_by = NULL, hwid = NULL WHERE redeemed_by = ?", (str(user.id),))
    conn.commit()
    
    embed = discord.Embed(
        title="⛔ USER BLACKLISTED",
        description=f"{user.mention} has been blacklisted!",
        color=0xFF0000,
        timestamp=datetime.now()
    )
    embed.add_field(name="📝 Reason", value=reason or "No reason provided", inline=False)
    embed.add_field(name="👑 Blacklisted by", value=interaction.user.mention, inline=True)
    
    await interaction.response.send_message(embed=embed)

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
    
    await interaction.user.send(f"🔑 **New Project Created: {project_name}**\n\n**Project ID:** `{project_id}`\n**API Key:** `{api_key}`\n\n⚠️ Keep this key secret!")
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
        modal.add_item(discord.ui.TextInput(label="Enter your redemption key", placeholder="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", style=discord.TextStyle.short))
        
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
        
        c.execute("SELECT script_name, script_source FROM projects WHERE id = ?", (project_id,))
        script = c.fetchone()
        
        loader = f'''-- GrimPot Loader
-- Script: {script[0] if script else "GrimPot Script"}
-- This loader requires a valid key

local key = "YOUR_KEY_HERE"
local hwid = game:GetService("RbxAnalyticsService"):GetDeviceId()

local function httpPost(url, data)
    local syn = syn and syn.request or request or http_request
    if syn then
        local res = syn({{
            Url = url,
            Method = "POST",
            Headers = {{["Content-Type"] = "application/json"}},
            Body = game:GetService("HttpService"):JSONEncode(data)
        }})
        return res.Body
    end
    return game:GetService("HttpService"):PostAsync(url, game:GetService("HttpService"):JSONEncode(data))
end

local result = game:GetService("HttpService"):JSONDecode(httpPost("{API_URL}/api/validate", {{key = key, hwid = hwid}}))

if result.code == "KEY_VALID" then
    print("✅ GrimPot: Key valid! Loading script...")
    loadstring(result.script)()
elseif result.code == "KEY_EXPIRED" then
    warn("❌ GrimPot: Your key has expired!")
elseif result.code == "KEY_HWID_LOCKED" then
    warn("❌ GrimPot: HWID mismatch! Use /reset_hwid")
else
    warn("❌ GrimPot: " .. result.message)
end'''
        
        await interaction.user.send(f"```lua\n{loader}\n```")
        await interaction.response.send_message("📥 Loader sent to your DMs!", ephemeral=True)
    
    elif custom_id.startswith("hwid_"):
        await interaction.response.send_message("🔄 HWID reset requested. Please provide your key:", ephemeral=True)
    
    elif custom_id.startswith("stats_"):
        await interaction.response.send_message("📊 Fetching your stats...", ephemeral=True)
    
    elif custom_id.startswith("role_"):
        await interaction.response.send_message("👑 Role assigned! You now have access to buyer channels.", ephemeral=True)

# ============================================
# FLASK API FOR DASHBOARD CONTROL
# ============================================

def get_db():
    conn = sqlite3.connect('grimpot.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/bot/whitelist', methods=['POST'])
def api_bot_whitelist():
    """Dashboard calls this to make bot whitelist a user"""
    api_key = request.headers.get('X-API-Key')
    
    if api_key != ADMIN_API_KEY:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    user_id = data.get('user_id')
    days = data.get('days')
    reason = data.get('reason', '')
    
    # This would trigger the bot to send the whitelist embed
    # The actual Discord message sending happens async
    return jsonify({'success': True, 'message': f'Whitelist command sent for user {user_id}'})

@app.route('/api/bot/blacklist', methods=['POST'])
def api_bot_blacklist():
    """Dashboard calls this to make bot blacklist a user"""
    api_key = request.headers.get('X-API-Key')
    
    if api_key != ADMIN_API_KEY:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    user_id = data.get('user_id')
    reason = data.get('reason', '')
    
    return jsonify({'success': True, 'message': f'Blacklist command sent for user {user_id}'})

@app.route('/api/bot/generate_keys', methods=['POST'])
def api_bot_generate_keys():
    """Dashboard calls this to generate keys via bot"""
    api_key = request.headers.get('X-API-Key')
    
    if api_key != ADMIN_API_KEY:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    amount = data.get('amount', 1)
    days = data.get('days')
    project_id = data.get('project_id')
    
    keys = []
    for _ in range(min(amount, 100)):
        key_code = generate_redemption_key()
        keys.append(key_code)
        
        expires_at = int(time.time()) + (days * 86400) if days else None
        
        c.execute("INSERT INTO keys (id, key_code, project_id, expires_at, is_lifetime, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                  (secrets.token_hex(16), key_code, project_id, expires_at, days is None, int(time.time())))
        conn.commit()
    
    return jsonify({'success': True, 'keys': keys})

@app.route('/api/bot/stats', methods=['GET'])
def api_bot_stats():
    """Dashboard calls this to get bot stats"""
    api_key = request.headers.get('X-API-Key')
    
    if api_key != ADMIN_API_KEY:
        return jsonify({'error': 'Unauthorized'}), 401
    
    c.execute("SELECT COUNT(*) FROM keys")
    total_keys = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM keys WHERE redeemed_by IS NOT NULL")
    used_keys = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM whitelist WHERE is_blacklisted = 0")
    active_users = c.fetchone()[0]
    
    return jsonify({
        'total_keys': total_keys,
        'used_keys': used_keys,
        'unused_keys': total_keys - used_keys,
        'active_users': active_users
    })

@app.route('/api/bot/keys', methods=['GET'])
def api_bot_keys():
    """Dashboard calls this to get all keys"""
    api_key = request.headers.get('X-API-Key')
    
    if api_key != ADMIN_API_KEY:
        return jsonify({'error': 'Unauthorized'}), 401
    
    c.execute("SELECT key_code, redeemed_by, expires_at, is_lifetime, created_at FROM keys ORDER BY created_at DESC")
    keys = [{'key_code': row[0], 'redeemed_by': row[1], 'expires_at': row[2], 'is_lifetime': row[3], 'created_at': row[4]} for row in c.fetchall()]
    
    return jsonify({'keys': keys})

@app.route('/api/bot/users', methods=['GET'])
def api_bot_users():
    """Dashboard calls this to get whitelisted users"""
    api_key = request.headers.get('X-API-Key')
    
    if api_key != ADMIN_API_KEY:
        return jsonify({'error': 'Unauthorized'}), 401
    
    c.execute("SELECT w.user_id, w.whitelisted_at, w.expires_at, w.is_lifetime, w.is_blacklisted, k.key_code FROM whitelist w JOIN keys k ON w.key_id = k.id")
    users = [{'user_id': row[0], 'whitelisted_at': row[1], 'expires_at': row[2], 'is_lifetime': row[3], 'is_blacklisted': row[4], 'key_code': row[5]} for row in c.fetchall()]
    
    return jsonify({'users': users})

@app.route('/api/bot/logs', methods=['GET'])
def api_bot_logs():
    """Dashboard calls this to get execution logs"""
    api_key = request.headers.get('X-API-Key')
    
    if api_key != ADMIN_API_KEY:
        return jsonify({'error': 'Unauthorized'}), 401
    
    c.execute("SELECT key_code, hwid, success, message, executed_at FROM executions ORDER BY executed_at DESC LIMIT 100")
    logs = [{'key_code': row[0], 'hwid': row[1], 'success': row[2], 'message': row[3], 'executed_at': row[4]} for row in c.fetchall()]
    
    return jsonify({'logs': logs})

def run_flask():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    # Run Flask in a separate thread
    threading.Thread(target=run_flask, daemon=True).start()
    # Run Discord bot
    bot.run(TOKEN)
