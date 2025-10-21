import os 
import requests
import websockets
import json
import re
from pathlib import Path

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

# URL FUNCTIONS

def judotv_contest_information(comp_id: int):
    
    #SACAR HORA ACTUAL EN EL FORMATO HARDCODEADO EN LA URL
    url = f'https://judotv.com/api/v2/contests?IdCompetition={comp_id}&ForLive=true&Limit=5000&WithEmpty=trueW&WithWinners=false&UpdatedAtMin=2025-10-20T00:47:00'
    
    contest_information_json = requests.get(url).json()


def judotv_fragments_consult(comp_id: int):
    url = f'https://judotv.com/api/v2/competitions/{comp_id}/fragments'
    
    fragments_json = requests.get(url).json

<<<<<<< HEAD
=======

>>>>>>> 1fc0481 ( Class Mat, Championship & Round added, 20% implemented)
def judotv_commentator_channels_consult(comp_id: int):

    url = f'https://judotv.com/api/v2/competitions/{comp_id}/commentator-channels'
    
    comm_channels_response = requests.get(url).json()
    print(comm_channels_response)










