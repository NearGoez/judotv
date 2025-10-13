import requests
import os
import time
from threading import Thread
from pathlib import Path

def descargar_y_guardar_chunk(chunk_url, descargados):
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

def download_all_chunks(m3u8_url, descargados):
    r = requests.get(m3u8_url)
    r.raise_for_status()
    lines = r.text.strip().splitlines()

    # Filtrar líneas que tengan ".ts" en cualquier parte
    ts_chunks = [line for line in lines if ".ts" in line]

    for chunk_url in ts_chunks:
        descargar_y_guardar_chunk(chunk_url, descargados)

descargados = set()
m3u8_url = "https://manifest-gcp-us-east4-vop1.fastly.mux.com/16XvnWEGSOCbwAZ005qCCqEt9ZIbPVA8RX6xLog9en63GB6qlN1hWVxEg002eg8Ak4FqluTR1pVKbv02mm57D011mvhHDFjyXgmY/rendition.m3u8?cdn=fastly&exclude_pdt=false&expires=1760342400&live=1&skid=default&signature=NjhlY2E4MzRfYjk2M2MwYzBjZGMyMzAxMzBhMjg5NWMzYWM4ZmYxMjYzNzg4OWUzMTZhMjQ1ZTYzMDgwNWQ5YjExY2YxZmFlOQ==&vsid=kM3bvM76nYx7jko8Lbb9uqznP3n025UwlaFZvu2AehGG02rI5zThqf02zEF7h4zSiNhMlRABiuqphg"
save_dir = "Lima Grand Prix 2025/Dia 2/Final/fragments"
poll_interval = 4

os.makedirs(save_dir, exist_ok=True)

while True:
    try:
        r = requests.get(m3u8_url)
        r.raise_for_status()
        lines = r.text.strip().splitlines()

        # Filtrar líneas que tengan ".ts" en cualquier parte
        ts_chunks = [line for line in lines if ".ts" in line]

        download_all_chunks(m3u8_url, descargados)
        time.sleep(poll_interval)

    except Exception as e:
        print("Error:", e)
    time.sleep(poll_interval)

