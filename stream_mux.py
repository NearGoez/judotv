import requests
import sys
from session_data import (headers, 
                          cookies)
from m3u8 import get_highest_res_manifest_from_text

file = sys.argv[1]


def stream_mux_consult(stream_mux_url: str ) -> str:
    response  = requests.get(stream_mux_url).text

    highest_res_manifest_url = get_highest_res_manifest_from_text(response)

    return highest_res_manifest_url


if __name__ == "__main__":
    params = {
        'token': cookies['AccountLoginTokenV2'],
    }

    response = requests.get(
        f'https://stream.mux.com/{file}.m3u8',
        params=params,
        headers=headers,
        cookies=cookies,
    )

    print(response.text)
