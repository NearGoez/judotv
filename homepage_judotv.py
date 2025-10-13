import time
import asyncio
import json
import requests
from bs4 import BeautifulSoup as bs
from constants import JUDO_TV_HOME_URL
from session_data import cookies, headers
from utils import (ping_ijforg, get_json_ijforg,
                   get_fragments_json_ijf, posible_update,
                   create_fetch, websocket_judotv
                   )
from models import Streaming

streaming = Streaming('lima', 1, 2, 'final')

# seteamos el link de live actual en None, porque aun
# no lo tenemos
url_live_actual = None

while url_live_actual is None:

# HOME PAGE JUDO TV HTML
    home_html = requests.get(JUDO_TV_HOME_URL).text
    soup = bs(home_html, 'html.parser')

# EXTRAYENNDO LINK DE CAMPEONATO ACTUAL EN DIRECTO
    href_live_actual = soup.find('a', class_="bg-primary")['href']
    url_live_actual = JUDO_TV_HOME_URL + href_live_actual

# HTML DEL LIVE DEL TORNEO
live_html = requests.get(url_live_actual, headers=headers, cookies=cookies)
soup = bs(live_html.text, 'html.parser')


asyncio.run(websocket_judotv(streaming))






