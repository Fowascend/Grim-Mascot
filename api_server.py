# api_server.py - Backend API for key validation
from flask import Flask, request, jsonify
import sqlite3
import secrets
import time
import os

app = Flask(__name__)
DB_PATH = "grimpot.db"

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS keys (
        id TEXT PRIMARY KEY,
        key_code TEXT UNIQUE,
        redeemed_by TEXT,
        redeemed_at INTEGER,
        expires_at INTEGER,
        created_at INTEGER
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS executions (
        id TEXT PRIMARY KEY,
        key_code TEXT,
        hwid TEXT,
        ip TEXT,
        success BOOLEAN,
        message TEXT,
        executed_at INTEGER
    )''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized")

init_db()

@app.route('/api/validate', methods=['POST'])
def validate_key():
    data = request.json
    key = data.get('key')
    hwid = data.get('hwid')
    
    if not key:
        return jsonify({'code': 'INVALID_KEY', 'message': 'No key provided'})
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT * FROM keys WHERE key_code = ?", (key,))
    key_data = c.fetchone()
    
    if not key_data:
        conn.close()
        return jsonify({'code': 'INVALID_KEY', 'message': 'Key does not exist'})
    
    # Check expiration
    key_id, key_code, redeemed_by, redeemed_at, expires_at, created_at = key_data
    if expires_at and expires_at < int(time.time()):
        conn.close()
        return jsonify({'code': 'KEY_EXPIRED', 'message': 'Key has expired'})
    
    # Log execution
    exec_id = secrets.token_hex(16)
    c.execute('''INSERT INTO executions (id, key_code, hwid, ip, success, message, executed_at) 
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (exec_id, key, hwid, request.remote_addr, True, 'Valid key', int(time.time())))
    conn.commit()
    conn.close()
    
    return jsonify({
        'code': 'VALID',
        'message': 'Key is valid',
        'script': 'print("✅ GrimPot Loaded Successfully!")'
    })

@app.route('/api/generate', methods=['POST'])
def generate_key():
    auth = request.headers.get('Authorization')
    if auth != os.environ.get('ADMIN_KEY', 'admin123'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    days = data.get('days')
    
    key_code = secrets.token_hex(16).upper()
    expires_at = int(time.time()) + (days * 86400) if days else None
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO keys (id, key_code, created_at, expires_at) VALUES (?, ?, ?, ?)",
              (secrets.token_hex(16), key_code, int(time.time()), expires_at))
    conn.commit()
    conn.close()
    
    return jsonify({'key': key_code, 'expires_at': expires_at})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM keys")
    total_keys = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM keys WHERE redeemed_by IS NOT NULL")
    used_keys = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM executions")
    total_executions = c.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'total_keys': total_keys,
        'used_keys': used_keys,
        'unused_keys': total_keys - used_keys,
        'total_executions': total_executions
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
