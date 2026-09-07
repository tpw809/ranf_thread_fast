"""Reproduce data in NASA-TM-2012-217454

46 tests

3/8 in 0.375-24 UNJF-3A bolt

NAS1956C14 bolt
NAS1805-6 Nut
H20-6 220 ksi alloy steel Nut
NAS1587-6(C) Washer
NAS1395C6L Insert 

Puck faying surfaces lubricated

Bolt Material: A-286 CRES, 
180 ksi min ult tensile strength
108 ksi min ult shear strength

key-locked insert in Aluminum 7075 puck

440C puck

Target preload = 8000 lb

400 in-lb for nut configuration
600 in-lb for insert configuration

"""
import numpy as np

import thread_fast

######################
# Materials:
######################

bolt_material = thread_fast.english_material_database.a286_mat_dict

bolt_material = thread_fast.process_material_input(bolt_material)

print(f"\nBolt material: \n{bolt_material}")

puck_material1 = thread_fast.english_material_database.SS440C_mat_dict

puck_material1 = thread_fast.process_material_input(puck_material1)

print(f"\nPuck material: \n{puck_material1}")



bolt_thread = thread_fast.english_thread_database.UNJF_ext_3_8_24_class3A

print(f"\nBolt thread = \n{bolt_thread}")

insert_thread = None
nut_thread = None


######################
# nut factor:
######################
# T = k * p * d
# T = tightening torque
# k = nut factor
# p = preload
# d = nominal bolt diameter
# k = T / (p * d)

# [in], nominal bolt diameter:
d = 3.0 / 8.0

# [lb], target preload:
preload_target = 8000.0

# [in-lb], nut target torque:
torque_target_nut = 400.0
k_nut = torque_target_nut / (d * preload_target)
print(f"k_nut = {k_nut}")

# [in-lb], insert target torque:
torque_target_insert = 1200.0
torque_target_insert = 600.0
k_insert = torque_target_insert / (d * preload_target)
print(f"k_insert = {k_insert}")


######################
# Clamped Parts:
######################
print("\nClampedParts:")

clamped_part1_dict = {
    'type': 'ClampedPart',
    'name': 'clamped_part1',
    'material': puck_material1,
    'D_hole': 6.1,
    'D_outer': 12.5,
    'thickness': 5.0,
}
print(f"\ninput: \n{clamped_part1_dict}\n")
# clamped_part1_dict = process_clamped_part_input(clamped_part1_dict)
# print(f"\noutput: \n{clamped_part1_dict}\n")

clamped_part2_dict = {
    'type': 'ClampedPart',
    'name': 'clamped_part2',
    'material': puck_material1,
    'D_hole': 6.1,
    'D_outer': 12.5,
    'thickness': 10.0,
}
print(f"\ninput: \n{clamped_part2_dict}\n")
# clamped_part2_dict = process_clamped_part_input(clamped_part2_dict)
# print(f"\noutput: \n{clamped_part2_dict}\n")


######################
# Test Matrix:
######################

test_matrix = {
    0: {
        "load_angle": 0.0,
        "shear_plane": "body",
        "install_torque": 0.0,
        "test_ultimate_load": 17366,
        "failure_location": "thread_strip",
    },
}

print(test_matrix)
print(test_matrix[0])

