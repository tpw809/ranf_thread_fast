"""Separation Margin

Parameter Tracing:
-start with what you want to evaluate
-keep finding required parameters
-add those above / before the equations that needs it
-keep going until all parameters are defined
-once complete, collect all of the direct assignments as inputs
"""
import numpy as np

# conversion factors:
deg_to_rad = np.pi / 180.0
psi_to_MPa = 0.00689476

# assumptions and inputs:
# P_et : from application conditions
# SF_sep: from design requirements
# type of joint: config 1,2,3,4
# E_b: from material properties
# D: from fastener geometry
# D_p: from fastener geometry
# D_minor: fastener geometry
# D_major: fastener geometry
# preload application method
# L: joint geometry
# use of washers
# mu: friction assumption
# mu_c: friction assumption
# pitch: coarse or fine thread
# preload_stress_ratio: target preload stress / strength ratio
# relaxation_ratio: relaxation percent
# F_ty: material properties
# alpha: thread geometry / standard
# alpha_b: material properties
# alpha_j: material properties
# Temperatures
# loading plane location
# E_1: material properties


# assume config 1: through bolt with nut
# assume bolt material: A286 stainless steel
# assume hand torqueing
# assume M5 socket head bolt, coarse thread
# assumed 2x 10mm thick aluminum plates
# assume 0.65 stress / strength preload ratio
# assume 5% preload relaxation
# assume loading at midplane of the clamped parts



relaxation_ratio = 0.05
preload_stress_ratio = 0.65

# [-], safety factor for separation for structural applications:
SF_sep = 1.2
print(f"SF_sep = {SF_sep}")

# [C], Temperatures:
T_amb = 20.0
T_max = 80.0
T_min = -20.0

# [mm], nominal fastener diameter:
D = 5.0

# [mm], fastener major (outer) diameter:
D_major = 4.976

# [mm], fastener minor diameter:
D_minor = 4.134

# [mm], screw pitch: for M5 coarse thread
pitch = 0.8
print(f"pitch = {pitch}")

# [-], coefficient of friction between threads:
mu = 0.15
print(f"mu = {mu}")

# [-], coefficient of friction between bolt or nut head and abutment:
mu_c = 0.15
print(f"mu_c = {mu_c}")

# [rad], thread angle:
alpha = 60.0 * deg_to_rad
print(f"alpha = {alpha} [rad]")

# length of clamped joint:
L = 2.0 * 10.0
print(f"L = {L}")

# [MPa], bolt modulus of elasticity:
E_b = 200.0e3
print(f"E_b = {E_b} [MPa]")

# [MPa], tensile yield strength:
F_ty = 85000.0 * psi_to_MPa
print(f"F_ty = {F_ty} [MPa]")

# [1/C], bolt coefficient of thermal expansion:
alpha_b = 16.9e-6
print(f"alpha_b = {alpha_b} [1/C]")

# [1/C], joint coefficient of thermal expansion:
alpha_j = 23.1e-6
print(f"alpha_j = {alpha_j} [1/C]")

# [N], total externally applied axial load:
P_et = 100.0
print(f"P_et = {P_et} [N]")

# preload uncertainty factor: for hand torquing
u = 0.25
print(f"u = {u}")

# loading plane goemetry assumptions:
# [mm], length to loading plane of first clamped part:
l_1 = 5.0

# [mm], distance between loading plane of loaded clamped parts:
l_2 = 10.0

# [mm], distance between loading plane of last loaded clamped part:
l_n = 5.0

# [MPa], modulus of clamped part:
E_1 = 72.0e3

# [MPa], modulus of clamped part:
E_2 = 72.0e3

# [MPa], modulus of clamped part:
E_n = 72.0e3


# [mm], mean thread (pitch?) diameter:
D_p = (D_major + D_minor) / 2.0
print(f"D_p = {D_p} [mm]")

# [mm], mean radius of the screw thread:
r_m = D_p / 2.0
print(f"r_m = {r_m} [mm]")

# [mm^2], tensile area: eq 4
A_t = (np.pi / 4.0) * (D - 0.9743 * pitch)**2
print(f"A_t = {A_t} [m^2]")

# [rad], thread helix angle (lead angle?):
# psi = np.arctan(2.0 * np.pi * r_m / pitch)
# TODO: helix angle actually the lead angle???
psi = np.arctan(pitch / (2.0 * np.pi * r_m))
print(f"psi = {psi} [rad]")
print(f"psi = {psi / deg_to_rad} [deg]")

# [mm^2], nominal fastener cross sectional area:
A = np.pi * (D / 2.0)**2
print(f"A = {A} [m^2]")

# loading plane factor:
# for loading at mid-planes:
n = 0.5
# eq 35 (due to type assumption):
n = (l_1 / 2.0 + l_2 + l_n / 2.0) / L
# TODO: see blendulf pg 142...
# TODO: see NASA-TM-108377
print(f"n = {n}")

# bolt stiffness: eq 32  (due to type assumption)
# TODO: expand this based on blendulf pg 134...
# include different lengths and cross sections...
K_b = A * E_b / L
print(f"Bolt Stiffness: K_b = {K_b} [N/mm]")

# composite joint modulus: eq 34
E_j = L / ((l_1 / E_1) + (l_2 / E_2) + (l_n / E_n))
print(f"E_j = {E_j}")

# joint stiffness: eq 33 (due to type assumption)
K_j = np.pi * E_j * D / (2.0 * np.log(5.0 * ((L + 0.5*D)/(L + 2.5*D))))
# TODO: alternative based on blendulf, pg 136-137
# based on equivalent joint diameter, D_j
print(f"Joint Stiffness: K_j = {K_j} [N/mm]")

# joint stiffness factor: eq 29
phi = K_b / (K_b + K_j)
print(f"phi = {phi}")

# [C], change in temperature:
delta_T_min = T_min - T_amb 
delta_T_max = T_max - T_amb
print(f"delta_T_min = {delta_T_min} [C]")
print(f"delta_T_max = {delta_T_max} [C]")

# axial bolt load due to thermal effects: eq 10
P_th_min = ((K_b * K_j) / (K_b + K_j)) * L * delta_T_min * (alpha_j - alpha_b)
P_th_max = ((K_b * K_j) / (K_b + K_j)) * L * delta_T_max * (alpha_j - alpha_b)
print(f"P_th_min = {P_th_min} [N]")
print(f"P_th_max = {P_th_max} [N]")
P_th = np.min([P_th_min, P_th_max])
print(f"P_th = {P_th} [N]")

# may need an if statement for P_th...
# depends on which temperature delta reduces preload...

# nut factor: eq 2
# K = D_p / (2.0 * D) * ((np.tan(psi) + mu * np.sec(alpha)) / (1.0 - mu * np.tan(psi) * np.sec(alpha))) + 0.625 * mu_c
# sec = 1/cos
K = D_p / (2.0 * D) * ((np.tan(psi) + mu / np.cos(alpha)) / (1.0 - mu * np.tan(psi) / np.cos(alpha))) + 0.625 * mu_c
K = 0.15
# print(f"np.tan(psi) = {np.tan(psi)}")
# print(f"np.cos(alpha) = {np.cos(alpha)}")
print(f"Nut Factor: K = {K}")

# applied torque: target 0.65 tensile yield stress / strength, eq 3
T = preload_stress_ratio * F_ty * A_t * K * D
print(f"Tightening Torque: T = {T:.3f} [N-mm]")
print(f"Tightening Torque: T = {T / 1000.0:.3f} [N-m]")

# [N], minimum expected bolt preload, eq 13 (re-arranged)
# P_0_min = (T / (K * D)) * (1.0 - u) - P_th - P_relax
P_0_min = ((T / (K * D)) * (1.0 - u) - np.abs(P_th)) / (1.0 + relaxation_ratio)
print(f"Min Preload: P_0_min = {P_0_min} [N]")

# axial bolt preload loss due to embedment / settling:
P_relax = relaxation_ratio * P_0_min
print(f"P_relax = {P_relax} [N]")

# [N], separation load: eq 67
P_sep = (1.0 - n * phi) * P_et
print(f"P_sep = {P_sep} [N]")

# use eq67 in nasa_tm_106943.py:


# [-], margin of safety against separation: eq68
MS_sep = (P_0_min / (SF_sep * P_sep)) - 1.0
print(f"MS_sep = {MS_sep}")

# use eq68 in nasa_tm_106943.py: