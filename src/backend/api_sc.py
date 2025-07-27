from flask import Flask, jsonify, request
from flask_cors import CORS
from celery import Celery
import subprocess
import sqlite3
from flask import send_file

app = Flask(__name__)
CORS(app)

# === DATABASE ===
DATABASE = "./youtube_scrapper_for_internship-main/channels.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/channels", methods=["GET"])
def get_channels():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT channel_id, title, country, subscribers, views, video_count, url FROM influencers")
    rows = cursor.fetchall()
    conn.close()
    channels = [{
        "channel_id": row["channel_id"],
        "title": row["title"],
        "country": row["country"],
        "subscribers": row["subscribers"],
        "views": row["views"],
        "video_count": row["video_count"],
        "url": row["url"]
    } for row in rows]
    return jsonify(channels)

# === CELERY CONFIG ===
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.route('/start_scrape', methods=['POST'])
def start_scrape():
    task = run_scraper.delay()
    return jsonify({"task_id": task.id}), 202

@app.route('/scrape_status/<task_id>', methods=['GET'])
def scrape_status(task_id):
    try:
        task = run_scraper.AsyncResult(task_id)
        if task.state == 'PENDING':
            return jsonify({'status': 'pending'}), 200
        elif task.state == 'SUCCESS':
            return jsonify({'status': 'completed'}), 200
        elif task.state == 'FAILURE':
            return jsonify({
                'status': 'failed',
                'error': str(task.result),  # Добавим причину ошибки
                'traceback': task.traceback  # Отладка
            }), 500
        else:
            return jsonify({'status': task.state.lower()}), 200
    except Exception as e:
        print("🔥 Ошибка в /scrape_status:", str(e))
        return jsonify({'error': str(e)}), 500

# ✅ ВОТ ЭТО — ОБНОВЛЁННЫЙ run_scraper
@celery.task
def run_scraper():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM influencers")  # Удалить все записи
        conn.commit()
        conn.close()
        print("🧹 База данных очищена перед запуском скрапа.")
    except Exception as e:
        print("⚠️ Ошибка при очистке БД:", e)


    try:
        result = subprocess.run(
            ["python", "main.py"],
            check=True,
            capture_output=True,
            text=True,
            cwd="youtube_scrapper_for_internship-main"  # 👈 Укажи рабочую директорию!
        )
        print("✅ Scraping completed:", result.stdout)
        return {"status": "completed", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        print("❌ Scraping failed:", e.stderr)
        return {"status": "failed", "error": str(e), "traceback": e.stderr}

@app.route("/download_csv", methods=["GET"])
def download_csv():
    csv_path = "./youtube_scrapper_for_internship-main/influencers.csv"
    if not os.path.exists(csv_path):
        return jsonify({"error": "CSV file not found"}), 404

    return send_file(csv_path, as_attachment=True, download_name="influencers.csv")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)