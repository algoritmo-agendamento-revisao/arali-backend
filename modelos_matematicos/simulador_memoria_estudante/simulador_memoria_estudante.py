import math
import numpy as np

def obter_acerto_modelo_ebbinghaus(intervalo):
    probabilidade_lembrar = (0.9907 * math.pow(intervalo, -0.07 ))
    return np.random.random() < probabilidade_lembrar

def obter_acerto_primeira_repeticao():
    return np.random.random() < 0.5
