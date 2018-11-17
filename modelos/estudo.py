from datetime import datetime
from modelos.card import Card

class Estudo:
    tag: str
    card: Card
    data_ultima_repeticao: datetime
    data_proxima_repeticao: datetime
    numero_repeticao: int
    completado: bool
    acerto_ultima_repeticao: bool


    def __init__(self, card: Card, data_repeticao_atual, data_proxima_repeticao, numero_repeticao, completado, acerto_ultima_repeticao):
        self.card = card
        self.data_ultima_repeticao = data_repeticao_atual
        self.data_proxima_repeticao = data_proxima_repeticao
        self.numero_repeticao = numero_repeticao
        self.completado = completado
        self.acerto_ultima_repeticao = acerto_ultima_repeticao
