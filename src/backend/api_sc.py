from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DATABASE = "./youtube_scrapper_for_internship-main/channels.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # So we get dict-like rows
    return conn

@app.route("/channels", methods=["GET"])
def get_channels():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT channel_id, title, country, subscribers, views, video_count, url FROM influencers")
    rows = cursor.fetchall()
    conn.close()
    channels = []
    for row in rows:
        channels.append({
            "channel_id": row["channel_id"],
            "title": row["title"],
            "country": row["country"],
            "subscribers": row["subscribers"],
            "views": row["views"],
            "video_count": row["video_count"],
            "url": row["url"]
        })
    return jsonify(channels)

if __name__ == "__main__":
    app.run(debug=True)
