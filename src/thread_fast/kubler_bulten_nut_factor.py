"""Nut Factor based on Kubler/Bulten

From: Fastening Technology & Bolted Joint Seminar
Bengt Blendulf
pg 118
"""
import numpy as np


def kubler_bulten_nut_factor(
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
        mu_t: friction coefficient between threads
        mu_b: friction coefficient between bolt head or nut and abutment bearing surface
        d_w: effective diameter, bearing area, mm
        d: nominal thread diameter, mm
    Returns:
        float: estimated nut factor
    """
    K = (0.16*P + 0.58*d_2 * mu_t + 0.5* d_w * mu_b) / (d + P)
    return K


def main() -> None:
    
    # T = K * d * F_p, torque, Nmm
    # F_p = preload force, N
    # K = nut factor
    # d = diameter, mm
    
    # M5 bolt example:
    
    mu_t = 0.15
    mu_b = 0.15
    d = 5.0
    pitch = 0.8
    d_2 = 4.48
    d_w = (8.75 + 5.0) / 2.0
    
    K = kubler_bulten_nut_factor(
        P=pitch, 
        d_2=d_2,
        mu_t=mu_t, 
        mu_b=mu_b,
        d_w=d_w,
        d=d,
    )
    print(f"K = {K}")


if __name__ == "__main__":
    main()
    