"""Strength Margin

Parameter Tracing:
-start with what you want to evaluate
-keep finding required parameters
-add those above / before the equations that needs it
-keep going until all parameters are defined
-once complete, collect all of the direct assignments as inputs
"""
import numpy as np
import thread_fast

# conversion factors:
deg_to_rad = np.pi / 180.0
psi_to_MPa = 0.00689476

# assumptions and inputs:
# FF: fitting factor for loading / stiffness assumptions
# preload_stress_ratio: target preload stress / strength ratio
# relaxation_ratio: relaxation percent
# SF_u: ultimate factor of safety, from design requirements
# SF_y: yield factor of safety, from design requirements
# axial load
# P_sL: shear load
# bending load
# F_su: allowable ultimate shear strength for material
# D: from fastener geometry


relaxation_ratio = 0.05
preload_stress_ratio = 0.65

# fitting factor: requirement TFSR3 in NASA-STD-5020B
fitting_factor = 1.15

# [-], ultimate safety factor: requirement TFSR2 in NASA-STD-5020B
SF_u = 1.4
print(f"SF_u = {SF_u}")

# [-], yield safety factor: requirement TFSR2 in NASA-STD-5020B
SF_y = 1.1
print(f"SF_y = {SF_y}")



# [mm], nominal fastener diameter:
D = 5.0

# [mm], screw pitch: for M5 coarse thread
pitch = 0.8
print(f"pitch = {pitch}")

# Loads:

# [N], limit shear load acting on the shear plane:
P_sL = 100.0


# allowable ultimate tensile strength for the fastener material:
F_tu = 120000.0 * psi_to_MPa
print(f"F_tu = {F_tu} [MPa]")

# allowable ultimate shear strength for the fastener material:
# ratio of 0.577 to tensile strength (von Mises criterion)
F_su = 0.577 * F_tu
print(f"F_su = {F_su} [MPa]")

# [mm^2], minimum minor diameter area for the fastener threads:
# NSTS 08307A, bolt_tensile_stress_area

# TODO: this might not be the right area... need shear area...
A_m = thread_fast.nsts_08307a.bolt_tensile_stress_area(
    D_e_bsc=D, 
    n_0=None,
    pitch=pitch,
)
print(f"A_m = {A_m}")


# [N], allowable ultimate shear load:
# NASA-STD-5020B eq 12 & 13

# NASA-STD-5020B eq 12:
P_su_allow = np.pi * D**2 * F_su / 4.0
print(f"P_su_allow = {P_su_allow}")

# NASA-STD-5020B eq 13:
P_su_allow = F_su * A_m
print(f"P_su_allow = {P_su_allow}")



# Margin of Safety:

# ultimate, axial load only:
# NASA-STD-5020B eq 6 & 7


# ultimate, shear loading only:
# NASA-STD-5020B eq 14
# compare to: NASA-TM-106943, equation 54, pg 16
MS_u_shear = P_su_allow / (fitting_factor * SF_u * P_sL) - 1.0
print(f"MS_u_shear = {MS_u_shear}")

MS_u_shear = thread_fast.nasa_std_5020b.eq14(
    P_su_allow=P_su_allow,
    FS_u=SF_u,
    P_sL=P_sL,
    FF=fitting_factor,
)
print(f"MS_u_shear = {MS_u_shear}")

# yield, axial load only:
# NASA-STD-5020B eq 15 & 16

# no shear yield margin: combined components of normal and shear into principal stresses and use failure theory such as von-mises

# combined loads:
# NASA-STD-5020B eq 20 & 21, 22, 23

