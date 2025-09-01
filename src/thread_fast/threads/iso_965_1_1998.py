"""Equations from ISO-965-1:1998

ISO general purpose metric screw threads — Tolerances

Part 1: Principles and basic data

Standards:

- ISO 68 ISO general purpose screw threads - Basic profile
- ISO 262
- ISO 5408

Symbols:

- d: basic major diameter of external thread
- d_2: basic pitch diameter of external thread
- d_3: minor diameter of external thread
- D: basic major diameter of internal thread
- D_1: basic minor diameter of internal thread
- D_2: basic pitch diameter of internal thread
- T_d: tolerance for d
- T_d2: tolerance for d2
- T_D2: tolerance for D2
- es: upper deviation
- ES: upper deviation
- ei: lower deviation
- EI: lower deviation
- R: root radius of external thread
- C: root truncation of external thread

EI + T = ES

es + T = ei ???

"""
import numpy as np


###################################
# Table 1: Fundamental deviations for internal threads and external threads, pg 8
###################################

# TODO: implement table 1


###################################
# Table 2: Lengths of thread engagement, pg 9
###################################

# TODO: implement table 2


###################################
# Table 3: Minor diameter tolerance of internal thread , pg 10
###################################


# TODO: implement table 3



###################################
# 10: Pitch diameter tolerances, pg 11
###################################

###################################
# Table 5: Pitch diameter tolerance of internal thread, pg 12
###################################



###################################
# 11: Root contours, pg 14
###################################


def eq_C_max(H: float, R_min: float, T_d2: float) -> float:
    """Calculate 
    
    ISO 965:1998, pg
    
    Args:
        H (float):
        R_min (float):
        T_d2 (float):
    Returns:
        float:
    """
    C_max = H/4.0 - R_min * (1.0 - np.cos(np.pi/3.0 - np.arccos(1.0 - T_d2 / (4.0*R_min)))) + T_d2 / 2.0
    return C_max


def eq_C_min(P: float) -> float:
    """Calculate
    
    ISO 965:1998, pg 
    
    Args:
        P (float):
    Returns:
        float:
    """
    C_min = 0.125 * P
    return C_min


###################################
# Table 7: Minimum root radii, pg 15
###################################



###################################
# 13: Formulae, pg 16
###################################

###################################
# 13.1: Fundamental deviations, pg 16
###################################

EI_G = (0.015 + 0.011 * P)

EI_H = 0.0

es_e = -(0.050 + 0.011 * P)

es_f = -(0.030 + 0.011 * P)

es_g = -(0.015 + 0.011 * P)

es_h = 0.0

###################################
# 13.2: Length of thread engagement, pg 16
###################################

l_N_min = 2.24 * P * d**0.2

l_N_max = 6.7 * P * d**0.2

###################################
# 13.3: Crest diameter tolerances, pg 17
###################################

T_d_6 = 180.0 * P**(2.0/3.0) - 3.15 / np.sqrt(P)

T_d_4 = 0.63 * T_d_6

T_d_8 = 1.6 * T_d_6

# 13.3.2:

T_D1_6 = 433 * P - 190 * P**1.22

T_D1_6 = 230 * P**0.7

T_D1_4 = 0.63 * T_D1_6

T_D1_5 = 0.8 * T_D1_6

T_D1_7 = 1.25 * T_D1_6

T_D1_8 = 1.6 * T_D1_6

###################################
# 13.4: Pitch diameter tolerances, pg 17
###################################

T_d2_6 = 90 * P**0.4 * d**0.1


T_D2_4 = 0.85 * T_d2_6





def main() -> None:
    # Tests:
    
    # basic major diameter:
    d = 6.0
    
    # thread pitch:
    pitch = 1.0
    
    
    

if __name__ == "__main__":
    main()
    