import time
import os
from keywords import keywords_by_lang
from youtube_api import search_channels, get_channel_info
from database import init_db, save_channel, close_db, export_to_csv
from config import LANGUAGE_REGIONS, MIN_SUBSCRIBERS, REQUEST_DELAY
from database import DATABASE

def main():
    print("📂 Используемая база данных:", os.path.abspath(DATABASE))
    init_db()  # ✅ ОБЯЗАТЕЛЬНО инициализируем таблицу

    for lang, keywords in keywords_by_lang.items():
        print(f"\n🔍 Searching for: {lang.upper()}")
        for query in keywords:
            print(f"→ Query: {query}")
            try:
                channel_ids = search_channels(query, max_results=10)
                print(f"🔎 Найдено {len(channel_ids)} каналов")
                for cid in channel_ids:
                    time.sleep(REQUEST_DELAY)
                    info = get_channel_info(cid)
                    print(f"📦 Info: {info}")  # ⚠️ Проверка, что info не None

                    if info and info["subscribers"] >= MIN_SUBSCRIBERS:
                        save_channel(info)
                        print(f"✔️ Сохранён: {info['title']} | {info['subscribers']} subs")
                    else:
                        print(f"ℹ️ Пропущен: подписчиков меньше {MIN_SUBSCRIBERS}")
            except Exception as e:
                print(f"❌ Ошибка запроса: {e}")

    export_to_csv()
    close_db()
    print("✅ Готово!")

if __name__ == '__main__':
    main()
