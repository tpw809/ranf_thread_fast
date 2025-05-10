"""Example Bolted Joint Analysis
Timothy P Woodard
June 26, 2021
"""
import numpy as np
from metric_fastener_class import M5MetricFastener
from metric_fastener_class import M10MetricFastener

# Bolted Joint description:
# M5 socket head cap screw
# bolt material = 18-8 stainless steel
# clamped material = aluminum
# secured with nut
# washers between nut and bolt head
# installed using torque wrench

M5bolt = M5MetricFastener()

# [-], estimated coefficient of friction between threads:
mu_s = 0.14

# [-], estimated coefficient of friction between nut face and washer:
mu_w = 0.14

# estimated k (nut factor):
kest = M5bolt.estimated_k(
    mus=mu_s, 
    muw=mu_w,
)
print("estimated nut factor, k = ", kest)

Athread = M5bolt.thread_tensile_stress_area
print("Tensile area of threaded portion of bolt = ", Athread, ' mm^2')
Athread = M5bolt.thread_tensile_stress_area_jis
print("Tensile area of threaded portion of bolt = ", Athread, ' mm^2')

Fycl = M5bolt.yield_clamping_force(mu_s)
print("yield clamping force = ", Fycl, " N")

# [N], desired preload = tension, 80% of yield capability
Pdes = 0.8 * Fycl
Treq = M5bolt.torque_for_tension(prld=Pdes, k=kest)
print("Required Torque = ", Treq, " N-mm")

# Turn of the nut method to get preload:
theta = M5bolt.nut_turns_for_tension(
    prld=Pdes, 
    lj=50.0, 
    hn=5.0, 
    hb=5.0,
)
print("nut turns for preload = ", theta, " deg")
print("nut turns for preload = ", theta / 360.0, " revs")

# [mm], bolt stretch (change in length) due to preload:
delta = M5bolt.length_change(prld=Pdes, lj=50.0)
print("Bolt Stretch = ", delta, " mm")

Tp = M5bolt.tension_torque_t1(Pdes)
print("torque to apply desired tension (preload) = ", Tp, " N-mm")

Ttf = M5bolt.thread_friction_torque_t2(mu_s, Pdes)
print("torque to overcome thread friction = ", Ttf, " N-mm")

Tbs = M5bolt.washer_friction_torque_t3(mu_w, Pdes)
print("torque to overcome washer friction = ", Tbs, " N-mm")

Ttot = Tp + Ttf + Tbs
print("Total torque = ", Ttot, " N-mm")

sigma = M5bolt.thread_section_stress(Pdes, Ttf)
print("thread cross section stress = ", sigma, " MPa  < ", M5bolt.sigma_y, " MPa")

# What is the axial load capability of the joint?
# What is the shear capability of the joint?
# Temperature effects during service?


# Machinery Handbook 29th Edition Pg 1531 comparison:
print("\n\nM10 Example:")
M10bolt = M10MetricFastener()
print("d2 = ", M10bolt.d2)

# [-], estimated coefficient of friction between threads:
mu_s = 0.12

# [-], estimated coefficient of friction between nut face and washer:
mu_w = 0.12

# estimated k (nut factor):
kest = M10bolt.estimated_k(
    mus=mu_s, 
    muw=mu_w,
)
print("estimated nut factor, k = ", kest)

# what is max tension available based on stress capability?
# what is the yield clamping force?

# Athread = M5bolt.thread_tensile_stress_area
# print("Tensile area of threaded portion of bolt = ", Athread, ' mm^2')
Athread = M10bolt.thread_tensile_stress_area_jis
print("Tensile area of threaded portion of bolt = ", Athread, ' mm^2')

Fycl = M10bolt.yield_clamping_force(mu_s)
print("yield clamping force = ", Fycl, " N")

# [N], desired preload = tension
Pdes = Fycl
Treq = M10bolt.torque_for_tension(prld=Pdes, k=kest)
print("Required Torque = ", Treq, " N-mm")

Ttf = M10bolt.thread_friction_torque_t2(mu_s, Pdes)
print("torque to overcome thread friction = ", Ttf, " N-mm")

sigma = M10bolt.thread_section_stress(Pdes, Ttf)
print("thread cross section stress = ", sigma, " MPa  < ", M10bolt.sigma_y, " MPa")

# Turn of the nut method to get preload:
theta = M10bolt.nut_turns_for_tension(
    prld=Pdes, 
    lj=30.0, 
    hn=10.0, 
    hb=10.0,
)
print("nut turns for preload = ", theta, " deg")
print("nut turns for preload = ", theta / 360.0, " revs")
