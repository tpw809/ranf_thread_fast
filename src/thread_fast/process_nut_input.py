"""
Use functional programming instead of object oriented...

focus on web-app interface...

Goal: user can input as little or as much as they want...

Also try going unitless...

Parameters:

- type: 'Nut'
- name: descriptor
- material: 
- thread:
- length:
- Do: outer diameter

"""
import numpy as np
import thread_fast.conversion_factors as cf
import thread_fast.nsts_08307a as nsts_08307a
import thread_fast.nasa_tm_106943 as nasa_tm_106943
from thread_fast.material_class import Material
from thread_fast.threads.metric_thread_class import ExternalMetricThread
from thread_fast.process_material_input import process_material_input
from thread_fast.threads.process_metric_thread import process_metric_thread_input


def process_nut_input(input_dict: dict):
    """Read and modify the input dict to ensure completeness and validity.
    
    Must supply:
    - type: 'Nut'
    - name: description
    - material: material data dictionary
    - thread: thread data dictionary
    - length: length of the nut
    - Do: outer diameter (bearing area)
    
    Optional:
    
    """
    # check required inputs:
    
    assert input_dict['type'] == 'Nut'
    
    assert input_dict.get('name') is not None
    
    assert input_dict.get('material') is not None
    
    assert input_dict.get('thread') is not None
    
    assert 'Do' in input_dict
    
    assert 'length' in input_dict
    
    # process subclasses:
    input_dict['material'] = process_material_input(input_dict['material'])
    input_dict['thread'] = process_metric_thread_input(input_dict['thread'])
    
    # outer bearing diameter (on abutment):
    Do = input_dict['Do']
    assert Do > 0.0, "nut outer diamter must be > 0"
    
    length = input_dict['length']
    assert length > 0.0, "nut length must be > 0"
    
    # the following is bolted joint level, includes both innternal and external thread goemetry: 
    
    # shear area of internal threads:
    # NSTS_08307A, pg A-4 & A-5:
    # A_si = 
    
    # thread shear (pull out) load allowable, internal thread
    # NSTS 08307A, pg A-4
    # PA_s_08307a = nsts_08307a.internal_thread_shear_load_allowable(
    #     A_si=A_si,
    #     F_su_nut=material.Ssu,
    # )
    # input_dict['PA_s_08307a'] = PA_s_08307a
    
    # TODO: add 'processed' tag ???
    
    return input_dict


def main() -> None:
    
    material_dict = {
        'type': 'Material',
        'name': 'test_input_dict',
        'E': 200000.0,  # modulus of elasticity
        'nu': 0.3,  # Poisson's ratio
        'cte': 2.0e-6,  # coefficient of thermal expansion
        'Sty': 600.0,  # tensile yield strength
        'Stu': 800.0,  # tensile ultimate strength
    }
    print(f"\nmaterial_dict = \n{material_dict}\n")
    
    material_dict = process_material_input(material_dict)
    print(f"\nmaterial_dict = \n{material_dict}\n")
    
    thread_dict = {
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
    print(f"\nthread_dict = \n{thread_dict}\n")
    
    thread_dict = process_metric_thread_input(thread_dict)
    print(f"\nthread_dict = \n{thread_dict}\n")
    
    input_dict = {
        'type': 'Nut',
        'name': 'nut_test_input_dict',
        'material': material_dict,
        'thread': thread_dict,
        'Do': 8.5,
        'length': 5.0,
    }
    print(f"\ninput_dict = \n{input_dict}\n")
    
    output_dict = process_nut_input(input_dict)
    print(f"\noutput_dict = \n{output_dict}\n")
    

if __name__ == "__main__":
    main()
    