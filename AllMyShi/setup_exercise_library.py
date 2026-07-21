import sqlite3

conn = sqlite3.connect("database/users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS exercise_library (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
""")

exercises = [
    "Bench Press", "Squat", "Deadlift", "Lat Pulldown", "Shoulder Press",
    "Bicep Curl", "Tricep Extension", "Leg Press", "Hamstring Curl", "Calf Raise"
]

for e in exercises:
    cursor.execute("INSERT OR IGNORE INTO exercise_library (name) VALUES (?)", (e,))

conn.commit()
conn.close()

print("Exercise library created and populated.")
