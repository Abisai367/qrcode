from urllib import request
import uuid

fields = {'url': 'https://www.google.com', 'image_name': 'test-qr'}
boundary = '----WebKitFormBoundary' + uuid.uuid4().hex
lines = []
for key, value in fields.items():
    lines.append('--' + boundary)
    lines.append(f'Content-Disposition: form-data; name="{key}"')
    lines.append('')
    lines.append(value)
lines.append('--' + boundary + '--')
lines.append('')
body = '\r\n'.join(lines).encode('utf-8')
req = request.Request('http://127.0.0.1:5000/generate', data=body, method='POST')
req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
with request.urlopen(req) as resp:
    print(resp.status)
    print(resp.getheader('Content-Type'))
    data = resp.read(16)
    print(data)
