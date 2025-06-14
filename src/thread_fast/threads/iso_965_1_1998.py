"""Equations from ISO-965-1:1998

ISO general purpose metric screw threads —

Tolerances —

Part 1: Principles and basic data


Symbols:
-d: basic major diameter of external thread
-d_2: basic pitch diameter of external thread
-d_3: minor diameter of external thread
-D: basic major diameter of internal thread
-D_1: basic minor diameter of internal thread
-D_2: basic pitch diameter of internal thread
-T_d: tolerance for d
-T_d2: tolerance for d2
-T_D2: tolerance for D2
-es: upper deviation
-ES: upper deviation
-ei: lower deviation
-EI: lower deviation
-R: root radius of external thread
-C: root truncation of external thread

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
    """
    
    """
    C_max = H/4.0 - R_min * (1.0 - np.cos(np.pi/3.0 - np.arccos(1.0 - T_d2 / (4.0*R_min)))) + T_d2 / 2.0
    return C_max


def eq_C_min(P: float) -> float:
    """
    
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



###################################
# 13.2: Length of thread engagement, pg 16
###################################


###################################
# 13.3: Crest diameter tolerances, pg 17
###################################



###################################
# 13.4: Pitch diameter tolerances, pg 17
###################################



def main() -> None:
    pass
    

if __name__ == "__main__":
    main()
    