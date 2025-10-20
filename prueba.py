import requests
import regex as re
from bs4 import BeautifulSoup as bs
from session_data import (cookies, headers)
import json

JUDO_TV_HOME_URL = "https://judotv.com/"

homepage_judotv_html = requests.get(JUDO_TV_HOME_URL, 
                                    cookies=cookies, headers=headers).text

soup = bs(homepage_judotv_html, 'html.parser')

championship_name_div = soup.find(string=re.compile("3081"), recursive=True)


for i, node in enumerate(championship_name_div.parent):

    with open(f'nodo{i}.json', 'w') as f:
        f.write(node)

    nodo_procesado = json.loads(node)
    print(nodo_procesado)


