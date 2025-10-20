import requests
import sys
from session_data import (headers, 
                          cookies)

file = sys.argv[1]


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
