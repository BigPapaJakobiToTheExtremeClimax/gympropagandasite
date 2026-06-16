import sqlite3
import os

os.makedirs("database", exist_ok=True)
db_path = "database/users.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Table for workout sessions
cursor.execute("""
CREATE TABLE IF NOT EXISTS workout_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    template_name TEXT NOT NULL,
    date TEXT NOT NULL
)
""")

# Table for individual sets
cursor.execute("""
CREATE TABLE IF NOT EXISTS workout_sets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workout_id INTEGER NOT NULL,
    exercise_name TEXT NOT NULL,
    set_number INTEGER NOT NULL,
    reps INTEGER,
    weight REAL,
    completed INTEGER DEFAULT 0,
    FOREIGN KEY (workout_id) REFERENCES workout_logs(id)
)
""")

conn.commit()
conn.close()

print("Workout tables created successfully.")