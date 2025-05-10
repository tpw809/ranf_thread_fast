"""Test English Fastener Class
Timothy P Woodard
July 1, 2021
"""
import numpy as np
from english_fastener_class import EnglishFastener

# Bolted Joint description:
# 1/2in-20 socket head cap screw
# bolt material = 18-8 stainless steel
# clamped material = aluminum
# secured with nut
# washers between nut and bolt head
# installed using torque wrench

# create bolt object:
bolt = EnglishFastener()

# mu_s [-], estimated coefficient of friction between threads
mu_s = 0.14

# mu_w [-], estimated coefficient of friction between nut face and washer
mu_w = 0.14

# estimated k (nut factor):
k_est = bolt.estimated_k(
    mus=mu_s, 
    muw=mu_w,
)
print("estimated nut factor, k = ", k_est)

Athread = bolt.thread_tensile_stress_area
print("Tensile area of threaded portion of bolt = ", Athread, ' in^2')

Fycl = bolt.yield_clamping_force(mu_s)
print("yield clamping force = ", Fycl, " lb")

# Pdes [lb], desired preload = tension, 80% of yield capability
Pdes = 0.8 * Fycl
Treq = bolt.torque_for_tension(prld=Pdes, k=k_est)
print("Required Torque = ", Treq, " in-lb")

# Turn of the nut method to get preload:
theta = bolt.nut_turns_for_tension(prld=Pdes, lj=50.0, hn=5.0, hb=5.0)
print("nut turns for preload = ", theta, " deg")
print("nut turns for preload = ", theta / 360.0, " revs")

# delta [mm], bolt stretch (change in length) due to preload
delta = bolt.length_change(prld=Pdes, lj=50.0)
print("Bolt Stretch = ", delta, " in")

Tp = bolt.tension_torque_t1(Pdes)
print("torque to apply desired tension (preload) = ", Tp, " in-lb")

Ttf = bolt.thread_friction_torque_t2(mu_s, Pdes)
print("torque to overcome thread friction = ", Ttf, " in-lb")

Tbs = bolt.washer_friction_torque_t3(mu_w, Pdes)
print("torque to overcome washer friction = ", Tbs, " in-lb")

Ttot = Tp + Ttf + Tbs
print("Total torque = ", Ttot, " in-lb")

sigma = bolt.thread_section_stress(Fycl, Ttf)
print("thread cross section stress = ", sigma, " psi  < ", bolt.sigma_y, " psi")

# What is the axial load capability of the joint?
# What is the shear capability of the joint?
# Temperature effects during service?


# Machinery Handbook 29th Edition Pg 1531 comparison:
print("\n\nSecond Example:")
bolt = EnglishFastener()
print("dp = ", bolt.dp)

# mu_s [-], estimated coefficient of friction between threads
mu_s = 0.12

# mu_w [-], estimated coefficient of friction between nut face and washer
mu_w = 0.12

# estimated k (nut factor):
k_est = bolt.estimated_k(
    mus=mu_s, 
    muw=mu_w,
)
print("estimated nut factor, k = ", k_est)

# what is max tension available based on stress capability?
# what is the yield clamping force?

# Athread = bolt.thread_tensile_stress_area
# print("Tensile area of threaded portion of bolt = ", Athread, ' mm^2')
Athread = bolt.thread_tensile_stress_area
print("Tensile area of threaded portion of bolt = ", Athread, ' in^2')

Fycl = bolt.yield_clamping_force(mu_s)
print("yield clamping force = ", Fycl, " lb")

# [N], desired preload = tension:
Pdes = Fycl
Treq = bolt.torque_for_tension(
    prld=Pdes, 
    k=k_est,
)
print("Required Torque = ", Treq, " in-lb")

Ttf = bolt.thread_friction_torque_t2(mu_s, Pdes)
print("torque to overcome thread friction = ", Ttf, " in-lb")

sigma = bolt.thread_section_stress(Fycl, Ttf)
print("thread cross section stress = ", sigma, " psi  < ", bolt.sigma_y, " psi")

# Turn of the nut method to get preload:
theta = bolt.nut_turns_for_tension(
    prld=Pdes, 
    lj=30.0, 
    hn=10.0, 
    hb=10.0,
)
print("nut turns for preload = ", theta, " deg")
print("nut turns for preload = ", theta / 360.0, " revs")
