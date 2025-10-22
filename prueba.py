import requests
import regex as re
from bs4 import BeautifulSoup as bs
from session_data import (cookies, headers)
import json
from utils import(parse_championship_id, get_championship_comms_channels,
                  get_championship_contest_information, 
                  get_championship_fragments, 
                  websocket_json_parser, calculate_current_championship_day, 
                  parse_current_championship_json, parse_start_date,
                  parse_championship_data, get_competition_json, 
                  parse_competition_id, parse_competition_start_date, consult_championship_name)

championship_name = "Guadalajara Grand Prix 2025"

judo_mex_gp_url = "https://judotv.com/competitions/gp_mex2025/overview"

championship_overview_html = requests.get(judo_mex_gp_url, 
                                    cookies=cookies, headers=headers).text

soup = bs(championship_overview_html, "html.parser")

competition_json = get_competition_json(championship_name) 

championship_id = parse_competition_id(competition_json)

championship_start_date = parse_competition_start_date(competition_json) 

comms_channels = get_championship_comms_channels(championship_id)

all_championship_contests = get_championship_contest_information(championship_id)

championship_fragments = get_championship_fragments(championship_id)

championship_fragments = get_championship_fragments(championship_id)

for fragment in championship_fragments:
    print(calculate_current_championship_day(fragment, championship_start_date))
    pass
    
