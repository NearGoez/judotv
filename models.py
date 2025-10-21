import asyncio
from queue import Queue
import websockets
from dataclasses import dataclass
from collections import dequeu
from utils import (websocket_judotv, websocket_json_parser)
from constants import (wss_url)


@dataclass
class Round:
    id_round: int
    white_name: str
    white_nacionality: str
    blue_name: str
    blue_nacionality: str
    round_name: str


class Mat:
    def __init__(self, championship_name: str, n_mat: int):
        self.championship_name = championship_name
        self.n_mat = n_mat


        self.current_round = None
        self.wss_messages_queue = Queue(maxsize=1)


    def terminate_current_round(self):
        pass   

class Championship:
    def __init__(self, championship_name: str,   
                 day: int, phase: str, date: str):

        self.championship_name = championship_name
        self.day = day
        self.fase = phase
        self.date = date

        self.number_of_mats = 0
        self.mats = []

        self.websocket = {}


    async def websocket_judotv(self):
        url = "wss://wsrt.ijf.org/"
        async with websockets.connect(url) as ws:
            print("Conectado")
            async for message in ws:
                # Sending each wss message's part to the right Mat


                print("Mensaje:", websocket_json_parser(message))

    def consult_number_of_mats(self):
        #TODO -> Implement the mats' counting by consulting the judotv API
        pass   


        

