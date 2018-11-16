import numpy as np
from utilitario.utilitario_qlearning.utilitarioqlearning import UtilitarioQLearning
from modelos.estudo import Estudo
from gerenciador.gerenciador_tabela_qlearning.gerenciador_tabela_qlearning import GerenciadorTabelaQLearning

class Agente:
    def __init__(self):
        # Contrói uma tabela com uma linha a mais por causa da ultima repetição
        self.__qtd_efs__ = 16  # 1.3 - 2.8
        self.__qtd_repeticoes = 36  # Número de repetições para que no ef mais baixo dê mais de 2 anos
        self.__utilitario_qlearning__ = UtilitarioQLearning()
        self.__taxa_aprendizagem__ = 0.1
        self.__fator_desconto__ = 0.1
        self.__taxa_exploracao__ = 0.1
        self.__gerenciador_tabela_qlearning__ = GerenciadorTabelaQLearning(self.__qtd_repeticoes, self.__qtd_efs__)

    def tomar_acao(self, recompensa: float, estudo: Estudo):
        if estudo.numero_repeticao is not 1:
            self.__atualizar_politica__(recompensa, estudo)
        novo_ef = self.__calcular_ef_card__(estudo)
        return 2.4

    def __atualizar_politica__(self, recompensa: float, estudo: Estudo):
        fator_desconto = self.__fator_desconto__  # y
        taxa_aprendizagem = self.__taxa_aprendizagem__  # a
        tag = estudo.card.tag

        tabela_qlearning = self.__gerenciador_tabela_qlearning__.obter_tabela_qlearning(tag)

        s = self.__mapear_numero_repeticao_em_estado__(estudo.numero_repeticao)
        a = self.__mapear_ef_em_acao__(estudo.card.ef)

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

            taxa_exploracao = self.__taxa_exploracao__

            acao = np.argmax(q_atual + np.random.randn(1, self.__qtd_efs__) * taxa_exploracao)
            return self.__utilitario_qlearning__.mapear_acao_em_ef(acao)

    def __mapear_numero_repeticao_em_estado__(self, repeticao: int):
        return repeticao - 1

    def __mapear_ef_em_acao__(self, ef):
        # Mapeia ef de 1.3 a 2.8 em 0 até 15
        return int(round((ef - 1.3), 1) * 10)

    def __mapear_acao_em_ef__(self, acao):
        #Mapeia acao de 0 a 15 em ef de 1.3 a 2.8
        return round(acao * 0.1 + 1.3, 1)