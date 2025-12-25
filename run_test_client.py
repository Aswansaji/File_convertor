import io
import os
from PIL import Image
from main import app

# create an in-memory image
img = Image.new('RGB', (100, 60), (0, 128, 200))
buf = io.BytesIO()
img.save(buf, format='JPEG')
buf.seek(0)

data = {
    'file': (buf, 'sample.jpg'),
    'format': 'pdf'
}

with app.test_client() as client:
    resp = client.post('/', data=data, content_type='multipart/form-data')
    print('Status code:', resp.status_code)
    open('run_test_response.html', 'wb').write(resp.data)

# check uploads directory
uploads = os.path.abspath('uploads')
converted = os.path.abspath('converted')
print('Uploads exists:', os.path.exists(uploads))
print('Uploads contents:', os.listdir(uploads) if os.path.exists(uploads) else [])
print('Converted contents:', os.listdir(converted) if os.path.exists(converted) else [])
