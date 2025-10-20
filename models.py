

class Streaming:
    def __init__(self, nombre_campeonato: str, num_tatamis: int,  dia: int, fase: str):
        self.nombre_campeonato = nombre_campeonato
        self.num_tatamis = num_tatamis
        self.dia = dia
        self.fase = fase
        self.websocket = {}
        

