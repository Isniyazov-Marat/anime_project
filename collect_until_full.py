import requests
import sqlite3
import time
import os

conn = sqlite3.connect("anime.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS characters")

cursor.execute("""
CREATE TABLE characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    anime TEXT,
    birthday TEXT,
    image TEXT
)
""")

conn.commit()

os.makedirs("static/images", exist_ok=True)

url = "https://graphql.anilist.co"

query = """
query ($page: Int) {
  Page(page: $page, perPage: 50) {
    characters(sort: FAVOURITES_DESC) {
      name {
        full
        native
      }
      image {
        large
      }
      dateOfBirth {
        month
        day
      }
      media(perPage: 1) {
        nodes {
          title {
            romaji
          }
        }
      }
    }
  }
}
"""

page = 1
count = 0

while page <= 30:
    try:
        r = requests.post(url, json={"query": query, "variables": {"page": page}}, timeout=15)
        data = r.json()

        characters = data["data"]["Page"]["characters"]

        for char in characters:
            month = char["dateOfBirth"]["month"]
            day = char["dateOfBirth"]["day"]

            if not month or not day:
                continue

            birthday = f"{month:02d}-{day:02d}"
            name = char["name"]["native"] or char["name"]["full"]

            anime = "Unknown"
            if char["media"]["nodes"]:
                anime = char["media"]["nodes"][0]["title"]["romaji"]

            image_url = char["image"]["large"]
            image_path = f"static/images/{count + 1}.jpg"
            db_image_path = f"/static/images/{count + 1}.jpg"

            if image_url:
                img = requests.get(image_url, timeout=15)
                with open(image_path, "wb") as f:
                    f.write(img.content)

            cursor.execute(
                "INSERT INTO characters (name, anime, birthday, image) VALUES (?, ?, ?, ?)",
                (name, anime, birthday, db_image_path)
            )

            count += 1

        conn.commit()
        print(f"Page {page} done / characters: {count}")

        page += 1
        time.sleep(1)

    except Exception as e:
        conn.commit()
        print("ERROR:", e)
        page += 1
        time.sleep(3)

conn.commit()
conn.close()

print(f"Imported {count} characters")

