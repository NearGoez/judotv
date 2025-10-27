import requests
import os
import sys
import time
from threading import Thread
from pathlib import Path
from m3u8 import download_all_chunks

descargados = set()

if len(sys.argv) != 3:
    print("Uso del programa: python3 main.py <m3u8_link> <save_dir>")
    sys.exit(1)

m3u8_url = sys.argv[1]
save_dir = sys.argv[2] 

poll_interval = 4

os.makedirs(save_dir, exist_ok=True)

while True:
    try:
        r = requests.get(m3u8_url)
        r.raise_for_status()
        lines = r.text.strip().splitlines()

        # Filtrar líneas que tengan ".ts" en cualquier parte
        ts_chunks = [line for line in lines if ".ts" in line]

        download_all_chunks(m3u8_url, descargados, save_dir)
        time.sleep(poll_interval)

    except Exception as e:
        print("Error:", e)
    time.sleep(poll_interval)

