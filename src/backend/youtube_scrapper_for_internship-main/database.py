
import sqlite3
from youtube_api import search_channels, get_channel_info 

DATABASE = "./youtube_scrapper_for_internship-main/channels.db"

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

def populate():
    init_db()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = "python"
    channel_ids = search_channels(query, max_results=5)

    for cid in channel_ids:
        info = get_channel_info(cid)
        if info:
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
    print("Done!")

if __name__ == "__main__":
    populate()