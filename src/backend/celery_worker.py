from api_sc import celery
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "youtube_scrapper_for_internship_main"))
sys.path.append(os.path.dirname(__file__))  
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) 