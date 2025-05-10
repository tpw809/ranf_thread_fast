"""kappa factor from Bulten

From: Fastening Technology & Bolted Joint Seminar
Bengt Blendulf
pg 149
"""
import numpy as np


def kappa(d_As, P, mu_t, d_2):
    """ratio between effective stress and preload stress
    
    1.155 is a constant for 60 degree thread profile
    
    Args:
        d_As:
        P:
        mu_t:
        d_2:
    """
    k = np.sqrt(1.0 + (12.0/d_As**2)*(P/np.pi + 1.155 * mu_t * d_2))
    return k



def main() -> None:
    pass



if __name__ == "__main__":
    main()
    