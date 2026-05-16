from flask import Flask, request, jsonify
import sqlite3
import time
import hmac
import hashlib
import base64

app = Flask(__name__)

conn = sqlite3.connect('grimpot.db', check_same_thread=False)
c = conn.cursor()

# Your actual script content (obfuscated/minified)
# This will be served when key is valid
PROTECTED_SCRIPT = """
--[[ GrimPot Protected Script ]]
-- Loaded successfully!

local Players = game:GetService("Players")
local player = Players.LocalPlayer

print("✅ GrimPot Script Loaded!")

-- Your full AJ script goes here
-- This is the protected content

loadstring([[
    -- Paste your actual Lazy AJ / ZYROX AJ script here
    print("ZYROX AJ - Fully Loaded")
]])()
"""

@app.route('/api/validate', methods=['POST'])
def validate_key():
    data = request.json
    key = data.get('key')
    hwid = data.get('hwid')
    
    if not key:
        return jsonify({'code': 'INVALID_KEY', 'message': 'No key provided'})
    
    c.execute("SELECT id, project_id, redeemed_by, is_lifetime, expires_at FROM keys WHERE key_code = ?", (key,))
    key_data = c.fetchone()
    
    if not key_data:
        return jsonify({'code': 'INVALID_KEY', 'message': 'Key does not exist'})
    
    key_id, project_id, redeemed_by, is_lifetime, expires_at = key_data
    
    # Check if expired
    if not is_lifetime and expires_at and expires_at < int(time.time()):
        return jsonify({'code': 'KEY_EXPIRED', 'message': 'Key has expired'})
    
    # Check if HWID locked
    if redeemed_by:
        c.execute("SELECT hwid FROM executions WHERE key_code = ? ORDER BY id DESC LIMIT 1", (key,))
        hwid_data = c.fetchone()
        if hwid_data and hwid_data[0] and hwid_data[0] != hwid:
            return jsonify({'code': 'HWID_MISMATCH', 'message': 'Key locked to different HWID'})
    
    # Log execution
    c.execute("INSERT INTO executions (key_code, hwid, executed_at, ip) VALUES (?, ?, ?, ?)",
              (key, hwid, int(time.time()), request.remote_addr))
    conn.commit()
    
    return jsonify({
        'code': 'VALID',
        'message': 'Key is valid',
        'script': PROTECTED_SCRIPT,
        'expires_at': expires_at,
        'is_lifetime': is_lifetime
    })

@app.route('/api/load', methods=['GET'])
def load_script():
    key = request.args.get('key')
    hwid = request.args.get('hwid')
    
    if not key:
        return "Invalid key", 403
    
    c.execute("SELECT id, is_lifetime, expires_at FROM keys WHERE key_code = ?", (key,))
    key_data = c.fetchone()
    
    if not key_data:
        return "Invalid key", 403
    
    key_id, is_lifetime, expires_at = key_data
    
    if not is_lifetime and expires_at and expires_at < int(time.time()):
        return "Key expired", 403
    
    # Return obfuscated script that can't be viewed in browser
    import zlib
    import base64
    
    compressed = zlib.compress(PROTECTED_SCRIPT.encode())
    encoded = base64.b64encode(compressed).decode()
    
    loadstring_code = f'loadstring(game:HttpGet("https://YOUR_API_URL/api/execute?key={key}&hwid={hwid}"))()'
    
    return loadstring_code

@app.route('/api/execute', methods=['GET'])
def execute_script():
    key = request.args.get('key')
    hwid = request.args.get('hwid')
    
    if not key:
        return "Invalid key", 403
    
    c.execute("SELECT id, is_lifetime, expires_at FROM keys WHERE key_code = ?", (key,))
    key_data = c.fetchone()
    
    if not key_data:
        return "Invalid key", 403
    
    key_id, is_lifetime, expires_at = key_data
    
    if not is_lifetime and expires_at and expires_at < int(time.time()):
        return "Key expired", 403
    
    # Return the actual script
    return PROTECTED_SCRIPT

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
