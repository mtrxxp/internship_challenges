from flask import Flask, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import string
import random

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class URL(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_id = db.Column(db.String(6), unique=True, nullable=False)

class Click(db.Model):
    __tablename__ = 'clicks'
    id = db.Column(db.Integer, primary_key=True)
    url_id = db.Column(db.Integer, db.ForeignKey('urls.id'), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    referrer = db.Column(db.String(500))
    user_agent = db.Column(db.String(300))
    ip_address = db.Column(db.String(100))

def generate_short_id(num_chars=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=num_chars))



@app.route('/shortener', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')

    if not original_url:
        return jsonify({'error': 'URL is required'}), 400

    while True:
        short_id = generate_short_id()
        if not URL.query.filter_by(short_id=short_id).first():
            break

    new_url = URL(original_url=original_url, short_id=short_id)
    db.session.add(new_url)
    db.session.commit()

    return jsonify({'short_url': request.host_url + short_id})

@app.route('/<short_id>')
def redirect_url(short_id):
    url = URL.query.filter_by(short_id=short_id).first()
    if url:
        click = Click(
            url_id=url.id,
            referrer=request.referrer,
            user_agent=request.headers.get('User-Agent'),
            ip_address=request.remote_addr
        )
        db.session.add(click)
        db.session.commit()

        return redirect(url.original_url)
    else:
        return jsonify({'error': 'Invalid short URL'}), 404

@app.route('/analytics/<short_id>', methods=['GET'])
def analytics(short_id):
    url = URL.query.filter_by(short_id=short_id).first()
    if not url:
        return jsonify({'error': 'Invalid short URL'}), 404

    clicks = Click.query.filter_by(url_id=url.id).all()
    click_data = []
    for click in clicks:
        click_data.append({
            'timestamp': click.timestamp.isoformat(),
            'referrer': click.referrer,
            'user_agent': click.user_agent,
            'ip_address': click.ip_address
        })

    return jsonify({
        'original_url': url.original_url,
        'short_id': url.short_id,
        'clicks': len(clicks),
        'click_data': click_data
    })

@app.route('/all_urls')
def all_urls():
    urls = URL.query.all()
    result = []
    for url in urls:
        result.append({
            'id': url.id,
            'original_url': url.original_url,
            'short_id': url.short_id
        })
    return jsonify(result)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)