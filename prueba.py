import requests
import regex as re
from bs4 import BeautifulSoup as bs
from session_data import (cookies, headers)
import json

JUDO_LIMA_GP_URL = "https://judotv.com/competitions/eju_u23_mda2025/overview"

championship_overview_html = requests.get(JUDO_LIMA_GP_URL, 
                                    cookies=cookies, headers=headers).text

soup = bs(championship_overview_html, 'html.parser')

championship_information_raw_json = soup.find('script', attrs={'data-nuxt-data': 'nuxt-app'})

json_parsed = json.loads(championship_information_raw_json.text)


svue_query_index = json_parsed[5]['$svue-query']

queries_index = json_parsed[svue_query_index]['queries']

nineth_index = json_parsed[queries_index][9]

state_index = json_parsed[nineth_index]['state']

data_index = json_parsed[state_index]['data']

id_competition_index = json_parsed[data_index][0]

id_competition = json_parsed[id_competition_index]
name_competition = json_parsed[id_competition_index + 1]

print(id_competition)
print(name_competition)
print(json_parsed[data_index])