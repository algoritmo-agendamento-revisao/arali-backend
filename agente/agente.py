from random import randint

import numpy as np
from datetime import timedelta
from datetime import datetime

from utilitario.utilitario_qlearning.utilitarioqlearning import UtilitarioQLearning
from modelos.estudo.estudo import Estudo
from modelos_matematicos.formula_repeticao.formula_repeticao import calcular_oi
from gerenciador.gerenciador_tabela_qlearning.gerenciador_tabela_qlearning import GerenciadorTabelaQLearning


class Agente:


    def __init__(self, fator_desconto, modo_aleatorio, taxa_aprendizagem=None, taxa_exploracao=None, tabelas_q_learning=None):
        # Contrói uma tabela com uma linha a mais por causa da ultima repetição
        self.__qtd_efs__ = 16  # 1.3 - 2.8
        self.__qtd_repeticoes = 15
        self.__utilitario_qlearning__ = UtilitarioQLearning()
        self.__taxa_aprendizagem__ = taxa_aprendizagem
        self.__fator_desconto__ = fator_desconto
        self.__modo_aleatorio__ = modo_aleatorio
        self.__taxa_exploracao__ = taxa_exploracao
        self.__gerenciador_tabela_qlearning__ = GerenciadorTabelaQLearning(self.__qtd_repeticoes, self.__qtd_efs__)
        self.__inicializar_tabelas_qlearning__(tabelas_q_learning)

    def __inicializar_tabelas_qlearning__(self, tabelas_qlearning):
        # Inicializa as tabelas Q Learning caso venha como parâmetro
        if tabelas_qlearning is not None:
            for tag_tabela in tabelas_qlearning:
                tabela_qlearning = tabelas_qlearning[tag_tabela]
                self.__gerenciador_tabela_qlearning__.criar_nova_tabela(tabela_qlearning, tag_tabela)

    def obter_tabelas_q_learing(self):
        return self.__gerenciador_tabela_qlearning__.obter_tabelas_q_learning()

    def tomar_acao(self, recompensa: float, estudo: Estudo):
        if estudo.numero_repeticao is not 1:
            self.__atualizar_politica__(recompensa, estudo)
        estudo.card.ef = randint(13, 28) / 10 if self.__modo_aleatorio__ else self.__calcular_ef_card__(estudo)

        estudo_atualizado = self.__atualizar_info_estudo__(estudo)
        estudo_atualizado.concluido = self.__verificar_estudo_concluido__(estudo_atualizado)
        return estudo_atualizado

    def __atualizar_politica__(self, recompensa: float, estudo: Estudo):
        fator_desconto = self.__fator_desconto__ # y
        taxa_aprendizagem = (1/estudo.numero_repeticao) if self.__taxa_aprendizagem__ is None else self.__taxa_aprendizagem__
        tag = estudo.card.tag

        tabela_qlearning = self.__gerenciador_tabela_qlearning__.obter_tabela_qlearning(tag)

        s = self.__utilitario_qlearning__.mapear_numero_repeticao_em_estado(estudo.numero_repeticao)
        a = self.__utilitario_qlearning__.mapear_ef_em_acao(estudo.card.ef)

        q_atual = tabela_qlearning[s, a]
        q_proxima_acao = tabela_qlearning[s + 1, :]

        tabela_qlearning[s, a] = q_atual + taxa_aprendizagem * (recompensa + (fator_desconto * np.max(q_proxima_acao)) - q_atual)
        self.__gerenciador_tabela_qlearning__.atualizar_tabela_qlearning(tabela_qlearning, tag)


    def __calcular_ef_card__(self, estudo: Estudo):
        if estudo.acerto_ultima_repeticao is False:  # Reseta estudo caso o usuário erre a questão
            return 1.3
        else:
            tag = estudo.card.tag
            tabela_qlearning = self.__gerenciador_tabela_qlearning__.obter_tabela_qlearning(tag)

            s = estudo.numero_repeticao - 1  # Recompensa será atribuída a ação passada
            q_atual = tabela_qlearning[s, :]

            taxa_exploracao = (1 / (s + 1)) if self.__taxa_exploracao__ is None else self.__taxa_exploracao__

            acao = np.argmax(q_atual + np.random.randn(1, self.__qtd_efs__) * taxa_exploracao)
            return self.__utilitario_qlearning__.mapear_acao_em_ef(acao)


    def __atualizar_info_estudo__(self, estudo: Estudo):
        if estudo.acerto_ultima_repeticao is False:  # Caso o usuário tenha errado a pergunta
            estudo.numero_repeticao = 1
            estudo.data_primeira_repeticao = datetime.utcfromtimestamp(0) #datetime.now()
            estudo.data_ultima_repeticao = estudo.data_primeira_repeticao
            # A próxima repetição será agendada para o próximo dia
            estudo.data_proxima_repeticao = estudo.data_ultima_repeticao + timedelta(days=1)

        else:
            ef = estudo.card.ef  # O ef não é alterado, é apenas utilizado para ser passado de parâmetro
            if estudo.numero_repeticao is 1:
                estudo.data_ultima_repeticao = estudo.data_primeira_repeticao
                diferenca_em_dias = self.__calcular_intervalo_em_dias__(ef, estudo.numero_repeticao)
                estudo.data_proxima_repeticao = estudo.data_primeira_repeticao + diferenca_em_dias
            else:
                # Simulando que o tempo passou o tempo e que o card está sendo exibido na data estipulado
                try:
                    estudo.data_ultima_repeticao = estudo.data_proxima_repeticao
                    diferenca_em_dias = self.__calcular_intervalo_em_dias__(ef, estudo.numero_repeticao)
                    estudo.data_proxima_repeticao += diferenca_em_dias
                except Exception:
                    print(f"Algo deu errado com o intervalo : {diferenca_em_dias} + {estudo.data_proxima_repeticao}")

            estudo.__qtd_repeticoes__ += 1
            estudo.numero_repeticao += 1

        return estudo

    def __verificar_estudo_concluido__(self, estudo: Estudo):
        finalizou_por_repeticao = estudo.numero_repeticao >= 15
        finalizou_por_intervalo = (estudo.data_proxima_repeticao - estudo.data_ultima_repeticao).days >= 730
        return finalizou_por_repeticao or finalizou_por_intervalo

    def __calcular_intervalo_em_dias__(self, ef: float, repeticao: int):
        if repeticao is 1:
            return calcular_oi(ef, repeticao)
        else:
            return calcular_oi(ef, repeticao) - calcular_oi(ef, repeticao - 1)
