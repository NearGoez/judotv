import os 
import requests
import websockets
import json
from datetime import datetime
import re
from pathlib import Path
from bs4 import BeautifulSoup as bs
from constants import CHAMPIONSHIP_NAME_H1_CLASS

def websocket_json_parser(data):
    if isinstance(data, str):
        data = json.loads(data)
    
    packet = data.get("packet", {})
    
    # Datos básicos
    round_desc = packet.get("RoundDescription", "")
    category_long = packet.get("CategoryLong", "")
    gender = "M" if packet.get("Gender") == "1" else "F"
    
    # Nombres y países
    white_name = packet.get("NameWhiteLong", "").upper()
    blue_name = packet.get("NameBlueLong", "").upper()
    white_nation = packet.get("NationWhite", "")
    blue_nation = packet.get("NationBlue", "")
    
    # Evento
    event_id = packet.get("IDEvent", "")
    event_clean = event_id.replace("gp_", "").replace("_", " ").title()
    
    # Formato final
    formatted = "🏆 {} {} {} ({}) vs {} ({}) {} 🏆".format(
        round_desc, 
        category_long, 
        white_name, 
        white_nation, 
        blue_name, 
        blue_nation, 
        event_clean
    )
    return formatted

async def websocket_judotv():
    url = "wss://wsrt.ijf.org/"
    async with websockets.connect(url) as ws:
        print("Conectado")
        async for message in ws:
            print("Mensaje:", websocket_json_parser(message))

def consult_championship_name(current_live_soup) -> str:
    soup = current_live_soup 

    championship_name = soup.find('h1', class_=CHAMPIONSHIP_NAME_H1_CLASS).text
    return championship_name
# URL FUNCTIONS

def get_championship_contest_information(comp_id: int) -> list[dict]:
    #SACAR HORA ACTUAL EN EL FORMATO HARDCODEADO EN LA URL
    url = f'https://judotv.com/api/v2/contests?IdCompetition={comp_id}&ForLive=true&Limit=5000&WithEmpty=true'

    contest_information_dict = requests.get(url).json()

    return contest_information_dict

def get_championship_fragments(comp_id: int) -> list[dict]:
    url = f'https://judotv.com/api/v2/competitions/{comp_id}/fragments'
    
    fragments_information_dict = requests.get(url).json()

    return fragments_information_dict

def get_championship_comms_channels(comp_id: int) -> list[dict]:

    url = f'https://judotv.com/api/v2/competitions/{comp_id}/commentator-channels'
    
    comm_channels_dict = requests.get(url).json()

    return comm_channels_dict

def get_competition_json(competition_name) -> dict:
    url = 'https://judotv.com/api/v2/competitions'

    all_competitions = requests.get(url).json()

    for competition_json in all_competitions['list']:

        if competition_json.get('name') == competition_name:
            return competition_json

def parse_competition_id(competition_json: dict) -> int:

    competition_id = competition_json['idCompetition']
    return competition_id

def parse_competition_start_date(competition_json: dict) -> str:

    return competition_json['dateFrom']



def parse_current_championship_json(championship_overview_html: bs) -> list[dict]:

    championship_info_raw_json = championship_overview_html.find(
        'script',
        attrs={
            'data-nuxt-data': 'nuxt-app'
        }
    )
    parsed_championship_json = json.loads(championship_info_raw_json.text)

    with open('garbage/championship_info.json', 'w') as f:
        f.write(championship_info_raw_json.text)

    return parsed_championship_json


def parse_championship_data(championship_json: list[dict]) -> dict:

    svue_query_index = championship_json[5]['$svue-query']
    queries_index = championship_json[svue_query_index]['queries']
    nineth_index = championship_json[queries_index][9]
    state_index = championship_json[nineth_index]['state']
    data_index_index = championship_json[state_index]['data']
    data_index = championship_json[data_index_index][0]

    print(f"{svue_query_index=}")
    print(f"{queries_index=}")
    print(f"{nineth_index=}")
    print(f"{state_index=}")
    print(f"{data_index_index=}")
    print(f"{data_index=}")


    championship_data = championship_json[data_index]

    return championship_data

def parse_championship_id(championship_data: dict, championship_json: list[dict]) -> int:


    competition_id_index = championship_data['idCompetition']


    competition_id = championship_json[competition_id_index]
    
    return competition_id

def parse_start_date(championship_data, championship_json: list[dict]) -> int:

    start_date_index = championship_data['dateFrom']
    start_date = championship_json[start_date_index]
    
    return start_date


def calculate_current_championship_day(fragment_json: dict, 
                                       championship_start_date: str):

    format = "%Y-%m-%dT%H:%M:%S"

    fragment_start_date = fragment_json['dateTimeStart']

    dt_fragment_start = datetime.strptime(fragment_start_date, format)
    dt_championship_start= datetime.strptime(championship_start_date, format)

    diff = dt_fragment_start  - dt_championship_start

    # We return diff plus one because the championship days are counted
    # from one (Day 1, Day 2, Day 3)

    return diff.days + 1
    
def resume_contest_json(contest_json: dict) -> str:
    pass

