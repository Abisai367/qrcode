from io import BytesIO
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import qrcode

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/generate', methods=['POST'])
def generate_qr():
    url = request.form.get('url', '').strip()
    image_name = request.form.get('image_name', '').strip()
    qrcolor = request.form.get('qrcolor', '').strip()

    if not qrcolor:
        qrcolor = 'black'

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    if qrcolor.startswith('#'):
        qrcolor = qrcolor[1:]

    try:
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
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
