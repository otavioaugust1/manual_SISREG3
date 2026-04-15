import requests
import os

API = "https://wiki.saude.gov.br/SISREG/api.php"
os.makedirs("images", exist_ok=True)

def get_image_url(filename):
    params = {
        "action": "query",
        "titles": f"File:{filename}",
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }

    r = requests.get(API, params=params).json()
    pages = r["query"]["pages"]

    for p in pages.values():
        if "imageinfo" in p:
            return p["imageinfo"][0]["url"]

for img in images:
    url = get_image_url(img)
    if url:
        data = requests.get(url).content
        with open(f"images/{img}", "wb") as f:
            f.write(data)

print("Imagens baixadas!")