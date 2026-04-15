import requests

API = "https://wiki.saude.gov.br/SISREG/api.php"

def get_all_titles():
    titles = []
    params = {
        "action": "query",
        "list": "allpages",
        "aplimit": "500",
        "format": "json"
    }

    while True:
        r = requests.get(API, params=params).json()

        for p in r["query"]["allpages"]:
            titles.append(p["title"])

        if "continue" in r:
            params.update(r["continue"])
        else:
            break

    return titles

titles = get_all_titles()

print(f"Total de páginas: {len(titles)}")

with open("paginas.txt", "w", encoding="utf-8") as f:
    for t in titles:
        f.write(t + "\n")

chunk_size = 200

for i in range(0, len(titles), chunk_size):
    with open(f"paginas_{i}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(titles[i:i+chunk_size]))