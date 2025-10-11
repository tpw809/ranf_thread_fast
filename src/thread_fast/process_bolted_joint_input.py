"""
Use functional programming instead of object oriented...

focus on web-app interface...

Goal: user can input as little or as much as they want...

Also try going unitless...

Parameters:

- type: 'BoltedJoint'
- name: descriptor
- fastener: fastener data
- nut: nut data
- insert: insert data
- threaded_hole: threaded hole data
- mu_thread: coefficient of friction between threads
- mu_abutment: coefficient of friction between bolt head and washer or nut and washer (whichever is turned in torquing)

"""
import numpy as np
import thread_fast.conversion_factors as cf
import thread_fast.nsts_08307a as nsts_08307a
import thread_fast.nasa_tm_106943 as nasa_tm_106943
import thread_fast.nasa_std_5020.nasa_std_5020b as nasa_std_5020b
from thread_fast.material_class import Material
from thread_fast.threads.metric_thread_class import ExternalMetricThread
from thread_fast.process_material_input import process_material_input
from thread_fast.threads.process_metric_thread import process_metric_thread_input
from thread_fast.process_nut_input import process_nut_input
from thread_fast.process_fastener_input import process_fastener_input
from thread_fast.process_washer_input import process_washer_input
from thread_fast.process_clamped_part_input import process_clamped_part_input


def process_bolted_joint_input(input_dict: dict):
    """Read and modify the input dict to ensure completeness and validity.
    
    Must supply:
    - type: 'BoltedJoint'
    - name: description
    - fastener: fastener data dictionary
    
    Optional:
    
    
    """
    # check required inputs:
    
    assert input_dict['type'] == 'BoltedJoint'
    
    assert 'name' in input_dict
    
    assert 'fastener' in input_dict
    
    # at least 1 must exist: nut, insert, threaded_hole...
    # depends on configuration:
    # assert 'nut' in input_dict
    
    threaded_part_exists = False
    
    if 'nut' in input_dict:
        threaded_part_exists = True
        assert 'insert' not in input_dict
        assert 'threaded_hole' not in input_dict
    elif 'insert' in input_dict:
        threaded_part_exists = True
    elif 'threaded_hole' in input_dict:
        threaded_part_exists = True
    else:
        pass
    
    assert threaded_part_exists, "nut, insert, or threaded_hole must be included"
    
    #################################
    # process subsystems:
    #################################
    
    # Nut:
    if 'nut' in input_dict:
        input_dict['nut'] = process_nut_input(input_dict['nut'])
    
    nut = input_dict['nut']
    
    # Fastener:
    input_dict['fastener'] = process_fastener_input(input_dict['fastener'])
    
    # use dictionary or create an object?
    fastener = input_dict['fastener']
    
    
    # coefficient of friction at threads:
    assert 'mu_thread' in input_dict
    mu_thread = input_dict['mu_thread']
    assert mu_thread >= 0.0, "coefficient of friction must be >= 0.0"
    
    # coefficient of friction under head or nut:
    assert 'mu_abutment' in input_dict
    mu_abutment = input_dict['mu_abutment']
    assert mu_abutment >= 0.0, "coefficient of friction must be >= 0.0"
    
    #################################
    # Safety Factors:
    #################################
    
    # Yield Safety Factor:
    assert 'yield_safety_factor' in input_dict
    SF_y = input_dict['yield_safety_factor']
    assert SF_y >= 1.0, "factors of safety must be >= 1.0"
    
    # Ultimate Safety Factor:
    assert 'ultimate_safety_factor' in input_dict
    SF_u = input_dict['ultimate_safety_factor']
    assert SF_u >= 1.0, "factors of safety must be >= 1.0"
    
    # Separation Safety Factor:
    assert 'separation_safety_factor' in input_dict
    SF_sep = input_dict['separation_safety_factor']
    assert SF_sep >= 1.0, "factors of safety must be >= 1.0"
    
    # Fitting Factor:
    assert 'fitting_factor' in input_dict
    FF = input_dict['fitting_factor']
    assert FF >= 1.0, "fitting factor must be >= 1.0"
    
    #################################
    # Temperatures:
    #################################
    assert 'min_temperature' in input_dict
    assert 'max_temperature' in input_dict
    assert 'ambient_temperature' in input_dict
    T_amb = input_dict['ambient_temperature']
    T_min = input_dict['min_temperature']
    T_max = input_dict['max_temperature']
    
    assert T_max >= T_min, "max temperature must be >= min temperature"
    
    # [C], change in temperature:
    delta_T_min = T_min - T_amb
    delta_T_max = T_max - T_amb
    
    
    #################################
    # Check Externally Applied Loads:
    #################################
    
    if 'applied_tensile_load' in input_dict:
        applied_tensile_load = input_dict['applied_tensile_load']
        assert applied_tensile_load >= 0.0, "externally applied limit tensile load must be >= 0.0"
    else:
        applied_tensile_load = 0.0
        input_dict['applied_tensile_load'] = 0.0
    
    if 'applied_shear_load' in input_dict:
        applied_shear_load = input_dict['applied_shear_load']
        assert applied_shear_load >= 0.0, "externally applied limit shear load must be >= 0.0"
    else:
        applied_shear_load = 0.0
        input_dict['applied_shear_load'] = 0.0
    
    # TODO: Bending Moment:
    
    # Loaded Parts Index:
    assert 'loaded_part_index' in input_dict
    loaded_part_index = input_dict['loaded_part_index']
    print(loaded_part_index)
    assert len(loaded_part_index) >= 2, "there must be at least 2 loaded parts (equal and opposite reaction)"
    
    #################################
    # Preloading:
    #################################
    
    # Relaxation Ratio:
    assert 'relaxation_ratio' in input_dict
    relaxation_ratio = input_dict['relaxation_ratio']
    assert relaxation_ratio >= 0.0, "relaxation ratio must be >= 0.0"
    
    # Preload stress ratio:
    assert 'preload_stress_ratio' in input_dict
    preload_stress_ratio = input_dict['preload_stress_ratio']
    assert 0.0 <= preload_stress_ratio <= 1.0
    
    # Preload uncertainty factor:
    assert 'preload_uncertainty_factor' in input_dict
    preload_uncertainty_factor = input_dict['preload_uncertainty_factor']
    assert preload_uncertainty_factor >= 0.0
    
    # TODO: validity check:
    lower_preload_tolerance_factor = input_dict['lower_preload_tolerance_factor']
    
    # TODO: validity check:
    upper_preload_tolerance_factor = input_dict['upper_preload_tolerance_factor']
    
    # [bool], is the nut or fastener head torqued?
    # TODO: validity check:
    nut_torqued = input_dict['nut_torqued']
    
    # preload lost due to material creep:
    if 'preload_loss_due_to_material_creep' in input_dict:
        preload_loss_due_to_material_creep = input_dict['preload_loss_due_to_material_creep']
        assert preload_loss_due_to_material_creep >= 0.0
    else:
        preload_loss_due_to_material_creep = 0.0
    
    
    ###############################
    # Joint Length:
    ###############################
    
    # Check length of clamped parts puts threads at the nut or insert...
    clamped_parts = input_dict['clamped_parts']
        
    L_total_fast = fastener['length']
    print(f"L_total_fast = {L_total_fast}")
    
    #TODO: adjust for threaded holes or inserts...
    L_total_clamped_parts = 0.0
    
    for part in clamped_parts:
        try:
            temp_length = part['length']
        except:
            try:
                temp_length = part['thickness']
            except:    
                temp_length = 0.0
        L_total_clamped_parts += temp_length
    
    print(f"L_total_clamped_parts = {L_total_clamped_parts}")
    
    # TODO: include length of nut or insert
    # must extent past by 1 full thread
    # must engage 3 full threads
    
    if L_total_fast < L_total_clamped_parts:
        # only matters for config #1:
        raise Exception("clamped parts length exceeds fastener length")
        
    
    # TODO: check shank length < clamped parts length
    # plus some margin...
    # what margin? 2 threads?
    if fastener['L_shank'] + 2.0*fastener['thread']['pitch'] > L_total_clamped_parts:
        raise Exception("fastener shank (unthreaded portion) longer than clamped parts")
    
    # TODO: check later that bolt stretch is < 2 threads...
    
    # Length of engagement:
    # TODO: deal with inserts or tapped holes:
    if input_dict.get('L_e') is None:
        L_e = nut['length']
        input_dict['L_e'] = L_e
    
    print(f"Length of Engagement = {L_e}")
    
    ###############################
    # Joint Stiffness:
    ###############################
    
    # [N/mm], fastener (bolt) stiffness:
    K_b = fastener['stiffness']
    print(f"K_b, bolt stiffness = {K_b}")
    
    L_list = []
    E_list = []
    
    for part in clamped_parts:
        try:
            temp_length = part['length']
        except:
            try:
                temp_length = part['thickness']
            except:    
                temp_length = 0.0
        L_list.append(temp_length)
        E_list.append(part['material']['E'])
    
    # joint modulus:
    E_j = nasa_tm_106943.eq34mod(
        L_list=L_list,
        E_list=E_list,
    )
    
    # [N/mm], estimated clamped parts (joint) stiffness:
    K_j_106943 = nasa_tm_106943.eq33(
        E_j=E_j,
        D=fastener['thread']['basic_major_diameter'],
        L=L_total_clamped_parts,
    )
    print(f"K_j_106943 = {K_j_106943}")
    
    # joint stiffness:
    K_j = K_j_106943
    
    
    ###############################
    # Joint Stiffness Factor, phi:
    ###############################
    
    if input_dict.get('phi') is None:
        print("must estimate phi...")
        # NASA-TM-106943 eq 29:
        # NASA-STD-5020B eq 9:
        phi = nasa_std_5020b.eq9(
            k_b=K_b,
            k_c=K_j,
        )
        input_dict['phi'] = phi
    else:
        print("phi provided")
        phi = input_dict['phi']
        assert phi > 0.0
    
    print(f"phi = {phi}")
    
    
    ###############################
    # Load Introduction Factor, n:
    ###############################
    
    # depends on configuration !!!
    # start with configs 1 and 3...
    
    # distance between load planes in clamped parts
    # used for load introduction factor, n
    
    if 'distance_between_load_planes' in input_dict:
        if distance_between_load_planes is not None:
            distance_between_load_planes = input_dict['distance_between_load_planes']
            
            assert 0.0 <= distance_between_load_planes <= L_total_clamped_parts
    
    else:
        # use loaded_part_index...
        # assumes load is applied at middle of the loaded part
        distance_between_load_planes = 0.0
        
        if nut is not None:
            # configuration 1:
            for i, part in enumerate(clamped_parts):
                if i == loaded_part_index[0]:
                    distance_between_load_planes += clamped_parts[i]['thickness'] / 2.0
                
                if loaded_part_index[0] < i < loaded_part_index[1]:
                    distance_between_load_planes += clamped_parts[i]['thickness']
                
                if i == loaded_part_index[1]:
                    distance_between_load_planes += clamped_parts[i]['thickness'] / 2.0
    
            # NASA-TM-106943 eq 18, pg 10:
            n = nasa_tm_106943.eq18(
                d=distance_between_load_planes, 
                t=L_total_clamped_parts,
            )
            
            # TODO: configuration ???:
    
        if input_dict.get('insert') is not None:
            # configuration 3:
            raise Exception("insert not implemented yet...")
    
        # configuration 2 & 4 = flat head screws
    
    # NASA-STD-5020B, eq 37, pg 52:
    # NASA-STD-5020B, eq 48, pg 56:
    # NASA-STD-5020B, eq 52, pg 56:
    # NASA-STD-5020B, eq 57, pg 57:
    
    # NASA-TM-106943 eq 35, pg 12:
    # NASA-TM-106943 eq 46, pg 12:
    
    print(f"load introduction factor, n = {n}")
    
    
    ###############################
    # Nut Factor, K:
    ###############################
    
    if input_dict['nut_factor'] is None:
        print("need to calculate nut factors...")
    
    
    
    
    
    return input_dict


def main() -> None:
    
    print("\nFastener Material:")
    fastener_material_dict = {
        'type': 'Material',
        'name': 'fastener_material_dict',
        'E': 200000.0,  # modulus of elasticity
        'nu': 0.3,  # Poisson's ratio
        'cte': 2.0e-6,  # coefficient of thermal expansion
        'Sty': 600.0,  # tensile yield strength
        'Stu': 800.0,  # tensile ultimate strength
    }
    print(f"\ninput: \n{fastener_material_dict}")
    fastener_material_dict = process_material_input(fastener_material_dict)
    print(f"\noutput: \n{fastener_material_dict}")
    
    print("\nNut Material:")
    nut_material_dict = {
        'type': 'Material',
        'name': 'nut_material_dict',
        'E': 200000.0,  # modulus of elasticity
        'nu': 0.3,  # Poisson's ratio
        'cte': 2.0e-6,  # coefficient of thermal expansion
        'Sty': 600.0,  # tensile yield strength
        'Stu': 800.0,  # tensile ultimate strength
    }
    print(f"\ninput: \n{nut_material_dict}")
    
    print("\nFastener Thread:")
    fastener_thread_dict = {
        'type': 'Metric_Thread',
        'name': 'fastener_thread_dict',
        'basic_major_diameter': 6.0,
        'pitch': 1.0,
        'beta_deg': 30.0,  # thread half angle
        'external': True,
        'internal': False,
        'profile': 'MJ',  # thread profile, M or MJ
        'tolerance_grade': 6,
        'allowance_class': 'h',
    }
    print(f"\ninput: \n{fastener_thread_dict}")
    
    print("\nNut Thread:")
    nut_thread_dict = {
        'type': 'Metric_Thread',
        'name': 'test_input_dict',
        'basic_major_diameter': 6.0,
        'pitch': 1.0,
        'beta_deg': 30.0,  # thread half angle
        'external': False,
        'internal': True,
        'profile': 'MJ',  # thread profile, M or MJ
        'tolerance_grade': 6,
        'allowance_class': 'H',
    }
    print(nut_thread_dict)
    
    print("\nNut:")
    nut_dict = {
        'type': 'Nut',
        'name': 'nut_dict',
        'material': nut_material_dict,
        'thread': nut_thread_dict,
        'Do': 8.5,
        'length': 5.0,
    }
    print(nut_dict)
    
    print("\nFastener:")
    fastener_dict = {
        'type': 'Fastener',
        'name': 'fastener_dict',
        'material': fastener_material_dict,
        'thread': fastener_thread_dict,
        'Do_head': 8.5,
        'Do_shank': 5.0,
        'L_shank': 10.0,
        'L_thread': 20.0,
    }
    print(fastener_dict)
    
    
    print("\nWasher Material:")
    washer_material_dict = {
        'type': 'Material',
        'name': 'washer_material_dict',
        'E': 200000.0,  # modulus of elasticity
        'nu': 0.3,  # Poisson's ratio
        'cte': 2.0e-6,  # coefficient of thermal expansion
        'Sty': 600.0,  # tensile yield strength
        'Stu': 800.0,  # tensile ultimate strength
    }
    print(f"\ninput: \n{washer_material_dict}")
    washer_material_dict = process_material_input(washer_material_dict)
    print(f"\noutput: \n{washer_material_dict}")
    
    print("\nWasher:")
    washer_dict = {
        'type': 'Washer',
        'name': 'washer_test_input_dict',
        'material': washer_material_dict,
        'D_hole': 6.1,
        'D_outer': 8.5,
        'thickness': 2.0,
    }
    print(f"\ninput: \n{washer_dict}")
    washer_dict = process_washer_input(washer_dict)
    print(f"\noutput: \n{washer_dict}")
    
    
    # Loaded parts:
    ti6al4v_material_dict = {
        'type': 'Material',
        'name': 'ti6al4v',
        'E': 114.0e3,  # modulus of elasticity
        'nu': 0.342,  # Poisson's ratio
        'cte': 8.6e-6,  # coefficient of thermal expansion
        'Sty': 880.0,  # tensile yield strength
        'Stu': 950.0,  # tensile ultimate strength
    }
    
    print("\nClampedPart:")
    clamped_part1_dict = {
        'type': 'ClampedPart',
        'name': 'clamped_part1',
        'material': ti6al4v_material_dict,
        'D_hole': 6.1,
        'D_outer': 12.5,
        'thickness': 5.0,
    }
    print(f"\ninput: \n{clamped_part1_dict}")
    clamped_part1_dict = process_clamped_part_input(clamped_part1_dict)
    print(f"\noutput: \n{clamped_part1_dict}")
    
    clamped_part2_dict = {
        'type': 'ClampedPart',
        'name': 'clamped_part2',
        'material': ti6al4v_material_dict,
        'D_hole': 6.1,
        'D_outer': 12.5,
        'thickness': 10.0,
    }
    print(f"\ninput: \n{clamped_part2_dict}")
    clamped_part2_dict = process_clamped_part_input(clamped_part2_dict)
    print(f"\noutput: \n{clamped_part2_dict}")
    
    
    print("\nBoltedJoint:")
    bolted_joint_input_dict = {
        'type': 'BoltedJoint',
        'name': 'bolted_joint_input_test',
        'fastener': fastener_dict,
        'clamped_parts': [washer_dict, clamped_part1_dict, clamped_part2_dict, washer_dict],
        'nut': nut_dict,
        # 'insert': None,
        # 'threaded_hole': None,
        'mu_thread': 0.15,  # coefficient of friction between threads
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
    print(f"input: \n{bolted_joint_input_dict}")

    output_dict = process_bolted_joint_input(bolted_joint_input_dict)
    print(f"output: \n{output_dict}")


if __name__ == "__main__":
    main()
    