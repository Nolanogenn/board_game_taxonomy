import re
from bs4 import BeautifulSoup
import requests
import json

def get_text(link):
    t = requests.get(link).text
    s = BeautifulSoup(t, "html.parser")
    print(f'====={link}=====')
    scripts = s.find_all("script")
    items = [script for script in scripts if 'itemPreload' in script.text][0].text.split(';\n')
    descr = [x for x in items if 'itemPreload' in x][0]
    descr = descr.strip().split('itemPreload = ')[1]
    print(descr)
    #print('=====')
    item = json.loads(descr)['item']['description']
    item = BeautifulSoup(item, 'html.parser')
    ret = item.text.strip()
    return ret

baseUrl = "https://boardgamegeek.com"
url = "https://boardgamegeek.com/browse/boardgamemechanic"
page_text = requests.get(url).text
soup = BeautifulSoup(page_text, "html.parser")
tr_links = soup.select('tr a')
links = [(baseUrl+link["href"],link.text) for link in tr_links]

mechanics = [
        (link[1], get_text(link[0])) for link in links
        ]

with open('../data/mechanics', 'w+') as f:
    for m in mechanics:
        f.write(f"{m[0]}\t{m[1].replace('\n', ' ')}\n")
