"""
Equations from NSTS 08307 Rev A

Criteria for Preloaded Bolts
"""
import numpy as np


########################################################
# 3.0 Required Criteria for Preloaded Bolts: pg 3-1
########################################################

# Basic Requirements:
# adequate strength (at max preload & max external load)
# no joint separation (at min preload & max external load)
# fracture & fatigue life

# need to estimate max and min preloads...
# no factor of safety put on preload (use min & max estimated)
# safety factors applied to external loads

########################################################
# 3.2 Definitions: pg 3-1
########################################################


########################################################
# 3.2.2 Definition of Symbols: pg 3-2
########################################################

# a. External/Internal Loads:

# P = External axial load applied to joint at bolt location due to application of limit load to the structure
# Pb = Bolt axial load resulting from yield, ultimate or joint separation load
# V = Bolt shear load resulting from limit load
# M = Bolt bending moment resulting from limit load

# b. Factors of Safety:
# SF = Bolt strength factor of safety
# SFsep = Joint separation factor of safety

# c. Allowables/Strengths:
# PAt = Axial load allowable of bolt due to tension
# PAs = Axial load allowable of bolt or nut due to thread shear
# VA = Shear load allowable of bolt
# MA = Bending load allowable of bolt


########################################################
# 3.3 Calculation of Max and Min Preloads: pg 3-5
########################################################

# PLD_max = 

# PLD_min = 

# PLD_max = 

# PLD_min = 


# PLD_max = 

# PLD_min = 

# PLD_max = 

# PLD_min = 


########################################################
# 3.4 Typical Preload Uncertainties: pg 3-6
########################################################




########################################################
# 3.5 Typical Coefficients of Friction / Nut Factor: pg 3-7
########################################################




########################################################
# 3.6 Expected Preload Loss: pg 3-8
########################################################

# P_loss = 0.05 * PLD_max



########################################################
# 3.7 Preloaded Bolt Strength Criteria: pg 3-8
########################################################




########################################################
# 3.8 Plastic Bending: pg 3-10
########################################################




########################################################
# 3.9 Preloaded Bolt Separation Criteria: pg 3-11
########################################################




########################################################
# 3.10 Preloaded Bolt Fatigue & Fracture Criteria: pg 3-12
########################################################




########################################################
# 3.11 Re-Torquing of Preloaded Bolts: pg 3-12
########################################################



########################################################
# Appendix A: Bolt Axial Load Allowables: pg A-3
########################################################

########################################################
# 1.0 Axial Load Allowable Due to Tension: pg A-4
########################################################

# If a minimum ultimate tensile load is given for a bolt, the axial load allowables are calculated as follows:

# yield:
PA_t = (F_ty / F_tu) * minimum_ultimate_tensile_load

# ultimate:
PA_t = minimum_ultimate_tensile_load

# If a minimum ultimate tensile load is not given for a bolt, the axial load allowables must be determined from testing or calculated using the following equations:

# yield:
PA_t = A_t * F_ty

# ultimate:
PA_t = A_t * F_tu




########################################################
# 2.0 Axial Load Allowable Due to Thread Shear: pg A-4
########################################################

# The axial load allowable due to thread shear is the smaller of the external thread shear load allowable (Pse) and the internal thread shear load allowable (Psi). These two allowables are calculated as follows:

# external thread shear load allowable:
P_se = A_se * F_su_bolt

# internal thread shear load allowable:
P_si = A_si * F_su_nut


# The two thread shear areas are calculated using the following equations:


# external thread shear area:
A_se = np.pi * L_e * K_i_max * (0.750 - 0.57735 * n_0 * (T*K_i + T*E_e + G_e))


# internal thread shear area:
A_si = np.pi * L_e * D_e_min * (0.875 - 0.57735 * n_0 * (T*D_e + T*E_i + G_e))

# The equations for the tensile stress area and the thread shear areas were taken from FED-STD-H28, Screw Thread Standards for Federal Services, issued by the United States Department of Commerce, National Bureau of Standards.
