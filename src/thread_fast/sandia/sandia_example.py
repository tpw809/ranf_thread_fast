"""Example problem in Sandia Report SAND2008-0371

Guidelines for Bolted Joint Design and Analysis
Version 1.0, 2008

Kevin Brown
Charles Morrow
Samuel Durbin
Allen Baca

Appendix C: Example Problem, pg 43

Uses example from Shigley:
Mechanical Engineering Design, 7th Ed. 2004
"""
import json
import numpy as np

# [psi], young's modulus:
E_steel = 30.0e6

# [psi], yield strength:
sigma_yield_steel = 100000.0
sigma_yield_cast_iron = 30000.0

# [psi], ultimate strength:
sigma_ultimate_steel = 120000.0
sigma_ultimate_cast_iron = 45000.0

# [in/in/F], coefficient of thermal expansion:
cte_steel = 0.0000096
cte_cast_iron = 0.0000065

# [in^2], nominal tensile area:
A_t = 0.226

# [thread/in], threads per inch:
n_tpi = 11

# [in], min pitch diameter of external threads:
D_p_min = 0.5561

# [in], min major diameter of external threads:
D_major_min = 0.6052

# [in], max minor diameter of internal threads:
D_minor_max = 0.5460

# [in], max pitch diameter of internal threads:
D_p_max = 0.5767


nut_factor = 0.2

# [in-lb], applied torque:
# T = K*d*P
torque = 1800.0

uncertainty = 0.35

preload_loss_percent = 0.05


# [lb], applied external load:
F_axial_lb = 5000.0

# [F], temperatures:
T_ambient_F = 68.0
T_min_F = 40.0
T_max_F = 100.0

# Factors of Safety:
SF_yield = 1.5
SF_ultimate = 2.0
