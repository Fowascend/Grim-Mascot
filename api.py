# api.py - Flask API for Lua loader
from flask import Flask, request, jsonify
import sqlite3
import time
import secrets
from datetime import datetime

app = Flask(__name__)
DB_PATH = "grimpot.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/validate', methods=['POST'])
def validate_key():
    data = request.json
    key = data.get('key')
    hwid = data.get('hwid')
    discord_id = data.get('discordId')
    
    if not key:
        return jsonify({'code': 'INVALID_KEY', 'message': 'No key provided'})
    
    conn = get_db()
    
    # Check key exists
    key_record = conn.execute('''
        SELECT k.*, p.name as project_name, p.version, p.hwid_lock 
        FROM keys k
        JOIN projects p ON k.project_id = p.id
        WHERE k.key_code = ?
    ''', (key,)).fetchone()
    
    if not key_record:
        conn.close()
        return jsonify({'code': 'INVALID_KEY', 'message': 'Key does not exist'})
    
    # Check expiration
    if not key_record['is_lifetime'] and key_record['expires_at'] and key_record['expires_at'] < int(time.time()):
        conn.close()
        return jsonify({'code': 'KEY_EXPIRED', 'message': 'Key has expired'})
    
    # Check HWID
    if key_record['hwid_lock'] and key_record['redeemed_by']:
        last_exec = conn.execute('''
            SELECT hwid FROM executions 
            WHERE key_code = ? AND success = 1 
            ORDER BY executed_at DESC LIMIT 1
        ''', (key,)).fetchone()
        
        if last_exec and last_exec['hwid'] and last_exec['hwid'] != hwid:
            conn.close()
            return jsonify({'code': 'HWID_MISMATCH', 'message': 'Key locked to different HWID'})
    
    # Get script content
    script = conn.execute('''
        SELECT content FROM scripts 
        WHERE project_id = ? AND is_active = 1 
        ORDER BY version DESC LIMIT 1
    ''', (key_record['project_id'],)).fetchone()
    
    # Log execution
    conn.execute('''
        INSERT INTO executions (id, key_code, user_id, hwid, ip, success, message, executed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (secrets.token_hex(16), key, discord_id, hwid, request.remote_addr, True, 'Valid key', int(time.time())))
    conn.commit()
    conn.close()
    
    return jsonify({
        'code': 'VALID',
        'message': 'Key is valid',
        'script': script['content'] if script else '',
        'project': {
            'name': key_record['project_name'],
            'version': key_record['version']
        }
    })

@app.route('/api/redeem', methods=['POST'])
def redeem_key():
    data = request.json
    key = data.get('key')
    discord_id = data.get('discordId')
    discord_name = data.get('discordName')
    hwid = data.get('hwid')
    
    conn = get_db()
    
    # Check if user exists
    user = conn.execute('SELECT * FROM users WHERE discord_id = ?', (discord_id,)).fetchone()
    if not user:
        user_id = secrets.token_hex(16)
        conn.execute('''
            INSERT INTO users (id, discord_id, discord_name, created_at)
            VALUES (?, ?, ?, ?)
        ''', (user_id, discord_id, discord_name, int(time.time())))
        conn.commit()
    else:
        user_id = user['id']
    
    # Get key
    key_record = conn.execute('SELECT * FROM keys WHERE key_code = ?', (key,)).fetchone()
    
    if not key_record:
        conn.close()
        return jsonify({'success': False, 'message': 'Invalid key'})
    
    if key_record['redeemed_by']:
        conn.close()
        return jsonify({'success': False, 'message': 'Key already redeemed'})
    
    # Redeem key
    conn.execute('UPDATE keys SET redeemed_by = ?, redeemed_at = ? WHERE id = ?', 
                (user_id, int(time.time()), key_record['id']))
    
    # Add to whitelist
    conn.execute('''
        INSERT INTO whitelist (id, user_id, project_id, key_id, whitelisted_by, whitelisted_at, expires_at, is_lifetime)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (secrets.token_hex(16), user_id, key_record['project_id'], key_record['id'], 
          user_id, int(time.time()), key_record['expires_at'], key_record['is_lifetime']))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Key redeemed successfully'})

@app.route('/api/loader/<project_id>')
def get_loader(project_id):
    loader_template = f'''--[[ GrimPot Loader ]]
local key = "%s"
local hwid = game:GetService("RbxAnalyticsService"):GetDeviceId() or "Unknown"

local function httpPost(url, data)
    local syn = syn and syn.request or request or http_request
    if syn then
        local response = syn({{Url = url, Method = "POST", Headers = {{["Content-Type"] = "application/json"}}, Body = game:GetService("HttpService"):JSONEncode(data)}})
        return response.Body
    end
    return game:GetService("HttpService"):PostAsync(url, game:GetService("HttpService"):JSONEncode(data))
end

local response = httpPost("https://YOUR_API_URL/api/validate", {{key = key, hwid = hwid}})
local data = game:GetService("HttpService"):JSONDecode(response)

if data.code == "VALID" then
    print("✅ GrimPot: Key valid!")
    loadstring(data.script)()
else
    warn("❌ GrimPot: " .. data.message)
end
'''
    return loader_template

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
