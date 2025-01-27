import re
from bs4 import BeautifulSoup
import requests
import json

def get_text(link):
    t = requests.get(link).text
    s = BeautifulSoup(t, "html.parser")
    scripts = s.find_all("script")
    items = [script for script in scripts if 'itemPreload' in script.text][0].text.split(';\n')
    descr = [x for x in items if 'itemPreload' in x][0]
    descr = descr.strip().split('itemPreload = ')[1]
    i = json.loads(descr)['item']['id']
    item = json.loads(descr)['item']['description']
    item = BeautifulSoup(item, 'html.parser')
    ret = item.text.strip()
    return ret,i

baseUrl = "https://boardgamegeek.com"
url = "https://boardgamegeek.com/browse/boardgamecategory"
page_text = requests.get(url).text
soup = BeautifulSoup(page_text, "html.parser")
tr_links = soup.select('tr a')
links = [(baseUrl+link["href"],link.text) for link in tr_links]

mechanics = [
        (link[1], get_text(link[0])) for link in links
        ]

with open('../data/categories', 'w+') as f:
    for m in mechanics:
        f.write(f"{m[0]}\t{m[1][0].replace('\n', ' ')}\t{m[1][1].strip()}\n")
