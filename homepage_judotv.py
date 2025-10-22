import time
import asyncio
import json
import requests
from bs4 import BeautifulSoup as bs
from constants import (JUDO_TV_HOME_URL, CHAMPIONSHIP_NAME_H1_CLASS)
from session_data import cookies, headers
from utils import (websocket_judotv,
                   ijf_LivePlayback_consult,
                   stream_mux_consult, consult_championship_name, 
                   )
from models import Streaming

streaming = Streaming('lima', 1, 2, 'final')
# seteamos el link de live actual en None, porque aun
# no lo tenemos

def extract_current_live_url() -> str:
    current_live_url = None

    while current_live_url is None:
        # HOME PAGE JUDO TV HTML
        home_html = requests.get(JUDO_TV_HOME_URL).text
        soup = bs(home_html, 'html.parser')
        
        # Fetching "Watch Live" <a> html label 
        a_label_current_live = soup.find('a', class_="bg-primary")
        
        
        if a_label_current_live.text == "Watch Live":
    
            # Extracting href link from current championship live
            href_live_actual = soup.find('a', class_="bg-primary")['href']
            current_live_url = JUDO_TV_HOME_URL + href_live_actual

    return current_live_url


def inspect_current_live_html(current_live_url):
    # HTML DE HOMEPAGE DEL LIVE ACTUAL
    live_homepage_html = requests.get(current_live_url, 
                                      headers=headers, cookies=cookies)
    soup = bs(live_homepage_html.text, 'html.parser')

    return soup

def consult_championship_name(current_live_soup) -> str:
    soup = current_live_soup 

    championship_name = soup.find('h1', class_=CHAMPIONSHIP_NAME_H1_CLASS).text
    return championship_name
    
def consult_current_championship_phase(current_live_soup) -> str:
    soup = current_live_soup

    championship_phase = soup.find('span', class_='font-bold').text
    return championship_phase

if __name__ == "__main__":
    current_live_url = extract_current_live_url()
    current_live_html = inspect_current_live_html(current_live_url)

    championship_name = consult_championship_name(current_live_html)

    print(championship_name)

    stream_mux_url = ijf_LivePlayback_consult()
    manifest_hls_url = stream_mux_consult(stream_mux_url)

    print(manifest_hls_url)

    asyncio.run(websocket_judotv())





