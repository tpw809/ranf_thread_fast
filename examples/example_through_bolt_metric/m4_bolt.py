"""M4 Bolt Information

Geometry based on FED-STD-H28-21B for 1.6mm and larger

M= metric
MJ = metric with rounded root

ANSI/ASME B1.13M-1983/1995/2001 Metric Screw Threads: M Profile
ANSI B1.21M-l978 - MetricScrewThreads- MJ Profile
ANSI B46.1 - Surface Texture- SurfaceRoughness, Waviness and
Lay

ISO 68-1 General Purpose Screw Threads - Basic Profile
ISO 965-1 General Purpose Metric Screw Threads - Tolerances

Reference Temperature = 20 C
"""
import numpy as np

# M4x0.7-4g6g EXT

# thread angle = 60 degrees
# half thread angle = 30 degrees
# 45 degree chamfers

# [mm/thread], thread pitch:
pitch = 0.7

# [mm], fundamental triangle height:
H = np.sqrt(3.0) / 2.0 * pitch

# ASME B1.13M-2001, table 13, pg 21:
# upper deviation, external thread (fundamental deviation)
# based on specified tolerance position (e,f,g,h)
es_e = 0.056
es_f = 0.038
es_g = 0.022
es_h = 0.0

# [mm], major (outer) diameter:
d_major_basic = 4.0
d_major_max = d_major_basic - es_h
d_major_min = 

# [mm], minor diameter:
d_minor = 3.242
d_minor_basic = d_major_basic - H * (5.0/8.0)

# [mm], pitch diameter:
d_pitch = 3.545
d_pitch_basic = d_major_basic - 0.5 * H

# [mm], minimum root radius for rounded root threads:
r_min = 0.125 * pitch

# ASME B1.13M-2001, section 6.4, pg 16:
# normal length of thread engagement:
LE_min = 2.24 * pitch * d_major_basic**0.2
LE_max = 6.7 * pitch * d_major_basic**0.2


# max major diameter
# min major diameter
# max pitch diameter
# min pitch diameter
# max minor diameter (flat form)
# min minor diameter (flat form)
# max minor diameter (rounded form)
# min minor diameter (rounded form)

# thread on a part is either external (bolt) or internal (tapped, nut, insert)


# From ASME B1.13M-2001: Table 1 General Symbols:

# D = major diameter internal thread
# D_1 = minor diameter internal thread
# D_2 = pitch diameter internal thread
# d = major diameter external thread
# d_1 = minor diameter external thread
# d_2 = pitch diameter external thread
# d_3 = rounded form minor diameter external thread
# P = pitch
# r = external thread root radius
# T = tolerance
# TD_1,TD_2 = tolerances for D_1, D_2
# Td, Td_2 = tolerances for d, d_2
# ES = upper deviation, internal thread (fundamental deviation plus tolerance)
# EI = lower deviation, internal thread (fundamental deviation)
# G, H = letter designations for tolerance positions for upper deviation, internal thread
# g, h = letter designations for tolerance positions for upper deviation, external thread
# es = upper deviation, external thread (fundamental deviation)
# ei = lower deviation, external thread (fundamental deviation plus tolerance)
# H = height of fundamental triangle
# LE = length of engagement
# LH = left hand thread

# bsc = basic
# max = maximum
# min = minimum

# H = np.sqrt(3.0) / 2.0 * P
# H = 0.866025 * P
print(f"H = {np.sqrt(3.0) / 2.0} * P")
print(f"H = {0.866025} * P")

# 1/8 = 0.125
# 1/4 = 0.250
# 3/8 = 0.375
# 5/8 = 0.625

# thread basic thickness at pitch diameter = P/2
# basic internal thread is the inverse of the external thread
# real external thread has smaller root to allow a small radius
# metric tolerances eliminate possibility of interferance by  shifting from basic profile
