"""
Use functional programming instead of object oriented...

focus on web-app interface...

Goal: user can input as little or as much as they want...

Also try going unitless...

Parameters:

- type: 'BoltedJoint'
- name: descriptor


"""
import numpy as np
import thread_fast.conversion_factors as cf
import thread_fast.nsts_08307a as nsts_08307a
import thread_fast.nasa_tm_106943 as nasa_tm_106943
from thread_fast.material_class import Material
from thread_fast.threads.metric_thread_class import ExternalMetricThread
from thread_fast.process_material_input import process_material_input
from thread_fast.threads.process_metric_thread import process_metric_thread_input


def process_bolted_joint_input(input_dict: dict):
    """Read and modify the input dict to ensure completeness and validity.
    
    Must supply:
    - type: 'Nut'
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
    elif 'insert' in input_dict:
        threaded_part_exists = True
    elif 'threaded_hole' in input_dict:
        threaded_part_exists = True
    else:
        pass
    
    assert threaded_part_exists, "nut, insert, or threaded_hole must be included"
    
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
    assert 'separation_safety_factor' in input_dict
    assert 'yield_safety_factor' in input_dict
    assert 'ultimate_safety_factor' in input_dict
    assert 'fitting_factor' in input_dict
    
    SF_y = input_dict['yield_safety_factor']
    assert SF_y >= 1.0, "factors of safety must be >= 1.0"
    
    SF_u = input_dict['ultimate_safety_factor']
    assert SF_u >= 1.0, "factors of safety must be >= 1.0"
    
    SF_sep = input_dict['separation_safety_factor']
    assert SF_sep >= 1.0, "factors of safety must be >= 1.0"
    
    # Fitting Factor:
    FF = input_dict['fitting_factor']
    assert FF >= 1.0, "fitting factor must be >= 1.0"
    
    # Preloading:
    assert 'preload_stress_ratio' in input_dict
    assert 'preload_uncertainty_factor' in input_dict
    
    
    
    # process inputs:
    loaded_part_index = input_dict['loaded_part_index']
    print(loaded_part_index)
    
    
    if input_dict['nut_factor'] is None:
        print("need to calculate nut factors...")
    
        
    
    
    return input_dict


def main() -> None:
    
    fastener_material_dict = {
        'type': 'Material',
        'name': 'fastener_material_dict',
        'E': 200000.0,  # modulus of elasticity
        'nu': 0.3,  # Poisson's ratio
        'cte': 2.0e-6,  # coefficient of thermal expansion
        'Sty': 600.0,  # tensile yield strength
        'Stu': 800.0,  # tensile ultimate strength
    }
    
    nut_material_dict = {
        'type': 'Material',
        'name': 'nut_material_dict',
        'E': 200000.0,  # modulus of elasticity
        'nu': 0.3,  # Poisson's ratio
        'cte': 2.0e-6,  # coefficient of thermal expansion
        'Sty': 600.0,  # tensile yield strength
        'Stu': 800.0,  # tensile ultimate strength
    }
    
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
    
    nut_dict = {
        'type': 'Nut',
        'name': 'nut_dict',
        'material': nut_material_dict,
        'thread': nut_thread_dict,
        'Do': 8.5,
        'length': 5.0,
    }
    
    fastener_dict = {
        'type': 'Fastener',
        'name': 'fastener_dict',
        'material': fastener_material_dict,
        'thread': fastener_thread_dict,
        'Do_head': 8.5,
        'Do_shank': 5.0,
        'L_shank': 10.0,
        'L_thread': 10.0,
    }

    bolted_joint_input_dict = {
        'type': 'BoltedJoint',
        'name': 'bolted_joint_input_test',
        'fastener': fastener_dict,
        'clamped_parts': [],
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
    }

    output_dict = process_bolted_joint_input(bolted_joint_input_dict)
    print(output_dict)


if __name__ == "__main__":
    main()
    