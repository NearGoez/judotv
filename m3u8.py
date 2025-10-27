import requests 
import os
import re
from pathlib import Path
from typing import Any

def descargar_y_guardar_chunk(chunk_url: str, descargados: set[str], save_dir: str):
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

def ijf_LivePlayback_consult(id_fragment: int, comm_id: int) -> str:
    url = 'https://datav2.ijf.org/Streams/LivePlaybackUrlForMux'
    
    params: dict[str, Any] = {
            'Type': 'commentator',
            'IdFragment': id_fragment,
            'CommentatorIdx': comm_id,
            }
    json_response = requests.get(url, params=params).json()


    stream_mux_url = json_response['url']
    return stream_mux_url
