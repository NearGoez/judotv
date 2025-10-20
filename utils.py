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


def descargar_y_guardar_chunk(chunk_url, descargados, save_dir):
    if chunk_url in descargados:
        return

    chunk_filename = chunk_url.split("/")[-1].split(".ts")[0]
    full_path = os.path.join(save_dir, f"{chunk_filename}.ts")

    if Path(full_path).exists():
        descargados.add(chunk_url)
        return

    print(f"Descargando chunk {chunk_filename}...")
    chunk_data = requests.get(chunk_url).content
    
    with open(full_path, "wb") as f:
        f.write(chunk_data)

    print(f"Chunk {chunk_filename} guardado.")
    descargados.add(chunk_url)

def download_all_chunks(m3u8_url, descargados, save_dir):
    r = requests.get(m3u8_url)
    r.raise_for_status()
    lines = r.text.strip().splitlines()

    # Filtrar líneas que tengan ".ts" en cualquier parte
    ts_chunks = [line for line in lines if ".ts" in line]

    for chunk_url in ts_chunks:
        descargar_y_guardar_chunk(chunk_url, descargados, save_dir)


    
def get_highest_res_manifest_from_text(manifest_text: str) -> str:
    # Regex: captura ancho, alto y la URL que viene en la siguiente línea
    pattern = re.compile(
        r'RESOLUTION=(\d+)x(\d+)[^\n]*\n([^\s#][^\n]*)'
    )

    matches = pattern.findall(manifest_text)
    if not matches:
        raise ValueError("No se encontraron resoluciones en el texto del manifest")

    # Convertimos cada coincidencia a (ancho, alto, url)
    renditions = [(int(w), int(h), url.strip()) for w, h, url in matches]

    # Elegimos la de mayor resolución (ancho * alto)
    best = max(renditions, key=lambda x: x[0] * x[1])

    return best[2]


# URL FUNCTIONS

def judotv_contest_information(comp_id: int):
    
    #SACAR HORA ACTUAL EN EL FORMATO HARDCODEADO EN LA URL
    url = f'https://judotv.com/api/v2/contests?IdCompetition={comp_id}&ForLive=true&Limit=5000&WithEmpty=trueW&WithWinners=false&UpdatedAtMin=2025-10-20T00:47:00'
    
    contest_information_json = requests.get(url).json()


def judotv_fragments_consult(comp_id: int):
    url = f'https://judotv.com/api/v2/competitions/{comp_id}/fragments'
    
    fragments_json = requests.get(url).json

def judotv_commentator_channels_consult(comp_id: int):

    url = f'https://judotv.com/api/v2/competitions/{comp_id}/commentator-channels'
    
    comm_channels_response = requests.get(url).json()
    print(comm_channels_response)

def ijf_LivePlayback_consult() -> str:
    url = 'https://datav2.ijf.org/Streams/LivePlaybackUrlForMux'
    
    params = {
            'Type': 'commentator',
            'IdFragment': '3895',
            'CommentatorIdx': '0',
            }
    json_response = requests.get(url, params=params).json()
    print(json_response, type(json_response))

    stream_mux_url = json_response['url']
    return stream_mux_url

def stream_mux_consult(stream_mux_url: str ) -> str:
    response  = requests.get(stream_mux_url).text

    highest_res_manifest_url = get_highest_res_manifest_from_text(response)

    return highest_res_manifest_url








