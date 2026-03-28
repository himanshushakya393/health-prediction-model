import sqlite3

# 🔹 Create connection
conn = sqlite3.connect("appointments.db")
cursor = conn.cursor()

# 🔹 Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    date TEXT,
    disease TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()