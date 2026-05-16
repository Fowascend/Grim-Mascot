# init_db.py - Run this once to create database
import sqlite3

conn = sqlite3.connect('grimpot.db')
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
print("✅ Database created!")
