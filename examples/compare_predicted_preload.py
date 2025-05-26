import numpy as np
import thread_fast
import thread_fast.nsts_08307a as nsts_08307a
import thread_fast.nasa_tm_106943 as nasa_tm_106943
import thread_fast.nasa_std_5020 as nasa_std_5020

# conversion factors:
deg_to_rad = np.pi / 180.0

# nut factor:
K_min = 0.18
K_typ = 0.2
K_max = 0.22

# preload uncertainty factor:
gamma = 0.25

# Basic major diameter of external threads (bolt):
D = 5.0


# specified torque to tighten fastener:
T_nom = 20.0
T_min = 18.0
T_max = 22.0

# prevailing torque due to locking feature:
T_p = 5.0


PLD_min = nsts_08307a.min_preload(
    gamma=gamma, 
    T_min=T_min,  # add or subtract prevailing torque?
    K_typ=K_typ,
    T_p=T_p,
    D=D,
    P_thr_neg=0.0,
    relaxation_ratio=0.05,
)
print(f"PLD_min = {PLD_min}")


PLD_max = nsts_08307a.max_preload(
    gamma=gamma, 
    T_max=T_max,  # add or subtract prevailing torque?
    K_typ=K_typ,
    D=D,
    P_thr_pos=0.0,
)
print(f"PLD_max = {PLD_max}")
