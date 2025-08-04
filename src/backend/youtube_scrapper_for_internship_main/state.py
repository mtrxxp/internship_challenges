import os

FLAG_PATH = "/app/youtube_scrapper_for_internship_main/databases/stop.flag"

def set_stop_flag():
    with open(FLAG_PATH, "w") as f:
        f.write("1")

def clear_stop_flag():
    if os.path.exists(FLAG_PATH):
        os.remove(FLAG_PATH)

def is_stop_flag_set():
    exists = os.path.exists(FLAG_PATH)
    print(f"📍 is_stop_flag_set: {exists}")
    return exists
