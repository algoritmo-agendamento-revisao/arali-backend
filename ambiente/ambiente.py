from agente.agente import Agente
from modelos.card import Card
from modelos.estudo import Estudo
from modelos.respostausuario import RespostaUsuario
from datetime import datetime
from datetime import timedelta
from modelos_matematicos.formula_repeticao.formula_repeticao import calcular_oi

class Ambiente:

    __agente__: Agente

    def __init__(self):
        self.__agente__ = Agente()

    def obter_proxima_repeticao(self, api_object):
        resposta_usuario = RespostaUsuario(
            api_object['timeForResolution'],
            api_object['isRight']
        )
        estudo_corrente = Estudo(
            Card(
                api_object['card']['id'],
                api_object['card']['difficulty'])
            ,
            api_object['currentDate'],
            api_object['lastRepetition'],
            api_object['numberOfRepetition'],
            False,
            api_object['isRight']
        )
        recompensa = self.__calcular_recompensa__(resposta_usuario, estudo_corrente)

        novo_ef = self.__agente__.tomar_acao(recompensa, estudo_corrente)
        proxima_repeticao = self.__calcular_proxima_repeticao__(estudo_corrente)
        estudo_completado = self.__verificar_estudo_completado__(estudo_corrente.data_ultima_repeticao, proxima_repeticao)

        return {
            "card": {
                "id": estudo_corrente.card.id,
                "difficulty": novo_ef,
            },
            "completed": estudo_completado,
            "nextRepetition": proxima_repeticao
        }

    def __calcular_recompensa__(self, resposta: RespostaUsuario, estudo_corrente: Estudo):
        if resposta.acerto is False:
            return -1
        else:
            intervalo = (estudo_corrente.data_proxima_repeticao - estudo_corrente.data_ultima_repeticao).days
            repeticao = estudo_corrente.numero_repeticao
            tempo_resposta = resposta.tempo_resposta
            recompensa = round((intervalo * (repeticao / tempo_resposta)), 5)
            return recompensa

    def __calcular_proxima_repeticao__(self, estudo: Estudo):
        if estudo.acerto_ultima_repeticao is False:  # Caso o usuário tenha errado a pergunta
            # A próxima repetição será agendada para o próximo dia
            return estudo.datetime.now() + timedelta(days=1)
        else:  # Caso o usuário tenha acertado
            ef = estudo.card.ef  # O ef não é alterado, é apenas utilizado para ser passado de parâmetro
            # A próxima repetição será agendada conforme a diferença entre os intervalos das repetições R e R-1
            diferenca_em_dias = self.__calcular_intervalo_em_dias__(ef, estudo.numero_repeticao)
            return datetime.now() + diferenca_em_dias

    def __calcular_intervalo_em_dias__(self, ef: float, repeticao: int):
        if repeticao is 1:
            return calcular_oi(ef, repeticao)
        else:
            return calcular_oi(ef, repeticao) - calcular_oi(ef, repeticao - 1)

    def __verificar_estudo_completado__(self, ultima_repeticao, proxima_repeticao):
        return (proxima_repeticao - ultima_repeticao).days >= 730

    def __montar_resposta__(self, novo_ef, data_proxima_repeticao, estudo_foi_completado):
        return {
            "card":{
                "difficulty": novo_ef
            },
            "nextRepetition": data_proxima_repeticao,
            "completed": estudo_foi_completado
        }