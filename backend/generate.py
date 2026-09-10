from io import BytesIO
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import qrcode
from qrcode.image.pil import PilImage

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/generate', methods=['POST'])
def generate_qr():
    url = request.form.get('url', '').strip()
    image_name = request.form.get('image_name', '').strip()
    qrcolor = request.form.get('qrcolor', '').strip()

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    if not qrcolor:
        qrcolor = '#000000'

    try:
        qr = qrcode.QRCode(box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(image_factory=PilImage)
        
        img = img.convert('RGB')
        
        pixels = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixels[x, y] == (0, 0, 0):
                    if qrcolor.startswith('#'):
                        hex_val = qrcolor[1:]
                        pixels[x, y] = tuple(int(hex_val[i:i+2], 16) for i in (0, 2, 4))
                    else:
                        pixels[x, y] = (0, 0, 0)

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
