import sys
import subprocess

# ensure dependencies
try:
    from PIL import Image
except Exception:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pillow'])
    from PIL import Image

try:
    import requests
except Exception:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
    import requests

# create a sample image
img = Image.new('RGB', (200, 120), (200, 50, 50))
img_path = 'test_upload.jpg'
img.save(img_path, 'JPEG')

url = 'http://127.0.0.1:5000'
files = {'file': open(img_path, 'rb')}
data = {'format': 'pdf'}
print('Posting', img_path, '->', url)
r = requests.post(url, files=files, data=data)
print('Status:', r.status_code)
open('upload_response.html', 'wb').write(r.content)
print('Saved response to upload_response.html')
