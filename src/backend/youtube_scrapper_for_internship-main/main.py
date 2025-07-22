import time
from keywords import keywords_by_lang
from youtube_api import search_channels, get_channel_info
from database import save_channel, close_db, export_to_csv
from config import LANGUAGE_REGIONS, MIN_SUBSCRIBERS, REQUEST_DELAY

for lang, keywords in keywords_by_lang.items():
    print(f"\n🔍 Searching for: {lang.upper()}")
    for query in keywords:
        print(f"→ {query}")
        try:
            channel_ids = search_channels(query, max_results=10)
            for cid in channel_ids:
                time.sleep(REQUEST_DELAY)  # ⏱️ задержка
                info = get_channel_info(cid)
                if info and info["subscribers"] >= MIN_SUBSCRIBERS:
                    save_channel(info)
                    print(f"✔️ {info['title']} | {info['subscribers']} subs | {info['url']}")
                else:
                    print(f"ℹ️ Skipped (subscribers < {MIN_SUBSCRIBERS})")
        except Exception as e:
            print(f"❌ Error: {e}")

export_to_csv()
close_db()
