"""Nut Factor based on Kubler/Bulten

From: Fastening Technology & Bolted Joint Seminar
Bengt Blendulf
pg 118
"""
import numpy as np


def nut_factor(
        P: float, 
        d_2: float, 
        mu_t: float, 
        mu_b: float, 
        d_w: float, 
        d: float,
    ) -> float:
    """Estimated nut factor.
    
    Args:
        P: thread pitch, mm
        d_2: pitch diameter, mm
        mu_t: friction coefficient, threads
        mu_b: friction coefficient, bearing surface
        d_w: effective diameter, bearing area, mm
        d: nominal thread diameter, mm
    Returns:
        float: estimated nut factor
    """
    K = (0.16*P + 0.58*d_2 * mu_t + 0.5* d_w * mu_b) / (d + P)
    return K


def main() -> None:
    pass
    
    # T = K * d * F_p, Nmm
    # F_p = preload force, N
    # K = 
    # d = 


if __name__ == "__main__":
    main()
    