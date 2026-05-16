# database.py - SQLite database models
import sqlite3
import secrets
import time
from datetime import datetime

DB_PATH = "grimpot.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        discord_id TEXT UNIQUE,
        discord_name TEXT,
        email TEXT,
        created_at INTEGER
    )''')
    
    # Projects table
    c.execute('''CREATE TABLE IF NOT EXISTS projects (
        id TEXT PRIMARY KEY,
        name TEXT UNIQUE,
        api_key TEXT UNIQUE,
        buyer_role_id TEXT,
        hwid_lock BOOLEAN DEFAULT 1,
        hwid_cooldown INTEGER DEFAULT 604800,
        created_by TEXT,
        created_at INTEGER
    )''')
    
    # Keys table
    c.execute('''CREATE TABLE IF NOT EXISTS keys (
        id TEXT PRIMARY KEY,
        key_code TEXT UNIQUE,
        project_id TEXT,
        redeemed_by TEXT,
        redeemed_at INTEGER,
        is_lifetime BOOLEAN DEFAULT 0,
        expires_at INTEGER,
        created_by TEXT,
        created_at INTEGER,
        FOREIGN KEY(project_id) REFERENCES projects(id)
    )''')
    
    # Whitelist table
    c.execute('''CREATE TABLE IF NOT EXISTS whitelist (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        project_id TEXT,
        key_id TEXT,
        whitelisted_by TEXT,
        whitelisted_at INTEGER,
        expires_at INTEGER,
        is_lifetime BOOLEAN DEFAULT 0,
        is_active BOOLEAN DEFAULT 1,
        UNIQUE(user_id, project_id)
    )''')
    
    # Executions table (logs)
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
    
    # Scripts table
    c.execute('''CREATE TABLE IF NOT EXISTS scripts (
        id TEXT PRIMARY KEY,
        project_id TEXT,
        name TEXT,
        content TEXT,
        version TEXT,
        is_active BOOLEAN DEFAULT 1,
        created_at INTEGER
    )''')
    
    conn.commit()
    conn.close()

def generate_id():
    return secrets.token_hex(16)

def generate_api_key():
    return secrets.token_hex(32)

def generate_key_code():
    return secrets.token_hex(16).upper()
