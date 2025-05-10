"""Fastener Analysis based on NASA 5020
Timothy P Woodard
May 16, 2021
"""
import numpy as np


# Fitting Factor:
FF = 1.15


# Preload Variation:
# preload changes via: creep, relaxation, temperature

# factor that accounts for range of controlled installation parameter:
cmax = 1.05

# preload variation due to preloading method:
gamma = 0.35

# nominal target preload:
pi_nom = 1.0

# preload loss due to relaxation (embedment of imperfect surfaces):
Ppr = 0.0

# preload loss due to creep:
Ppc = 0.0

# preload gain due to temperature affects:
Pdt_max = 0.0

# preload loss due to temperature affects:
Pdt_min = 0.0

# max initial preload due to preloading method:
Ppi_max = cmax * (1.0 + gamma) * pi_nom

# min initial preload due to preloading method :
Ppi_min = cmax * (1.0 - gamma) * pi_nom
Pp_max = Ppi_max + Pdt_max
Pp_min = Ppi_min - Ppr - Ppc - Pdt_min


# Ultimate Design Load = Limit Load * Factor of Safety * Fitting Factor


# Margin of Safety (ultimate):
MSu = Ptu_allow / (FF * FSu * PtL) - 1.0

# FF = fitting factor
# FSu = ultimate factor of safety
# PtL = tensile limit load
# Ptu_allow = allowable ultimate load for the fastening system

# ultimate factor of safety:
FSu = 1.5


# Stiffness Factor:

# bolt stiffness:
kb = 1.0

# stiffness of the clamped parts:
kc = 1.0
phi = kb / (kb + kc)


# Margin of Safety (yield)
MSy = Pty_allow / (FF * FSy * PtL) - 1.0
# FF = fitting factor
# FSy = yield factor of safety
# PtL = tensile limit load
# Pty_allow = allowable yield load for the fastening system

# Margin of Safety (separation)
MSsep = Pp_min / (FF * FSsep * PtL) - 1.0
