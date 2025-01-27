import re
from bs4 import BeautifulSoup
import requests
import json

def get_text(link):
    i = link.split('/')[4]
    t = requests.get(link).text
    s = BeautifulSoup(t, "html.parser")
    descr = s.select('div p')[0].text
    return descr,i

baseUrl = "https://boardgamegeek.com"
url = "https://boardgamegeek.com/browse/boardgamesubdomain"
page_text = requests.get(url).text
soup = BeautifulSoup(page_text, "html.parser")
tr_links = soup.select('tr a')
links = [(baseUrl+link["href"],link.text) for link in tr_links if link.text != '']

mechanics = [
        (link[1], get_text(link[0])) for link in links
        ]

with open('../data/subdomains', 'w+') as f:
    for m in mechanics:
        f.write(f"{m[0]}\t{m[1][0].replace('\n', ' ')}\t{m[1][1]}\n")
