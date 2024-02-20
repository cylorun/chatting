import sqlite3
from PIL import Image
from io import BytesIO

# Connect to the SQLite database
conn = sqlite3.connect("C:\\Users\\alfgr\\Desktop\\school\\forri2-verk\\server\\db\\app.db")
cursor = conn.cursor()

# Assuming you have a table named 'images' with columns 'id' and 'data'
cursor.execute("SELECT date,file FROM files")
rows = cursor.fetchall()

for row in rows:
    date, blob_data = row
    image = Image.open(BytesIO(blob_data))
    image = image.convert('RGB')
    filename = f"image_.jpg"  
    image.save(filename)

conn.close()
