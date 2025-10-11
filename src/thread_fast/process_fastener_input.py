"""
Use functional programming instead of object oriented...

focus on web-app interface...

Goal: user can input as little or as much as they want...

Also try going unitless...

Parameters:

- type: Fastener
- name: descriptor
- material: material data
- thread: external thread data
- Do_head: head outer diameter
- Do_shank: outer diameter of unthreaded portion
- L_shank: length of unthreaded portion
- L_thread: length of threaded portion

Calculated:

- A_t: thread area
- A_bolt: bolt shank area
- length: total length (thread and shank)
- stiffness
- P_ty_allow
- P_tu_allow

"""
import numpy as np
import thread_fast.conversion_factors as cf
import thread_fast.nsts_08307a as nsts_08307a
import thread_fast.nasa_tm_106943 as nasa_tm_106943
from thread_fast.material_class import Material
from thread_fast.threads.metric_thread_class import ExternalMetricThread
from thread_fast.process_material_input import process_material_input
from thread_fast.threads.process_metric_thread import process_metric_thread_input



def process_fastener_input(input_dict: dict):
    """
    modify the input dict to ensure completeness
    
    Must supply:
    - type
    - name
    - material
    - thread
    - Do_head
    - Do_shank
    - L_shank
    - L_thread
    
    
    Optional:
    
    
    
    """
    # check required inputs:
    
    assert input_dict['type'] == 'Fastener'
    
    assert 'name' in input_dict
    
    assert 'material' in input_dict
    
    assert 'thread' in input_dict
    
    assert 'Do_head' in input_dict
    
    assert 'Do_shank' in input_dict
    
    assert 'L_shank' in input_dict
    
    assert 'L_thread' in input_dict
    
    material = input_dict['material']
    material = process_material_input(material)
    
    thread = input_dict['thread']
    thread = process_metric_thread_input(thread)
    
    Do_head = input_dict['Do_head']
    Do_shank = input_dict['Do_shank']
    L_shank = input_dict['L_shank']
    L_thread = input_dict['L_thread']
    
    assert L_shank >= 0.0, "shank length must be >= 0"
    assert L_thread > 0.0, "thread length must be > 0"
    assert Do_shank > 0.0, "shank diameter must be > 0"
    assert Do_head > Do_shank, "head diameter must be > shank diameter"
    assert Do_head > thread['basic_major_diameter'], "head diameter must be > thread.basic_major_diameter"
    
    # [mm^2], minimum minor diameter area for the fastener threads:
    # NSTS 08307A, bolt_tensile_stress_area
    if input_dict.get('A_t') is None:
        print("calculating A_t...")
        A_t = nsts_08307a.bolt_tensile_stress_area(
            D_e_bsc=thread['basic_major_diameter'], 
            n_0=None,  # tpi
            pitch=thread['pitch'],
        )
        input_dict['A_t'] = A_t
    
    # [N], allowable ultimate tensile load:
    # NSTS 08307A page A-4, ultimate tensile load:
    if input_dict.get('P_tu_allow') is None:
        print("calculating P_tu_allow...")
        P_tu_allow = input_dict['A_t'] * material['Stu']
        input_dict['P_tu_allow'] = P_tu_allow
    
    if input_dict.get('P_ty_allow') is None:
        print("calculating P_ty_allow...")
        P_ty_allow = input_dict['A_t'] * material['Sty']
        input_dict['P_ty_allow'] = P_ty_allow
    
    # [N], allowable ultimate shear load:
    # NASA-STD-5020B eq 12 & 13
    
    # NASA-STD-5020B eq 12:
    # F_su = allowable ultimate shear strength for the fastener material
    F_su = material['Ssu']
    
    # For shank (not threads):
    if input_dict.get('A_bolt') is None:
        A_bolt = np.pi  * thread['basic_major_diameter']**2 / 4.0
        input_dict['A_bolt'] = A_bolt
    
    # P_su_allow: allowable ultimate shear load
    # depends on if threads are in the shear plane...
    
    # NASA-STD-5020B eq 12:
    # threads NOT in shear plane:
    if input_dict.get('P_su_allow_1') is None:
        P_su_allow_1 = input_dict['A_bolt'] * F_su
        input_dict['P_su_allow_1'] = P_su_allow_1

    
    # NASA-STD-5020B eq 13:
    # threads in shear plane:
    if input_dict.get('P_su_allow_2') is None:
        P_su_allow_2 = F_su * A_t
        input_dict['P_su_allow_2'] = P_su_allow_2
    
    
    # Ro_shank = Do_shank / 2.0
    
    # total tensile length:
    # length = L_shank + L_thread
    if input_dict.get('length') is None:
        input_dict['length'] = L_shank + L_thread
    
    
    # Axial Stiffness:
    # k = (A * E) / L
    # NASA-TM-106943 eq 32, pg 12
    if input_dict.get('stiffness') is None:
        A_thread_mean = thread['A_mean']
        A_shank = A_bolt
        k_shank = A_shank * material['E'] / L_shank
        k_thread = A_thread_mean * material['E'] / L_thread
        
        # combined stiffness in series:
        k_total = 1.0 / (1.0 / k_shank + 1.0 / k_thread)
        print(f"k_b_total = {k_total} [N/mm]")
        input_dict['stiffness'] = k_total
    
    
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
    
    material_dict = process_material_input(material_dict)
    print(f"material_dict = \n{material_dict}")
    
    thread_dict = {
        'type': 'Metric_Thread',
        'name': 'test_input_dict',
        'basic_major_diameter': 6.0,
        'pitch': 1.0,
        'beta_deg': 30.0,  # thread half angle
        'external': True,
        'internal': False,
        'profile': 'MJ',  # thread profile, M or MJ
        'tolerance_grade': 6,
        'allowance_class': 'h',
    }
    
    thread_dict = process_metric_thread_input(thread_dict)
    print(f"thread_dict = \n{thread_dict}")
    
    # minimal fastener input dictionary:
    input_dict = {
        'type': 'Fastener',
        'name': 'fastener_test_input_dict',
        'material': material_dict,
        'thread': thread_dict,
        'Do_head': 8.5,
        'Do_shank': 5.0,
        'L_shank': 10.0,
        'L_thread': 10.0,
    }
    
    # test fastener processor:
    output_dict = process_fastener_input(input_dict)
    print(output_dict)
    
    # test accessing data:
    thread_pitch = output_dict['thread']['pitch']
    print(f"thread pitch = {thread_pitch}")


if __name__ == "__main__":
    main()
    