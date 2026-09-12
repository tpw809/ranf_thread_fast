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
import json
import numpy as np

import thread_fast

######################
# Materials:
######################

bolt_material_dict = thread_fast.english_material_database.a286_mat_dict

bolt_material_dict = thread_fast.process_material_input(bolt_material_dict)

print(f"\nBolt material: \n")
print(json.dumps(bolt_material_dict, indent=4))

puck_material1_dict = thread_fast.english_material_database.SS440C_mat_dict

puck_material1_dict = thread_fast.process_material_input(puck_material1_dict)

print(f"\nPuck material: \n")
print(json.dumps(puck_material1_dict, indent=4))

######################
# Threads:
######################

# bolt:
bolt_thread_dict = thread_fast.english_thread_database.UNJF_ext_3_8_24_class3A
print(f"\nBolt thread: \n")
print(json.dumps(bolt_thread_dict, indent=4))

# insert:
insert_thread_dict = None

# nut:
nut_thread_dict = thread_fast.english_thread_database.UNJF_int_3_8_24_class3A
print(f"\nNut thread: \n")
print(json.dumps(nut_thread_dict, indent=4))


######################
# Fastener (Bolt):
######################

# minimal fastener input dictionary:
bolt_dict = {
    'type': 'Fastener',
    'name': 'fastener_test_input_dict',
    'units': 'english: in, lb',
    'material': bolt_material_dict,
    'thread': bolt_thread_dict,
    'Do_head': 8.5,
    'Do_shank': 3.0/8.0,
    'L_shank': 10.0,
    'L_thread': 10.0,
}

bolt_dict = thread_fast.process_fastener_input(bolt_dict)
print(f"\nbolt_dict: \n")
print(json.dumps(bolt_dict, indent=4))


######################
# Nut:
######################

nut_dict = {
    'type': 'Nut',
    'units': 'english: in, lb, psi, F',
    'name': 'nut_test_input_dict',
    'material': bolt_material_dict,
    'thread': nut_thread_dict,
    'Do': 8.5,
    'length': 5.0,
}

nut_dict = thread_fast.process_nut_input(nut_dict)
print(f"\nnut_dict: \n")
print(json.dumps(nut_dict, indent=4))

######################
# Insert:
######################



######################
# Washers:
######################

print("\nWasher:")
washer_dict = {
    'type': 'Washer',
    'units': 'english: in, lb, psi, F',
    'name': 'washer',
    'material': puck_material1_dict,
    'D_hole': 3.0/8.0,
    'D_outer': 8.5,
    'thickness': 2.0,
}

washer_dict = thread_fast.process_washer_input(washer_dict)
print(f"\nwasher_dict: \n")
print(json.dumps(washer_dict, indent=4))


######################
# Clamped Parts:
######################
print("\nClampedParts:")

clamped_part1_dict = {
    'type': 'ClampedPart',
    'units': 'english: in, lb, psi, F',
    'name': 'clamped_part1',
    'material': puck_material1_dict,
    'D_hole': 6.1,
    'D_outer': 12.5,
    'thickness': 5.0,
}

# clamped_part1_dict = process_clamped_part_input(clamped_part1_dict)
print(f"\nclamped_part1_dict: \n")
print(json.dumps(clamped_part1_dict, indent=4))

clamped_part2_dict = {
    'type': 'ClampedPart',
    'units': 'english: in, lb, psi, F',
    'name': 'clamped_part2',
    'material': puck_material1_dict,
    'D_hole': 6.1,
    'D_outer': 12.5,
    'thickness': 10.0,
}

# clamped_part2_dict = process_clamped_part_input(clamped_part2_dict)
print(f"\nclamped_part2_dict: \n")
print(json.dumps(clamped_part2_dict, indent=4))


######################
# Preloading:
######################

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




######################
# Bolted Joint:
######################


print("\nBoltedJoint:")
bolted_joint_dict = {
    'type': 'BoltedJoint',
    'units': 'english: lb, in, psi, F',
    'name': 'bolted_joint_input_test',
    'fastener': bolt_dict,
    'clamped_parts': [washer_dict, clamped_part1_dict, clamped_part2_dict, washer_dict],
    'nut': nut_dict,
    # 'insert': None,
    # 'threaded_hole': None,
    'mu_thread': 0.15,  # threads coefficient of friction
    'mu_abutment': 0.1,  # coefficient of friction between head or nut and washer
    'separation_safety_factor': 1.2,
    'yield_safety_factor': 1.1,
    'ultimate_safety_factor': 1.4,
    'fitting_factor': 1.15,
    'preload_stress_ratio': 0.65,
    'preload_uncertainty_factor': 0.25,
    'lower_preload_tolerance_factor': 0.9,
    'upper_preload_tolerance_factor': 1.1,
    'relaxation_ratio': 0.05,
    'preload_loss_due_to_material_creep': 0.0,
    'ambient_temperature': 20.0,
    'max_temperature': 40.0,
    'min_temperature': 10.0,
    'applied_tensile_load': 100.0,  # externally applied
    'applied_shear_load': 100.0,  # externally applied
    'loaded_part_index': [1,2],  # which clamped parts are externally loaded?
    'nut_torqued': False,  # is the bolt head or nut torqued during preloading?
    'distance_between_loading_planes': None,
    'material_creep_preload_loss': 0.0,
    'nut_factor': None,  # optional override
    'applied_preload_torque': None,  # optional override
    'applied_preload': None,  # optional override
    'phi': None,
}

bolted_joint_dict = thread_fast.process_bolted_joint_input(bolted_joint_dict)
print(f"\nbolted_joint_dict: \n")
print(json.dumps(bolted_joint_dict, indent=4))

# Find Predicted Failure Loads:

# TODO: ...
