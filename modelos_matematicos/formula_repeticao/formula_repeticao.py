from datetime import timedelta
import numpy as np

def calcular_oi(ef, repeticao):
    try:
        if repeticao is 1:
            return timedelta(days=5)

        part1 = calcular_oi(ef, repeticao - 1)
        part2 = ef - 0.1 + np.power(np.e, (-2.3 * repeticao + 5))
        oi = part1 * part2
        return timedelta(days=oi.days)
    except Exception:
        # Quando o intervalo é muito grande
        raise Exception
