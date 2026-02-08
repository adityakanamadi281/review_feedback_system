import sqlite3
import os

# Get the directory where this file is located
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(CURRENT_DIR, "data", "feedback.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rating INTEGER,
        review TEXT,
        ai_response TEXT,
        ai_summary TEXT,
        ai_action TEXT
    )
    """)
    conn.commit()
    conn.close()

def insert_feedback(rating, review, response, summary, action):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO feedback (rating, review, ai_response, ai_summary, ai_action)
    VALUES (?, ?, ?, ?, ?)
    """, (rating, review, response, summary, action))
    conn.commit()
    conn.close()

def fetch_all():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT rating, review, ai_summary, ai_action FROM feedback")
    rows = cur.fetchall()
    conn.close()
    return rows
