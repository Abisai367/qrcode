from io import BytesIO

from flask import Flask, request, send_file, make_response, jsonify
import qrcode

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate_qr():
    if request.method == 'OPTIONS':
        return make_response('', 204)

    url = request.form.get('url', '').strip()
    image_name = request.form.get('image_name', '').strip()
    qrcolor = request.form.get('qrcolor', '').strip() or 'black'

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=qrcolor, back_color='white').convert('RGB')

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    filename = image_name if image_name else 'qrcode'
    if not filename.lower().endswith('.png'):
        filename += '.png'

    return send_file(
        buffer,
        mimetype='image/png',
        as_attachment=False,
        download_name=filename,
    )


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
