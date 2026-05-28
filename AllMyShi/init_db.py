import sqlite3
import os

# Ensure the database folder exists
os.makedirs("database", exist_ok=True)

# Path to your database
db_path = "database/users.db"

# Connect and create table
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Database created successfully at", db_path)