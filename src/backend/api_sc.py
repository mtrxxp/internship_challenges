from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from celery import Celery
from flask import send_from_directory
import glob
import subprocess
import os
import sqlite3
from youtube_scrapper_for_internship_main.state import set_stop_flag
from youtube_scrapper_for_internship_main.database import DATABASE, export_to_csv
from youtube_scrapper_for_internship_main.utils import split_tables



app = Flask(__name__)
CORS(app)

celery = Celery(app.name, broker='redis://redis:6379/0', backend='redis://redis:6379/0')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/stop_scrape', methods=['POST'])
def stop_scrape():
    set_stop_flag()
    export_to_csv() 
    split_tables()
    return jsonify({"status": "stopping"}), 200

@app.route('/channels', methods=['GET'])
def get_channels():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM influencers")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


@app.route('/download_csv/<filename>', methods=['GET'])
def download_csv(filename):
    csv_dir = os.path.join(os.path.dirname(__file__), "youtube_scrapper_for_internship_main", "databases")

    if not filename.endswith(".csv") or not os.path.exists(os.path.join(csv_dir, filename)):
        return jsonify({"error": "CSV file not found"}), 404

    return send_from_directory(csv_dir, filename, as_attachment=True)

@app.route('/start_scrape', methods=['POST'])
def start_scrape():
    task = run_scraper.delay()
    return jsonify({"task_id": task.id}), 202

@app.route('/scrape_status/<task_id>', methods=['GET'])
def scrape_status(task_id):
    task = run_scraper.AsyncResult(task_id)
    if task.state == 'PENDING':
        return jsonify({'status': 'pending'}), 200
    elif task.state == 'SUCCESS':
        return jsonify({'status': 'completed'}), 200
    elif task.state == 'FAILURE':
        return jsonify({'status': 'failed', 'error': str(task.result), 'traceback': task.traceback}), 500
    return jsonify({'status': task.state.lower()}), 200

@app.route('/csv_files', methods=['GET'])
def list_csv_files():
    csv_dir = os.path.join(os.path.dirname(__file__), "youtube_scrapper_for_internship_main", "databases")
    try:
        files = [f for f in os.listdir(csv_dir) if f.endswith(".csv")]
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@celery.task
def run_scraper():
    # Удаляем старые CSV перед новым запуском
    for file in glob.glob("youtube_scrapper_for_internship_main/databases/*.csv"):
        os.remove(file)

    try:
        result = subprocess.run(
            ["python", "main.py"],
            cwd="youtube_scrapper_for_internship_main",
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ Скрэпинг завершён:", result.stdout)

    except subprocess.CalledProcessError as e:
        print("❌ Ошибка при запуске main.py:", e.stderr)

    finally:
        # Гарантируем сохранение CSV в любом случае
        try:
            from youtube_scrapper_for_internship_main.database import export_to_csv
            from youtube_scrapper_for_internship_main.utils import split_tables
            from youtube_scrapper_for_internship_main.state import clear_stop_flag

            print("💾 Финальное сохранение CSV и разбиение таблиц...")
            export_to_csv()
            split_tables()
            clear_stop_flag()

        except Exception as ex:
            print("⚠️ Не удалось сохранить CSV:", ex)

    return {"status": "done"}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
