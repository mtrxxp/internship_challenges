import os
import csv
import sqlite3
from dotenv import load_dotenv

load_dotenv()

DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()


DB_DIR = os.path.join(os.path.dirname(__file__), "databases")
os.makedirs(DB_DIR, exist_ok=True)


DATABASE = os.path.join(DB_DIR, "channels.db")

def get_connection():
    if DB_TYPE == "postgres":
        import psycopg2
        return psycopg2.connect(
            host=os.getenv("DB_HOST", "postgres"),
            port=os.getenv("DB_PORT", 5432),
            dbname=os.getenv("DB_NAME", "youtube_db"),
            user=os.getenv("DB_USER", "myuser"),
            password=os.getenv("DB_PASS", "mypass")
        )
    else:
        DB_DIR = os.path.join(os.path.dirname(__file__), "databases")
        os.makedirs(DB_DIR, exist_ok=True)
        DATABASE = os.path.join(DB_DIR, "channels.db")
        return sqlite3.connect(DATABASE)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS influencers (
            channel_id TEXT PRIMARY KEY,
            title TEXT,
            country TEXT,
            subscribers INTEGER,
            views INTEGER,
            video_count INTEGER,
            url TEXT,
            type TEXT CHECK(type IN ('c', 't'))
        )
    ''')
    conn.commit()
    conn.close()

def save_channel(info):
    conn = get_connection()
    cursor = conn.cursor()

    if DB_TYPE == "postgres":
        query = '''
            INSERT INTO influencers (channel_id, title, country, subscribers, views, video_count, url, type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (channel_id) DO UPDATE SET
                title=EXCLUDED.title,
                country=EXCLUDED.country,
                subscribers=EXCLUDED.subscribers,
                views=EXCLUDED.views,
                video_count=EXCLUDED.video_count,
                url=EXCLUDED.url,
                type=EXCLUDED.type
        '''
    else:
        query = '''
            INSERT INTO influencers (channel_id, title, country, subscribers, views, video_count, url, type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(channel_id) DO UPDATE SET
                title=excluded.title,
                country=excluded.country,
                subscribers=excluded.subscribers,
                views=excluded.views,
                video_count=excluded.video_count,
                url=excluded.url,
                type=excluded.type
        '''

    cursor.execute(query, (
        info["channel_id"], info["title"], info["country"], info["subscribers"],
        info["views"], info["video_count"], info["url"], info["type"]
    ))
    conn.commit()
    conn.close()

def export_to_csv(filename="influencers.csv"):
    full_path = os.path.join(DB_DIR, filename)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM influencers")
    rows = cursor.fetchall()
    conn.close()

    with open(full_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["channel_id", "title", "country", "subscribers", "views", "video_count", "url", "type"])
        writer.writerows(rows)

    print(f"📁 CSV экспортирован: {full_path}")

def close_db():
    pass
