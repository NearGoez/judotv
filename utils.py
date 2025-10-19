import os 
import subprocess
from pathlib import Path
import requests
import websockets

async def websocket_judotv():
    url = "wss://wsrt.ijf.org/"
    async with websockets.connect(url) as ws:
        print("Conectado")
        async for message in ws:
            print("Mensaje:", message)


def ejecutar_concat_ffmpeg(list_file_path: str, output_file_path: str):
    cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file_path),
        "-c", "copy",
        str(output_file_path)
    ]
    subprocess.run(cmd, check=True)


def create_temporal_fragments_list(absolute_fragments_dir, start: int, end: int):
    

    print(type(start), type(end))
    ts_files = sorted(absolute_fragments_dir.glob("*.ts"),
                      key=lambda f: int(f.stem))
    list_file = absolute_fragments_dir/ ".ts_list.txt"

    if end == -1:
        end = len(ts_files)

    with open(list_file, "w") as f:
        for i in range(start, end):
            f.write(f"file '{ts_files[i].resolve()}'\n")
    return list_file

def concatenar_fragmentos(fragments_dir: str, start: int, end: int):
    base_dir = Path(__file__).resolve().parent
    
    absolute_fragments_dir = base_dir / fragments_dir
    
    list_file = create_temporal_fragments_list(absolute_fragments_dir, start, end)
        
    output_file_path = (base_dir / fragments_dir).parent / "streaming.mp4"
    ejecutar_concat_ffmpeg(list_file, output_file_path)
    


def get_json_ijforg():

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Access-Control-Request-Method': 'GET',
        'Access-Control-Request-Headers': 'authorization',
        'Referer': 'https://judotv.com/',
        'Origin': 'https://judotv.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Priority': 'u=4',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    params = {
        '_j': '{"id_competition":3086,"action":"contest.user_votes"}',
    }

    response = requests.options('https://data.ijf.org/api/get_json', params=params, headers=headers)
    return response

def ping_ijforg():

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'authorization,content-type',
        'Referer': 'https://judotv.com/',
        'Origin': 'https://judotv.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Priority': 'u=4',
    }

    response = requests.options('https://datav2.ijf.org/Playbacks/45534168/Ping', headers=headers)
    
    return response




def get_fragments_json_ijf():
    cookies = {
        'theme.selectedColor': 'light',
        'theme.selectedContrastMode': 'auto',
        'locale': 'en',
        'displayAppPopup': 'true',
        'CookieConsent': '{stamp:%27-1%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27implied%27%2Cver:1%2Cutc:1760217036342%2Cregion:%27CL%27}',
        'AccountLoginTokenV2': 'eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJJZFVzZXIiOjExMjM5MTksIkVtYWlsIjoic2x5dGhpbjA3QGdtYWlsLmNvbSIsIk5hbWUiOiJNYXRpID8iLCJEaXNwbGF5TmFtZSI6bnVsbCwiR2VuZGVyIjpudWxsLCJleHAiOjE3NjE1OTk0NTE0NzMsIkxpa2VzSnVkbyI6ZmFsc2UsIkNhbkdldEZiTGlrZXMiOmZhbHNlLCJDYW5HZXRGYkVtYWlsIjpmYWxzZSwiSWRMb2dpbiI6MTM4MTE0MTIsIkdyb3VwcyI6IiIsIlJvbGVzIjoiIiwiQWN0aXZhdGVkIjp0cnVlLCJFbWFpbFZlcmlmaWVkIjp0cnVlfQ.APuPN3aktKQvrFeaAx5dufivqlGVq2QZlg874tn3Ka2t4fHIBZcnyz49KWNDYaMIENrub4LyKTHSE5pHXQrzOX5GAY-Y0TkENa1wjafg37XlK262XINeQnct_2-ObLgnYTh3rJgiRUj2M13fVpHAOSC9Hs0oZRiQ1Y579mdr0Vz3326H',
        'theme.color': 'light',
        'theme.contrastMode': 'normal',
        'muxData': '=undefined&mux_viewer_id=98420ba8-0901-44dd-9f28-7b11d51e9e4a&msn=0.7863692214794965&sid=4470a22e-4b3f-46db-8113-7d9bda6e3f60&sst=1760306282336&sex=1760310289322',
        'draw.show_scores': 'false',
        'brackets.zoom': '100',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': 'https://judotv.com/competitions/gp_per2025/live',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'If-Modified-Since': 'Sun, 12 Oct 2025 22:38:48 GMT',
        'If-None-Match': 'W/"JKbPOEtxbj"',
        'Priority': 'u=4',
    }

    response = requests.get('https://judotv.com/api/v2/competitions/3086/fragments', cookies=cookies, headers=headers)
    return response

def posible_update():
    cookies = {
        'theme.selectedColor': 'light',
        'theme.selectedContrastMode': 'auto',
        'locale': 'en',
        'displayAppPopup': 'true',
        'CookieConsent': '{stamp:%27-1%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27implied%27%2Cver:1%2Cutc:1760217036342%2Cregion:%27CL%27}',
        'AccountLoginTokenV2': 'eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJJZFVzZXIiOjExMjM5MTksIkVtYWlsIjoic2x5dGhpbjA3QGdtYWlsLmNvbSIsIk5hbWUiOiJNYXRpID8iLCJEaXNwbGF5TmFtZSI6bnVsbCwiR2VuZGVyIjpudWxsLCJleHAiOjE3NjE1OTk0NTE0NzMsIkxpa2VzSnVkbyI6ZmFsc2UsIkNhbkdldEZiTGlrZXMiOmZhbHNlLCJDYW5HZXRGYkVtYWlsIjpmYWxzZSwiSWRMb2dpbiI6MTM4MTE0MTIsIkdyb3VwcyI6IiIsIlJvbGVzIjoiIiwiQWN0aXZhdGVkIjp0cnVlLCJFbWFpbFZlcmlmaWVkIjp0cnVlfQ.APuPN3aktKQvrFeaAx5dufivqlGVq2QZlg874tn3Ka2t4fHIBZcnyz49KWNDYaMIENrub4LyKTHSE5pHXQrzOX5GAY-Y0TkENa1wjafg37XlK262XINeQnct_2-ObLgnYTh3rJgiRUj2M13fVpHAOSC9Hs0oZRiQ1Y579mdr0Vz3326H',
        'theme.color': 'light',
        'theme.contrastMode': 'normal',
        'muxData': '=undefined&mux_viewer_id=98420ba8-0901-44dd-9f28-7b11d51e9e4a&msn=0.7863692214794965&sid=4470a22e-4b3f-46db-8113-7d9bda6e3f60&sst=1760306282336&sex=1760311817625',
        'draw.show_scores': 'false',
        'brackets.zoom': '100',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Connection': 'keep-alive',
        'Referer': 'https://judotv.com/competitions/gp_per2025/live',
        # 'Cookie': 'theme.selectedColor=light; theme.selectedContrastMode=auto; locale=en; displayAppPopup=true; CookieConsent={stamp:%27-1%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27implied%27%2Cver:1%2Cutc:1760217036342%2Cregion:%27CL%27}; AccountLoginTokenV2=eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJJZFVzZXIiOjExMjM5MTksIkVtYWlsIjoic2x5dGhpbjA3QGdtYWlsLmNvbSIsIk5hbWUiOiJNYXRpID8iLCJEaXNwbGF5TmFtZSI6bnVsbCwiR2VuZGVyIjpudWxsLCJleHAiOjE3NjE1OTk0NTE0NzMsIkxpa2VzSnVkbyI6ZmFsc2UsIkNhbkdldEZiTGlrZXMiOmZhbHNlLCJDYW5HZXRGYkVtYWlsIjpmYWxzZSwiSWRMb2dpbiI6MTM4MTE0MTIsIkdyb3VwcyI6IiIsIlJvbGVzIjoiIiwiQWN0aXZhdGVkIjp0cnVlLCJFbWFpbFZlcmlmaWVkIjp0cnVlfQ.APuPN3aktKQvrFeaAx5dufivqlGVq2QZlg874tn3Ka2t4fHIBZcnyz49KWNDYaMIENrub4LyKTHSE5pHXQrzOX5GAY-Y0TkENa1wjafg37XlK262XINeQnct_2-ObLgnYTh3rJgiRUj2M13fVpHAOSC9Hs0oZRiQ1Y579mdr0Vz3326H; theme.color=light; theme.contrastMode=normal; muxData==undefined&mux_viewer_id=98420ba8-0901-44dd-9f28-7b11d51e9e4a&msn=0.7863692214794965&sid=4470a22e-4b3f-46db-8113-7d9bda6e3f60&sst=1760306282336&sex=1760311817625; draw.show_scores=false; brackets.zoom=100',
        'Sec-Fetch-Dest': 'script',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'If-None-Match': 'W/"a071605efcda6af25b43cf329a0a7007"',
        'Priority': 'u=1',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    response = requests.get('https://judotv.com/judo_tv/DFS9jmYK.js', cookies=cookies, headers=headers)
    return response



def create_fetch():

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'authorization,content-type,user-agent',
        'Referer': 'https://judotv.com/',
        'Origin': 'https://judotv.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Priority': 'u=4',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    response = requests.options('https://datav2.ijf.org/Playbacks/Create', headers=headers)

