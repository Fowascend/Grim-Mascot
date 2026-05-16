from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import secrets
import time
from datetime import datetime

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Database connection
def get_db():
    conn = sqlite3.connect('grimpot.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home page - Login
@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    api_key = request.form.get('api_key')
    
    conn = get_db()
    project = conn.execute("SELECT * FROM projects WHERE api_key = ?", (api_key,)).fetchone()
    conn.close()
    
    if project:
        session['logged_in'] = True
        session['project_id'] = project['id']
        session['project_name'] = project['name']
        session['api_key'] = api_key
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error="Invalid API Key")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Main Dashboard
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    
    conn = get_db()
    project_id = session['project_id']
    
    # Get project info
    project = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    
    # Get stats
    total_keys = conn.execute("SELECT COUNT(*) FROM keys WHERE project_id = ?", (project_id,)).fetchone()[0]
    used_keys = conn.execute("SELECT COUNT(*) FROM keys WHERE project_id = ? AND redeemed_by IS NOT NULL", (project_id,)).fetchone()[0]
    unused_keys = total_keys - used_keys
    total_users = conn.execute("SELECT COUNT(*) FROM whitelist WHERE project_id = ?", (project_id,)).fetchone()[0]
    
    conn.close()
    
    return render_template('dashboard.html', 
                          project=project,
                          total_keys=total_keys,
                          used_keys=used_keys,
                          unused_keys=unused_keys,
                          total_users=total_users)

# Keys Management Page
@app.route('/keys')
def keys_page():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    
    conn = get_db()
    project_id = session['project_id']
    
    keys = conn.execute("""
        SELECT k.*, u.name as user_name, u.id as user_discord_id 
        FROM keys k
        LEFT JOIN whitelist w ON k.id = w.key_id
        LEFT JOIN users u ON w.user_id = u.id
        WHERE k.project_id = ?
        ORDER BY k.created_at DESC
    """, (project_id,)).fetchall()
    
    conn.close()
    
    return render_template('keys.html', keys=keys)

# Users Management Page
@app.route('/users')
def users_page():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    
    conn = get_db()
    project_id = session['project_id']
    
    users = conn.execute("""
        SELECT w.*, k.key_code 
        FROM whitelist w
        JOIN keys k ON w.key_id = k.id
        WHERE w.project_id = ?
        ORDER BY w.whitelisted_at DESC
    """, (project_id,)).fetchall()
    
    conn.close()
    
    return render_template('users.html', users=users)

# Generate new keys (AJAX)
@app.route('/api/generate_keys', methods=['POST'])
def generate_keys():
    if not session.get('logged_in'):
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    amount = int(data.get('amount', 1))
    days = data.get('days')
    project_id = session['project_id']
    
    is_lifetime = days is None or days == ""
    expires_at = int(time.time()) + (int(days) * 86400) if days and not is_lifetime else None
    
    keys = []
    for _ in range(amount):
        key_code = secrets.token_hex(16)
        conn = get_db()
        conn.execute("INSERT INTO keys (key_code, project_id, is_lifetime, expires_at, created_by, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (key_code, project_id, is_lifetime, expires_at, session.get('user_id', 0), int(time.time())))
        conn.commit()
        conn.close()
        keys.append(key_code)
    
    return jsonify({'keys': keys})

# Blacklist user (AJAX)
@app.route('/api/blacklist_user', methods=['POST'])
def blacklist_user():
    if not session.get('logged_in'):
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    user_id = data.get('user_id')
    project_id = session['project_id']
    
    conn = get_db()
    
    # Get key_id before deleting
    key_data = conn.execute("SELECT key_id FROM whitelist WHERE user_id = ? AND project_id = ?", (user_id, project_id)).fetchone()
    
    if key_data:
        key_id = key_data[0]
        # Delete from whitelist
        conn.execute("DELETE FROM whitelist WHERE user_id = ? AND project_id = ?", (user_id, project_id))
        # Mark key as unused
        conn.execute("UPDATE keys SET redeemed_by = NULL, redeemed_at = NULL WHERE id = ?", (key_id,))
        conn.commit()
    
    conn.close()
    
    return jsonify({'success': True})

# Get key info (AJAX)
@app.route('/api/key_info/<key_code>')
def key_info(key_code):
    if not session.get('logged_in'):
        return jsonify({'error': 'Not logged in'}), 401
    
    conn = get_db()
    key = conn.execute("""
        SELECT k.*, w.user_id, w.whitelisted_at, w.expires_at, w.is_lifetime
        FROM keys k
        LEFT JOIN whitelist w ON k.id = w.key_id
        WHERE k.key_code = ? AND k.project_id = ?
    """, (key_code, session['project_id'])).fetchone()
    conn.close()
    
    if key:
        return jsonify(dict(key))
    return jsonify({'error': 'Key not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
