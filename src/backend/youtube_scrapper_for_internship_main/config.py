import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

LANGUAGE_REGIONS = {
    "en": ["US", "GB", "CA", "AU"],
    "ru": ["RU"],
    "pt": ["BR", "PT"],
    "fr": ["FR", "CA"],
    "de": ["DE", "AT", "CH"],
    "es": ["AR", "ES", "MX", "CL", "PE", "CO"],
    "pl": ["PL"],
    "uk": ["UA"],
    "tr": ["TR"],
    "hi": ["IN"],
}

MIN_SUBSCRIBERS = 10_000
REQUEST_DELAY = 1.0
USE_PROXIES = False
PROXIES = ["http://your.proxy:port"]