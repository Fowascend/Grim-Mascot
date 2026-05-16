# dashboard.py - Complete Control Panel
from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify
import sqlite3
import secrets
import time
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
DB_PATH = "grimpot.db"

# ============================================
# HTML TEMPLATES
# ============================================

LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GrimPot Login</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .login-card {
            background: rgba(20, 20, 40, 0.95);
            border-radius: 20px;
            padding: 40px;
            width: 100%;
            max-width: 400px;
            border: 1px solid #2a2a4a;
            backdrop-filter: blur(10px);
        }
        .login-card h1 {
            color: #00aaff;
            text-align: center;
            margin-bottom: 30px;
        }
        .form-control {
            background: #1a1a2e;
            border: 1px solid #2a2a4a;
            color: white;
        }
        .form-control:focus {
            background: #1a1a2e;
            color: white;
            border-color: #00aaff;
            box-shadow: none;
        }
        .btn-primary {
            background: #00aaff;
            border: none;
            width: 100%;
            padding: 12px;
            font-weight: bold;
        }
        .btn-primary:hover {
            background: #0088cc;
        }
        .error {
            color: #ff4444;
            text-align: center;
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <div class="login-card">
        <h1>🔐 GrimPot</h1>
        <form method="POST" action="/login">
            <div class="mb-3">
                <input type="password" class="form-control" name="api_key" placeholder="Enter API Key" required>
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
'''

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GrimPot Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            background: #0a0a0a;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .sidebar {
            position: fixed;
            left: 0;
            top: 0;
            width: 260px;
            height: 100%;
            background: #0f0f1a;
            border-right: 1px solid #1f1f3a;
            padding-top: 20px;
        }
        .sidebar .logo {
            text-align: center;
            padding: 20px;
            border-bottom: 1px solid #1f1f3a;
            margin-bottom: 20px;
        }
        .sidebar .logo h2 {
            color: #00aaff;
            margin: 0;
        }
        .sidebar .nav-link {
            color: #aaa;
            padding: 12px 24px;
            transition: all 0.3s;
        }
        .sidebar .nav-link:hover, .sidebar .nav-link.active {
            background: #1a1a2e;
            color: #00aaff;
            border-left: 3px solid #00aaff;
        }
        .sidebar .nav-link i {
            margin-right: 10px;
            width: 24px;
        }
        .main-content {
            margin-left: 260px;
            padding: 20px;
        }
        .stat-card {
            background: #0f0f1a;
            border: 1px solid #1f1f3a;
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s;
        }
        .stat-card:hover {
            transform: translateY(-5px);
            border-color: #00aaff;
        }
        .stat-card .icon {
            font-size: 2rem;
            color: #00aaff;
            margin-bottom: 10px;
        }
        .stat-card .value {
            font-size: 2rem;
            font-weight: bold;
            color: white;
        }
        .stat-card .label {
            color: #aaa;
            font-size: 0.9rem;
        }
        .card-custom {
            background: #0f0f1a;
            border: 1px solid #1f1f3a;
            border-radius: 12px;
            margin-bottom: 20px;
        }
        .card-custom .card-header {
            background: #1a1a2e;
            border-bottom: 1px solid #2a2a4a;
            padding: 15px 20px;
            font-weight: bold;
            color: white;
        }
        .table-custom {
            color: white;
        }
        .table-custom thead th {
            border-bottom: 1px solid #2a2a4a;
            color: #aaa;
        }
        .table-custom td {
            border-bottom: 1px solid #1f1f3a;
            vertical-align: middle;
        }
        .btn-sm {
            padding: 4px 8px;
            font-size: 12px;
        }
        .key-code {
            font-family: monospace;
            background: #1a1a2e;
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 12px;
        }
        .modal-content {
            background: #0f0f1a;
            border: 1px solid #2a2a4a;
        }
        .modal-header {
            border-bottom: 1px solid #2a2a4a;
        }
        .modal-footer {
            border-top: 1px solid #2a2a4a;
        }
        .form-control, .form-select {
            background: #1a1a2e;
            border: 1px solid #2a2a4a;
            color: white;
        }
        .form-control:focus, .form-select:focus {
            background: #1a1a2e;
            color: white;
            border-color: #00aaff;
            box-shadow: none;
        }
        .badge-active {
            background: #00ff88;
            color: #000;
        }
        .badge-expired {
            background: #ff4444;
        }
        .badge-used {
            background: #ffaa00;
        }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="logo">
            <h2><i class="bi bi-shield-lock"></i> GrimPot</h2>
        </div>
        <nav class="nav flex-column">
            <a class="nav-link active" href="#" onclick="showPage('dashboard')">
                <i class="bi bi-speedometer2"></i> Dashboard
            </a>
            <a class="nav-link" href="#" onclick="showPage('keys')">
                <i class="bi bi-key"></i> Keys
            </a>
            <a class="nav-link" href="#" onclick="showPage('users')">
                <i class="bi bi-people"></i> Users
            </a>
            <a class="nav-link" href="#" onclick="showPage('logs')">
                <i class="bi bi-journal-text"></i> Logs
            </a>
            <a class="nav-link" href="#" onclick="showPage('settings')">
                <i class="bi bi-gear"></i> Settings
            </a>
            <a class="nav-link" href="/logout">
                <i class="bi bi-box-arrow-right"></i> Logout
            </a>
        </nav>
    </div>

    <div class="main-content">
        <!-- Dashboard Page -->
        <div id="page-dashboard">
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="stat-card">
                        <div class="icon"><i class="bi bi-key"></i></div>
                        <div class="value" id="total-keys">0</div>
                        <div class="label">Total Keys</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card">
                        <div class="icon"><i class="bi bi-check-circle"></i></div>
                        <div class="value" id="used-keys">0</div>
                        <div class="label">Used Keys</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card">
                        <div class="icon"><i class="bi bi-hourglass"></i></div>
                        <div class="value" id="unused-keys">0</div>
                        <div class="label">Unused Keys</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card">
                        <div class="icon"><i class="bi bi-people"></i></div>
                        <div class="value" id="total-users">0</div>
                        <div class="label">Whitelisted Users</div>
                    </div>
                </div>
            </div>

            <div class="card-custom">
                <div class="card-header">
                    <i class="bi bi-graph-up"></i> Recent Activity
                </div>
                <div class="card-body">
                    <canvas id="activityChart" height="100"></canvas>
                </div>
            </div>

            <div class="card-custom">
                <div class="card-header">
                    <i class="bi bi-plus-circle"></i> Generate New Key
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-4">
                            <input type="number" id="key-days" class="form-control" placeholder="Days (empty = lifetime)">
                        </div>
                        <div class="col-md-4">
                            <input type="text" id="key-note" class="form-control" placeholder="Note (optional)">
                        </div>
                        <div class="col-md-4">
                            <button class="btn btn-primary w-100" onclick="generateKey()">
                                <i class="bi bi-plus"></i> Generate Key
                            </button>
                        </div>
                    </div>
                    <div id="generate-result" class="mt-3"></div>
                </div>
            </div>
        </div>

        <!-- Keys Page -->
        <div id="page-keys" style="display: none;">
            <div class="card-custom">
                <div class="card-header">
                    <i class="bi bi-key"></i> All Keys
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-custom" id="keys-table">
                            <thead>
                                <tr>
                                    <th>Key</th>
                                    <th>Status</th>
                                    <th>Created</th>
                                    <th>Expires</th>
                                    <th>Redeemed By</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody id="keys-list">
                                <tr><td colspan="6" class="text-center">Loading...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- Users Page -->
        <div id="page-users" style="display: none;">
            <div class="card-custom">
                <div class="card-header">
                    <i class="bi bi-people"></i> Whitelisted Users
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-custom">
                            <thead>
                                <tr>
                                    <th>User ID</th>
                                    <th>Key</th>
                                    <th>Status</th>
                                    <th>Whitelisted At</th>
                                    <th>Expires</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody id="users-list">
                                <tr><td colspan="6" class="text-center">No users whitelisted</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- Logs Page -->
        <div id="page-logs" style="display: none;">
            <div class="card-custom">
                <div class="card-header">
                    <i class="bi bi-journal-text"></i> Execution Logs
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-custom">
                            <thead>
                                <tr>
                                    <th>Key</th>
                                    <th>HWID</th>
                                    <th>Status</th>
                                    <th>IP</th>
                                    <th>Time</th>
                                </tr>
                            </thead>
                            <tbody id="logs-list">
                                <tr><td colspan="5" class="text-center">Loading...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- Settings Page -->
        <div id="page-settings" style="display: none;">
            <div class="card-custom">
                <div class="card-header">
                    <i class="bi bi-gear"></i> API Settings
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        <label class="form-label text-white">API Base URL</label>
                        <input type="text" class="form-control" id="api-url" value="https://YOUR_API_URL" readonly>
                    </div>
                    <div class="mb-3">
                        <label class="form-label text-white">Admin API Key</label>
                        <input type="password" class="form-control" id="admin-key" value="{{ admin_key }}" readonly>
                    </div>
                    <div class="mb-3">
                        <label class="form-label text-white">HWID Lock</label>
                        <select class="form-select" id="hwid-lock">
                            <option value="1">Enabled</option>
                            <option value="0">Disabled</option>
                        </select>
                    </div>
                    <button class="btn btn-primary" onclick="saveSettings()">Save Settings</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentPage = 'dashboard';
        
        function showPage(page) {
            document.getElementById('page-dashboard').style.display = page === 'dashboard' ? 'block' : 'none';
            document.getElementById('page-keys').style.display = page === 'keys' ? 'block' : 'none';
            document.getElementById('page-users').style.display = page === 'users' ? 'block' : 'none';
            document.getElementById('page-logs').style.display = page === 'logs' ? 'block' : 'none';
            document.getElementById('page-settings').style.display = page === 'settings' ? 'block' : 'none';
            currentPage = page;
            
            if (page === 'dashboard') loadDashboard();
            if (page === 'keys') loadKeys();
            if (page === 'users') loadUsers();
            if (page === 'logs') loadLogs();
        }
        
        async function loadDashboard() {
            const response = await fetch('/api/stats');
            const stats = await response.json();
            
            document.getElementById('total-keys').innerText = stats.total_keys || 0;
            document.getElementById('used-keys').innerText = stats.used_keys || 0;
            document.getElementById('unused-keys').innerText = (stats.total_keys - stats.used_keys) || 0;
            document.getElementById('total-users').innerText = stats.total_users || 0;
        }
        
        async function loadKeys() {
            const response = await fetch('/api/keys');
            const keys = await response.json();
            
            const tbody = document.getElementById('keys-list');
            if (!keys.length) {
                tbody.innerHTML = '<tr><td colspan="6" class="text-center">No keys found</td></tr>';
                return;
            }
            
            tbody.innerHTML = keys.map(key => `
                <tr>
                    <td><code class="key-code">${key.key_code}</code></td>
                    <td>${key.redeemed_by ? '<span class="badge bg-warning">Used</span>' : '<span class="badge bg-success">Active</span>'}</td>
                    <td>${new Date(key.created_at * 1000).toLocaleDateString()}</td>
                    <td>${key.expires_at ? new Date(key.expires_at * 1000).toLocaleDateString() : 'Lifetime'}</td>
                    <td>${key.redeemed_by || '-'}</td>
                    <td>
                        <button class="btn btn-danger btn-sm" onclick="deleteKey('${key.key_code}')">
                            <i class="bi bi-trash"></i>
                        </button>
                    </td>
                </tr>
            `).join('');
        }
        
        async function loadUsers() {
            const response = await fetch('/api/users');
            const users = await response.json();
            
            const tbody = document.getElementById('users-list');
            if (!users.length) {
                tbody.innerHTML = '<tr><td colspan="6" class="text-center">No users whitelisted</td></tr>';
                return;
            }
            
            tbody.innerHTML = users.map(user => `
                <tr>
                    <td><code>${user.user_id}</code></td>
                    <td><code class="key-code">${user.key_code}</code></td>
                    <td>${user.is_lifetime ? 'Lifetime' : (user.expires_at > Date.now()/1000 ? 'Active' : 'Expired')}</td>
                    <td>${new Date(user.whitelisted_at * 1000).toLocaleDateString()}</td>
                    <td>${user.is_lifetime ? 'Never' : new Date(user.expires_at * 1000).toLocaleDateString()}</td>
                    <td>
                        <button class="btn btn-danger btn-sm" onclick="blacklistUser(${user.user_id})">
                            <i class="bi bi-person-x"></i> Blacklist
                        </button>
                    </td>
                </tr>
            `).join('');
        }
        
        async function loadLogs() {
            const response = await fetch('/api/logs');
            const logs = await response.json();
            
            const tbody = document.getElementById('logs-list');
            if (!logs.length) {
                tbody.innerHTML = '<tr><td colspan="5" class="text-center">No logs found</td></tr>';
                return;
            }
            
            tbody.innerHTML = logs.map(log => `
                <tr>
                    <td><code class="key-code">${log.key_code}</code></td>
                    <td><code>${log.hwid || '-'}</code></td>
                    <td>${log.success ? '✅ Success' : '❌ Failed'}</td>
                    <td>${log.ip || '-'}</td>
                    <td>${new Date(log.executed_at * 1000).toLocaleString()}</td>
                </tr>
            `).join('');
        }
        
        async function generateKey() {
            const days = document.getElementById('key-days').value;
            const note = document.getElementById('key-note').value;
            
            const response = await fetch('/api/generate_keys', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ days: days ? parseInt(days) : null, note: note })
            });
            
            const data = await response.json();
            
            if (data.keys) {
                document.getElementById('generate-result').innerHTML = `
                    <div class="alert alert-success">
                        <strong>✅ Key Generated!</strong><br>
                        <code class="key-code">${data.keys[0]}</code>
                    </div>
                `;
                loadKeys();
                loadDashboard();
            } else {
                document.getElementById('generate-result').innerHTML = `
                    <div class="alert alert-danger">❌ Failed to generate key</div>
                `;
            }
        }
        
        async function deleteKey(keyCode) {
            if (!confirm('Are you sure you want to delete this key?')) return;
            
            const response = await fetch('/api/delete_key', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ key_code: keyCode })
            });
            
            if (response.ok) {
                loadKeys();
                loadDashboard();
            }
        }
        
        async function blacklistUser(userId) {
            if (!confirm('Are you sure you want to blacklist this user?')) return;
            
            const response = await fetch('/api/blacklist_user', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId })
            });
            
            if (response.ok) {
                loadUsers();
                loadDashboard();
            }
        }
        
        function saveSettings() {
            alert('Settings saved!');
        }
        
        loadDashboard();
    </script>
</body>
</html>
'''

# ============================================
# ROUTES
# ============================================

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS keys (
        id TEXT PRIMARY KEY,
        key_code TEXT UNIQUE,
        redeemed_by TEXT,
        redeemed_at INTEGER,
        expires_at INTEGER,
        note TEXT,
        created_at INTEGER
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS whitelist (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        key_id TEXT,
        whitelisted_by TEXT,
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
    conn.close()

init_db()

@app.route('/')
def index():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    api_key = request.form.get('api_key')
    ADMIN_KEY = os.environ.get('ADMIN_KEY', 'admin123')
    
    if api_key == ADMIN_KEY:
        session['logged_in'] = True
        return redirect(url_for('dashboard'))
    
    return render_template_string(LOGIN_TEMPLATE, error='Invalid API Key')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    return render_template_string(DASHBOARD_TEMPLATE, admin_key=os.environ.get('ADMIN_KEY', 'admin123'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ============================================
# API ENDPOINTS
# ============================================

@app.route('/api/stats')
def api_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM keys")
    total_keys = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM keys WHERE redeemed_by IS NOT NULL")
    used_keys = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM whitelist")
    total_users = c.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'total_keys': total_keys,
        'used_keys': used_keys,
        'total_users': total_users
    })

@app.route('/api/keys')
def api_keys():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT key_code, redeemed_by, redeemed_at, expires_at, created_at FROM keys ORDER BY created_at DESC")
    keys = [{'key_code': row[0], 'redeemed_by': row[1], 'redeemed_at': row[2], 
             'expires_at': row[3], 'created_at': row[4]} for row in c.fetchall()]
    
    conn.close()
    return jsonify(keys)

@app.route('/api/users')
def api_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''SELECT w.user_id, w.whitelisted_at, w.expires_at, w.is_lifetime, k.key_code 
                 FROM whitelist w 
                 JOIN keys k ON w.key_id = k.id''')
    
    users = [{'user_id': row[0], 'whitelisted_at': row[1], 'expires_at': row[2], 
              'is_lifetime': row[3], 'key_code': row[4]} for row in c.fetchall()]
    
    conn.close()
    return jsonify(users)

@app.route('/api/logs')
def api_logs():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT key_code, hwid, ip, success, executed_at FROM executions ORDER BY executed_at DESC LIMIT 50")
    logs = [{'key_code': row[0], 'hwid': row[1], 'ip': row[2], 
             'success': row[3], 'executed_at': row[4]} for row in c.fetchall()]
    
    conn.close()
    return jsonify(logs)

@app.route('/api/generate_keys', methods=['POST'])
def api_generate_keys():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    days = data.get('days')
    note = data.get('note')
    
    key_code = secrets.token_hex(16).upper()
    expires_at = int(time.time()) + (days * 86400) if days else None
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO keys (id, key_code, expires_at, note, created_at) VALUES (?, ?, ?, ?, ?)",
              (secrets.token_hex(16), key_code, expires_at, note, int(time.time())))
    conn.commit()
    conn.close()
    
    return jsonify({'keys': [key_code]})

@app.route('/api/delete_key', methods=['POST'])
def api_delete_key():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    key_code = data.get('key_code')
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM keys WHERE key_code = ?", (key_code,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/blacklist_user', methods=['POST'])
def api_blacklist_user():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    user_id = data.get('user_id')
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM whitelist WHERE user_id = ?", (user_id,))
    c.execute("UPDATE keys SET redeemed_by = NULL, redeemed_at = NULL WHERE redeemed_by = ?", (user_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/validate', methods=['POST'])
def api_validate():
    data = request.json
    key = data.get('key')
    hwid = data.get('hwid')
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT key_code, expires_at FROM keys WHERE key_code = ?", (key,))
    key_data = c.fetchone()
    
    if not key_data:
        return jsonify({'code': 'INVALID_KEY', 'message': 'Key does not exist'})
    
    if key_data[1] and key_data[1] < int(time.time()):
        return jsonify({'code': 'KEY_EXPIRED', 'message': 'Key has expired'})
    
    exec_id = secrets.token_hex(16)
    c.execute("INSERT INTO executions (id, key_code, hwid, ip, success, executed_at) VALUES (?, ?, ?, ?, ?, ?)",
              (exec_id, key, hwid, request.remote_addr, True, int(time.time())))
    conn.commit()
    conn.close()
    
    return jsonify({
        'code': 'VALID',
        'message': 'Key is valid',
        'script': 'print("✅ GrimPot Loaded Successfully!")'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
