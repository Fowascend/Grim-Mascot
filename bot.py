@app.route('/api/validate_project', methods=['POST'])
def validate_project():
    data = request.json
    project_id = data.get('project_id')
    api_key = data.get('api_key')
    
    conn = get_db()
    project = conn.execute("SELECT name FROM projects WHERE id = ? AND api_key = ?", (project_id, api_key)).fetchone()
    conn.close()
    
    if project:
        return jsonify({'valid': True, 'project_name': project['name']})
    return jsonify({'valid': False, 'message': 'Invalid credentials'})

@app.route('/api/redeem_key', methods=['POST'])
def redeem_key():
    data = request.json
    key = data.get('key')
    discord_id = data.get('discord_id')
    
    conn = get_db()
    
    key_record = conn.execute("SELECT id, key_code, expires_at, is_lifetime FROM keys WHERE key_code = ? AND redeemed_by IS NULL", (key,)).fetchone()
    
    if not key_record:
        conn.close()
        return jsonify({'success': False, 'message': 'Invalid or already redeemed key'})
    
    key_id, key_code, expires_at, is_lifetime = key_record
    
    if not is_lifetime and expires_at and expires_at < int(time.time()):
        conn.close()
        return jsonify({'success': False, 'message': 'Key has expired'})
    
    conn.execute("UPDATE keys SET redeemed_by = ?, redeemed_at = ? WHERE id = ?", (discord_id, int(time.time()), key_id))
    conn.execute("INSERT INTO whitelist (id, user_id, key_id, whitelisted_at, expires_at, is_lifetime) VALUES (?, ?, ?, ?, ?, ?)",
                 (secrets.token_hex(16), discord_id, key_id, int(time.time()), expires_at, is_lifetime))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Key redeemed successfully!'})

@app.route('/api/reset_hwid', methods=['POST'])
def reset_hwid():
    data = request.json
    key = data.get('key')
    discord_id = data.get('discord_id')
    
    conn = get_db()
    
    key_record = conn.execute("SELECT id, hwid_resets FROM keys WHERE key_code = ? AND redeemed_by = ?", (key, discord_id)).fetchone()
    
    if not key_record:
        conn.close()
        return jsonify({'success': False, 'message': 'Key not found'})
    
    key_id, current_resets = key_record
    
    conn.execute("UPDATE keys SET hwid = NULL, hwid_resets = ?, last_hwid_reset = ? WHERE id = ?", 
                 (current_resets + 1, int(time.time()), key_id))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'HWID has been reset. You can now use the key on your new device.'})

@app.route('/api/user_stats', methods=['POST'])
def user_stats():
    data = request.json
    key = data.get('key')
    discord_id = data.get('discord_id')
    
    conn = get_db()
    
    stats = conn.execute('''
        SELECT k.key_code, k.hwid, k.hwid_resets, k.last_hwid_reset, 
               w.whitelisted_at, w.expires_at, w.is_lifetime,
               (SELECT COUNT(*) FROM executions WHERE key_code = k.key_code) as total_executions
        FROM keys k
        JOIN whitelist w ON k.id = w.key_id
        WHERE k.key_code = ? AND k.redeemed_by = ?
    ''', (key, discord_id)).fetchone()
    
    conn.close()
    
    if not stats:
        return jsonify({'success': False, 'message': 'Key not found'})
    
    key_code, hwid, hwid_resets, last_hwid_reset, whitelisted_at, expires_at, is_lifetime, total_executions = stats
    
    hwid_status = "🔒 Locked" if hwid else "🔓 Not locked"
    
    expires_text = "Lifetime" if is_lifetime else f"<t:{expires_at}:R>"
    
    return jsonify({
        'success': True,
        'stats': {
            'key_code': key_code,
            'hwid': hwid or 'Not set',
            'hwid_status': hwid_status,
            'hwid_resets': hwid_resets,
            'last_hwid_reset': last_hwid_reset,
            'whitelisted_at': whitelisted_at,
            'expires': expires_text,
            'total_executions': total_executions
        }
    })

@app.route('/api/validate', methods=['POST'])
def validate_key():
    data = request.json
    key = data.get('key')
    hwid = data.get('hwid')
    
    conn = get_db()
    
    key_record = conn.execute('''
        SELECT k.key_code, k.expires_at, k.is_lifetime, k.hwid, k.redeemed_by
        FROM keys k
        WHERE k.key_code = ?
    ''', (key,)).fetchone()
    
    if not key_record:
        conn.close()
        return jsonify({'code': 'KEY_INCORRECT', 'message': 'Key does not exist'})
    
    key_code, expires_at, is_lifetime, stored_hwid, redeemed_by = key_record
    
    if not redeemed_by:
        conn.close()
        return jsonify({'code': 'KEY_INCORRECT', 'message': 'Key not redeemed'})
    
    if not is_lifetime and expires_at and expires_at < int(time.time()):
        conn.execute("INSERT INTO executions (id, key_code, user_id, hwid, ip, success, message, executed_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                     (secrets.token_hex(16), key, redeemed_by, hwid, request.remote_addr, False, 'Key expired', int(time.time())))
        conn.commit()
        conn.close()
        return jsonify({'code': 'KEY_EXPIRED', 'message': 'Your key has expired. Please renew.'})
    
    if stored_hwid and stored_hwid != hwid:
        conn.execute("INSERT INTO executions (id, key_code, user_id, hwid, ip, success, message, executed_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                     (secrets.token_hex(16), key, redeemed_by, hwid, request.remote_addr, False, 'HWID mismatch', int(time.time())))
        conn.commit()
        conn.close()
        return jsonify({'code': 'KEY_HWID_LOCKED', 'message': 'This key is locked to a different HWID. Use /reset_hwid in Discord.'})
    
    if not stored_hwid:
        conn.execute("UPDATE keys SET hwid = ? WHERE key_code = ?", (hwid, key))
    
    conn.execute("INSERT INTO executions (id, key_code, user_id, hwid, ip, success, message, executed_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                 (secrets.token_hex(16), key, redeemed_by, hwid, request.remote_addr, True, 'Valid key', int(time.time())))
    conn.commit()
    
    # Get script content
    script = get_script_content(key)
    
    conn.close()
    
    return jsonify({
        'code': 'KEY_VALID',
        'message': 'Key is valid',
        'script': script,
        'data': {
            'auth_expire': expires_at if not is_lifetime else -1,
            'total_executions': get_execution_count(key)
        }
    })

@app.route('/api/load_script', methods=['GET'])
def load_script():
    project_id = request.args.get('project')
    key = request.args.get('key')
    is_free = request.args.get('free')
    
    if is_free:
        # Free script - check time limit
        # Return script with time check in Lua
        loader = f'''-- GrimPot Free Script
-- This free version expires in 24 hours
local start_time = os.time()
local expiry = start_time + 86400

if os.time() > expiry then
    game:GetService("StarterGui"):SetCore("SendNotification", {{
        Title = "GrimPot",
        Text = "Free trial expired. Purchase a key to continue.",
        Duration = 5
    }})
    return
end

print("✅ GrimPot Free Script Loaded")
print("⏰ This free version expires in: " .. math.floor((expiry - os.time()) / 3600) .. " hours")

-- Your script content here
print("Welcome to GrimPot!")
'''
        return loader
    
    # Paid script - validate key
    conn = get_db()
    key_record = conn.execute("SELECT expires_at, is_lifetime, redeemed_by FROM keys WHERE key_code = ?", (key,)).fetchone()
    conn.close()
    
    if not key_record:
        return "Invalid key"
    
    expires_at, is_lifetime, redeemed_by = key_record
    
    if not is_lifetime and expires_at and expires_at < int(time.time()):
        return "-- Key expired"
    
    loader = f'''-- GrimPot Loader
script_key = "{key}"
loadstring(game:HttpGet("{API_URL}/api/validate"))()
'''
    
    return loader

def get_script_content(key):
    return '''
print("✅ GrimPot Script Loaded Successfully!")
print("Welcome to your protected script!")

-- Your actual script content goes here
-- This is protected and cannot be viewed in browser

local Players = game:GetService("Players")
local player = Players.LocalPlayer

print("Hello, " .. player.Name .. "! Your script is running.")
'''

def get_execution_count(key):
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) FROM executions WHERE key_code = ? AND success = 1", (key,)).fetchone()[0]
    conn.close()
    return count
