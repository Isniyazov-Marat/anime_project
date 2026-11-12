import sqlite3

conn = sqlite3.connect("anime.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    anime TEXT,
    birthday TEXT
)
""")

cursor.execute("""
INSERT INTO characters (name, anime, birthday)
VALUES (?, ?, ?)
""", ("Naruto", "Naruto", "10-10"))

cursor.execute("""
INSERT INTO characters (name, anime, birthday)
VALUES (?, ?, ?)
""", ("Luffy", "One Piece", "05-05"))

conn.commit()
conn.close()

print("データベースが作成されました")