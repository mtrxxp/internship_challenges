import os
import csv
from youtube_scrapper_for_internship_main.database import get_connection, DB_TYPE

DB_DIR = "youtube_scrapper_for_internship_main/databases"

def split_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS channels_only AS SELECT * FROM influencers WHERE type = %s' if DB_TYPE=="postgres" else 'CREATE TABLE IF NOT EXISTS channels_only AS SELECT * FROM influencers WHERE type = "c"', ("c",) if DB_TYPE=="postgres" else [])
    cursor.execute('CREATE TABLE IF NOT EXISTS topics_only AS SELECT * FROM influencers WHERE type = %s' if DB_TYPE=="postgres" else 'CREATE TABLE IF NOT EXISTS topics_only AS SELECT * FROM influencers WHERE type = "t"', ("t",) if DB_TYPE=="postgres" else [])

    cursor.execute('DELETE FROM channels_only')
    cursor.execute('DELETE FROM topics_only')

    cursor.execute('INSERT INTO channels_only SELECT * FROM influencers WHERE type = %s' if DB_TYPE=="postgres" else 'INSERT INTO channels_only SELECT * FROM influencers WHERE type = "c"', ("c",) if DB_TYPE=="postgres" else [])
    cursor.execute('INSERT INTO topics_only SELECT * FROM influencers WHERE type = %s' if DB_TYPE=="postgres" else 'INSERT INTO topics_only SELECT * FROM influencers WHERE type = "t"', ("t",) if DB_TYPE=="postgres" else [])

    conn.commit()
    conn.close()

    for table_name in ["channels_only", "topics_only"]:
        file_path = os.path.join(DB_DIR, f"{table_name}.csv")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        conn.close()

        with open(file_path, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["channel_id", "title", "country", "subscribers", "views", "video_count", "url", "type"])
            writer.writerows(rows)

        print(f"📁 CSV сохранён: {file_path}")

    print("✅ Таблицы обновлены и CSV сохранены.")