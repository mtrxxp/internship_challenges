import os
import csv
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from zoneinfo import ZoneInfo  # встроенный модуль (Python 3.9+)

load_dotenv()

# Тип БД: postgres или sqlite
DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()

# Директория и файл БД для SQLite
DB_DIR = os.path.join(os.path.dirname(__file__), "databases")
os.makedirs(DB_DIR, exist_ok=True)
DATABASE = os.path.join(DB_DIR, "channels.db")


def get_connection():
    """Возвращает соединение с БД (Postgres или SQLite)."""
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
        return sqlite3.connect(DATABASE)


def init_db():
    """Создаёт таблицу influencers если её нет."""
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
            type TEXT CHECK(type IN ('c', 't')),
            scraped_at TEXT,
            found_keywords TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_channel(info: dict):
    """Сохраняет или обновляет информацию о канале."""

    conn = get_connection()
    cursor = conn.cursor()

    # время в часовом поясе Варшавы
    scraped_at = datetime.now(ZoneInfo("Europe/Warsaw")).strftime("%Y-%m-%d %H:%M:%S")

    # гарантируем строку для keywords
    keywords = info.get("keywords")
    if isinstance(keywords, list):
        found_keywords = ",".join(keywords)
    elif isinstance(keywords, str):
        found_keywords = keywords
    else:
        found_keywords = ""

    if DB_TYPE == "postgres":
        query = '''
            INSERT INTO influencers (channel_id, title, country, subscribers, views, video_count, url, type, scraped_at, found_keywords)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (channel_id) DO UPDATE SET
                title=EXCLUDED.title,
                country=EXCLUDED.country,
                subscribers=EXCLUDED.subscribers,
                views=EXCLUDED.views,
                video_count=EXCLUDED.video_count,
                url=EXCLUDED.url,
                type=EXCLUDED.type,
                scraped_at=EXCLUDED.scraped_at,
                found_keywords=EXCLUDED.found_keywords
        '''
    else:
        query = '''
            INSERT INTO influencers (channel_id, title, country, subscribers, views, video_count, url, type, scraped_at, found_keywords)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(channel_id) DO UPDATE SET
                title=excluded.title,
                country=excluded.country,
                subscribers=excluded.subscribers,
                views=excluded.views,
                video_count=excluded.video_count,
                url=excluded.url,
                type=excluded.type,
                scraped_at=excluded.scraped_at,
                found_keywords=excluded.found_keywords
        '''

    cursor.execute(query, (
        info["channel_id"],
        info.get("title"),
        info.get("country"),
        info.get("subscribers", 0),
        info.get("views", 0),
        info.get("video_count", 0),
        info.get("url"),
        info.get("type", "c"),
        scraped_at,
        found_keywords
    ))

    conn.commit()
    conn.close()


def export_to_csv(filename="influencers.csv"):
    """Экспортирует данные из БД в CSV."""
    full_path = os.path.join(DB_DIR, filename)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM influencers")
    rows = cursor.fetchall()
    conn.close()

    with open(full_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "scraped_at",
            "found_keywords",
            "channel_id",
            "title",
            "country",
            "subscribers",
            "views",
            "video_count",
            "url",
            "type"
        ])
        writer.writerows(rows)

    print(f"📁 CSV exported into: {full_path}")


def close_db():
    """На будущее (если нужен пул соединений)."""
    pass


# Если запускать напрямую: создаём БД
if __name__ == "__main__":
    init_db()
    print("✅ Database initialized")
