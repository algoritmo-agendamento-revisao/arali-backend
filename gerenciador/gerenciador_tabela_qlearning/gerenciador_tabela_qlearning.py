import copy
from collections import defaultdict
import numpy as np

class GerenciadorTabelaQLearning:

    __tabelas_qlearning__ = defaultdict(list)
    __qtd_estados__: int
    __qtd_acoes__ : int

    def __init__(self, qtd_estados, qtd_acoes):
        self.__tabelas_qlearning__.clear()
        self.__qtd_estados__ = qtd_estados
        self.__qtd_acoes__ = qtd_acoes

    def __criar_nova_tabela_vazia__(self, tag: str):

        self.__tabelas_qlearning__[tag] = nova_tabela

    def criar_nova_tabela(self, tabela_qlearning, tag):
        self.__tabelas_qlearning__[tag] = copy.deepcopy(tabela_qlearning)

    def obter_tabela_qlearning(self, tag):
        if tag not in self.__tabelas_qlearning__.keys():
            self.__criar_nova_tabela_vazia__(tag)
        return self.__tabelas_qlearning__[tag]

    def obter_tabelas_q_learning(self):
        return self.__tabelas_qlearning__

    def atualizar_tabela_qlearning(self,tabela_qlearning_atualizada, tag):
        self.__tabelas_qlearning__[tag] = copy.deepcopy(tabela_qlearning_atualizada)

    def verificar_existencia_tabela(self, tag):
        return tag in self.__tabelas_qlearning__.keys()

