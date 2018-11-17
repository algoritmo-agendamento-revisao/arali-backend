from pymongo import MongoClient
from bson.binary import Binary
import pickle
import numpy as np


class GerenciadorMongoDB:

    def __init__(self):
        self.__client__ = MongoClient('0.0.0.0:27017')
        self.__db__ = self.__client__.arali
        self.__estado__ = self.__db__.estado

    def atualizar_tabela(self, nova_tabela_qlearning, id_estudante, id_tag):
        try:
            tabela = self.__converter_nparray_to_binary__(nova_tabela_qlearning)
            self.__estado__.find_one_and_update(
                {'id_estudante':id_estudante, 'id_tag':id_tag},
                {'$set': {'tabela_qlearning': tabela}}
            )
        except Exception:
            print("Algo deu errado na atualização")

    def carregar_tabela(self, id_estudante, id_tag):
        try:
            registro = self.__obter_registro__(id_estudante, id_tag)
            if registro is not None:
                tabela_qlearning = self.__converter_binario_to_nparray__(registro['tabela_qlearning'])
                return tabela_qlearning
            else:
                return None
        except Exception:
            print("Algo deu errado no carregamento da tabela")

    def criar_tabela(self, id_estudante, id_tag):
        try:
            tabela_qlearning = np.zeros([36, 16])
            novo_registro = self.__criar_novo_registro__(id_estudante, id_tag, tabela_qlearning)
            self.__estado__.insert_one(novo_registro)
            return tabela_qlearning
        except Exception:
            print("Algo deu errado na criação da tabela")

    def __criar_novo_registro__(self, id_estudante, id_tag, tabela_qlearning):
        tabela_binaria = None
        if tabela_qlearning is not None:
            tabela_binaria = Binary(pickle.dumps(tabela_qlearning, protocol=2), subtype=128)
        return {
            "id_estudante": id_estudante,
            "id_tag": id_tag,
            "tabela_qlearning": tabela_binaria
        }

    def __obter_registro__(self, id_estudante, id_tag):
        return self.__estado__.find_one({"id_estudante": id_estudante, 'id_tag': id_tag})

    def __converter_binario_to_nparray__(self, tabela_qlearning):
        return pickle.loads(tabela_qlearning)

    def __converter_nparray_to_binary__(self, tabela_qlearning):
        return Binary(pickle.dumps(tabela_qlearning, protocol=2), subtype=128)

GerenciadorMongoDB().atualizar_tabela(None, 1, 2)