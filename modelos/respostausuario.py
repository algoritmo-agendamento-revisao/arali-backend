class RespostaUsuario:
    tempo_resposta: int
    acerto: bool

    def __init__(self, tempo_resposta=None, acerto=None):
        self.tempo_resposta = tempo_resposta
        self.acerto = acerto