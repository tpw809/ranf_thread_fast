"""Fastener Torque Limits Estimation
# Timothy P Woodard
# June 21, 2021
"""
import numpy as np

# Sy = yield strength of the bolt material:
sy = 1.0

k = 1.0

a = 1.0

d = 1.0

# [in-lb], torque to apply to fastener:
T_basic = 0.8 * k * sy * a * d


# Machinery's Handbook:
# Fi = recommended preload
# Sp = proof strength of the bolt
sp = 1.0

# At = tensile stress area of the bolt:
at = 1.0

Fi = 0.75 * at * sp

# Sp_approx, Approximate Proof Strength:
Sp_approx = 0.85 * sy


# Approximate Change in Length of Bolt due to recommended preload:

# bolt length:
l = 1.0

# bolt area:
A = 1.0

# bolt modulus of elasticity:
E = 200e6
delta = Fi * l / (A * E)


# Estimated Torque to tighten to recommended preload:

# Nut factor:
K = 0.2

# nominal bolt diameter:
d = 0.5

# estimated torque on wrench to tighten to recommended preload:
T = K * Fi * d

# K ranges from 0.117 to 0.553
# want minimum fastener size and number to adequately hold the load...

# Combined tensile stress: stress from preload + stress from torsion:

# axial applied tensile stress:
Ft = 1.0

# shear stress caused by torsion during torquing:
Fs = 0.2

# combined tensile stress:
Ftc = np.sqrt(Ft**2 + 3.0 * Fs**2)
