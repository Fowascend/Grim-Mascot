# dashboard.py - ADD THESE LINES TO YOUR EXISTING FILE

# Add these imports at the top (if not already there)
import sqlite3
import secrets
import time
import os

# Add these routes to your existing Flask app

@app.route('/api/validate', methods=['POST'])
def api_validate():
    """API endpoint for Lua loader to validate keys"""
    data = request.json
    key = data.get('key')
    hwid = data.get('hwid')
    
    if not key:
        return jsonify({'code': 'INVALID_KEY', 'message': 'No key provided'})
    
    conn = sqlite3.connect('grimpot.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM keys WHERE key_code = ?", (key,))
    key_data = c.fetchone()
    
    if not key_data:
        conn.close()
        return jsonify({'code': 'INVALID_KEY', 'message': 'Key does not exist'})
    
    # Check expiration
    if key_data[4] and key_data[4] < int(time.time()):  # expires_at column
        conn.close()
        return jsonify({'code': 'KEY_EXPIRED', 'message': 'Key has expired'})
    
    # Log execution
    c.execute('''INSERT INTO executions (id, key_code, hwid, ip, success, executed_at) 
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (secrets.token_hex(16), key, hwid, request.remote_addr, True, int(time.time())))
    conn.commit()
    conn.close()
    
    return jsonify({
        'code': 'VALID',
        'message': 'Key is valid',
        'script': 'print("✅ GrimPot Loaded!")'
    })

@app.route('/api/generate', methods=['POST'])
def api_generate():
    """Generate a new key (admin only)"""
    auth = request.headers.get('Authorization')
    if auth != os.environ.get('ADMIN_KEY', 'admin123'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    days = data.get('days')
    
    key_code = secrets.token_hex(16).upper()
    expires_at = int(time.time()) + (days * 86400) if days else None
    
    conn = sqlite3.connect('grimpot.db')
    c = conn.cursor()
    c.execute("INSERT INTO keys (id, key_code, created_at, expires_at) VALUES (?, ?, ?, ?)",
              (secrets.token_hex(16), key_code, int(time.time()), expires_at))
    conn.commit()
    conn.close()
    
    return jsonify({'key': key_code, 'expires_at': expires_at})

@app.route('/api/stats', methods=['GET'])
def api_stats():
    """Get key statistics"""
    conn = sqlite3.connect('grimpot.db')
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM keys")
    total = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM keys WHERE redeemed_by IS NOT NULL")
    used = c.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'total_keys': total,
        'used_keys': used,
        'unused_keys': total - used
    })
