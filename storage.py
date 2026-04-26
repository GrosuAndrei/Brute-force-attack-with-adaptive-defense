import sqlite3
import time
import hashlib

DB_NAME = "database.db"

def connect():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = connect()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip TEXT,
    username TEXT,
    status TEXT,
    timestamp REAL,
    attempted_password TEXT
    )
    """)

    users = [
        ("andrei", hash_password("daniel1")),
        ("admin", hash_password("mic"))
    ]

    for u in users:
        try:
            c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", u)
        except:
            pass

    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_user(username):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def log_attempt(ip, username, status, password=None):
    conn = connect()
    c = conn.cursor()
    now = time.time()
    c.execute("""
        INSERT INTO logs (ip, username, status, timestamp, attempted_password)
        VALUES (?, ?, ?, ?, ?)
    """, (ip, username, status, now, password))
    conn.commit()
    conn.close()

def get_recent_attempts(ip, window_seconds):
    conn = connect()
    c = conn.cursor()
    cutoff = int(time.time()) - window_seconds
    c.execute("""
        SELECT status FROM logs
        WHERE ip=? AND timestamp>?
    """, (ip, cutoff))
    data = c.fetchall()
    conn.close()
    return [d[0] for d in data]

def clear_logs():
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM logs")
    conn.commit()
    c.execute("VACUUM")
    conn.commit()
    conn.close()
    
def get_attempts_after_last_success(ip, window_seconds):
    conn = connect()
    c = conn.cursor()

    cutoff = int(time.time()) - window_seconds

    c.execute("""
        SELECT MAX(timestamp) FROM logs
        WHERE ip=? AND status='success' AND timestamp>?
    """, (ip, cutoff))

    row = c.fetchone()
    last_success_time = row[0] if row and row[0] else None

    if last_success_time:
        c.execute("""
            SELECT status FROM logs
            WHERE ip=? AND timestamp>? 
        """, (ip, last_success_time))
    else:
        c.execute("""
            SELECT status FROM logs
            WHERE ip=? AND timestamp>?
        """, (ip, cutoff))

    data = c.fetchall()
    conn.close()

    return [d[0] for d in data]