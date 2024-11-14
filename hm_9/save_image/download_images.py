import requests
from pathlib import Path

url = 'https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png'
def load_image(url, save_path):
    try:
        r = requests.get(url)
        if r.status_code == 200:

            with open('image.jpg', 'wb') as file:
                file.write(r.content)
            print('content saved')
        else:
            print('Error',r.status_code)
    except Exception as e:
        print('Error',e)

load_image(url,Path())