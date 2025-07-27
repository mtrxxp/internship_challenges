import sqlite3
import os
import csv

# Гарантируем, что папка существует
DB_DIR = "./youtube_scrapper_for_internship-main"
os.makedirs(DB_DIR, exist_ok=True)

# Путь к базе (виден и в git-проекте, и в контейнере)
DATABASE = os.path.join(DB_DIR, "channels.db")

def init_db():
    conn = sqlite3.connect(DATABASE)
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
    conn.close()

def save_channel(info):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO influencers
        (channel_id, title, country, subscribers, views, video_count, url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        info["channel_id"], info["title"], info["country"], info["subscribers"],
        info["views"], info["video_count"], info["url"]
    ))
    conn.commit()
    conn.close()

def export_to_csv(filename="influencers.csv"):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM influencers")
    rows = cursor.fetchall()
    conn.close()

    with open(filename, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["channel_id", "title", "country", "subscribers", "views", "video_count", "url"])
        writer.writerows(rows)

def close_db():
    pass