from flask import Flask, request, send_file, jsonify
import qrcode
from io import BytesIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
