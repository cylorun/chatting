import sqlite3, requests, base64
from PIL import Image
from io import BytesIO


d = requests.get('http://localhost:25565/api/channel/1')
blob_data = base64.b64decode(d.json()['files'][0]['data'])
image = Image.open(BytesIO(blob_data))
image = image.convert('RGB')
filename = f"image_.jpg"  
image.save(filename)

