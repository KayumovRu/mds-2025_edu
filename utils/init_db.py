import sqlite3

conn = sqlite3.connect("models.db")
conn.execute("""
CREATE TABLE IF NOT EXISTS training_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT NOT NULL,
    accuracy REAL,
    model_path TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()
conn.close()