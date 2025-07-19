import sqlite3
import csv

DB_NAME = "channels.db"
CSV_NAME = "influencers.csv"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS influencers (
        channel_id TEXT PRIMARY KEY,
        title TEXT,
        country TEXT,
        subscribers INTEGER,
        views INTEGER,
        video_count INTEGER,
        url TEXT
    )
''')
conn.commit()

def save_channel(info):
    cursor.execute('''
        INSERT OR REPLACE INTO influencers
        (channel_id, title, country, subscribers, views, video_count, url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        info["channel_id"], info["title"], info["country"],
        info["subscribers"], info["views"], info["video_count"], info["url"]
    ))
    conn.commit()

def export_to_csv():
    cursor.execute("SELECT * FROM influencers")
    rows = cursor.fetchall()
    with open(CSV_NAME, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["channel_id", "title", "country", "subscribers", "views", "video_count", "url"])
        writer.writerows(rows)
    print(f"\n📁 Saved {len(rows)} entries to {CSV_NAME}")

def close_db():
    conn.close()