"""Example Bolted Interface Design"""
import numpy as np

# Interface needs to hold 1000 N in tension
# Interface needs to hold 1000 N in shear

# How many and what size bolts to use?
# What preload in the bolts?

# Assume bolt circle diameter.
# Assume number of bolts.
# Assume bolts equally space around the diameter.
# Run statics to get estimated bolt load.

# What class of bolt?

# Class 4.6: 400 MPa
# Class 8.8: proof: 580 MPa, yield: 640 MPa, ultimate tensile: 800 MPa
# Class 10.9: 1040 MPa
# Class 12.9: 1220 MPa

# keep load below proof load...

# M4 size metric fastener, class 8.8
F_proof_m4 = 5090.0

# M6 size metric fastener, class 8.8
F_proof_m6 = 11600.0

# M8 size metric fastener, class 8.8
F_proof_m8 = 21200.0

# M10 size metric fastener, class 8.8
F_proof_m10 = 33700.0 

# [m], bolt circle diameter:
diamater = 0.5

