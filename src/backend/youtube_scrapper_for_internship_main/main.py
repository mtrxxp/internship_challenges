import time
import os
import sys
sys.path.append("/app")
from youtube_scrapper_for_internship_main.keywords import keywords_by_lang
from youtube_scrapper_for_internship_main.youtube_api import search_channels, get_channel_info
from youtube_scrapper_for_internship_main.database import init_db, save_channel, close_db, export_to_csv, DATABASE
from youtube_scrapper_for_internship_main.config import LANGUAGE_REGIONS, MIN_SUBSCRIBERS, REQUEST_DELAY
from youtube_scrapper_for_internship_main.utils import split_tables
from youtube_scrapper_for_internship_main.state import is_stop_flag_set

def main():
    print("📂 Используемая база данных:", os.path.abspath(DATABASE))
    init_db()

    try:
        for lang, keywords in keywords_by_lang.items():
            print(f"\n🔍 Searching for: {lang.upper()}")
            for query in keywords:
                print(f"→ Query: {query}")
                if is_stop_flag_set():
                    print("🛑 Скрапинг остановлен пользователем")
                    return
                try:
                    channel_ids = search_channels(query, max_results=10)
                    print(f"🔎 Найдено {len(channel_ids)} каналов")
                    for cid in channel_ids:
                        time.sleep(REQUEST_DELAY)
                        info = get_channel_info(cid)
                        print(f"📦 Info: {info}")

                        if info and info["subscribers"] >= MIN_SUBSCRIBERS:
                            save_channel(info)
                            print(f"✔️ Сохранён: {info['title']} | {info['subscribers']} subs")
                        else:
                            print(f"ℹ️ Пропущен: подписчиков меньше {MIN_SUBSCRIBERS}")
                except Exception as e:
                    print(f"❌ Ошибка запроса: {e}")

    finally:
        print("💾 Сохраняем CSV и разбиваем таблицы...")
        close_db()
        print("✅ Готово!")

if __name__ == '__main__':
    main()
