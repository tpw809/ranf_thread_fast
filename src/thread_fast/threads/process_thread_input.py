"""Process input and return validated and completed data.

Mandatory Parameters:

- type: Metric_Thread
- name: descriptor
- basic_major_diameter
- pitch: thread pitch
- beta_rad: thread half angle in radians

Calculated / Optional Parameters:

- H: fundamental triangle height

Thread data required for analysis:
- minimum major diameter (mm or in)
- basic_major_diameter (mm or in)
- maximum major diameter (mm or in)
- pitch: thread pitch (mm or in)
- beta_rad: thread half angle (radians)
- external or internal thread? (bool)
- height of fundamental triangle, H (mm or in)
- r_m: mean radius of thread (mm or in)
- psi_rad: thread lead angle (radians)

- basic_minor_diameter (mm or in)

- minimum pitch diameter (mm or in)
- basic_pitch_diameter (mm or in)
- maximum pitch diameter (mm or in)
- LE_min: minimum length of engagement (mm or in)
- LE_max: maximum length of engagement (mm or in)
- A_mean: mean area for stiffness estimate
- A_t: tensile area in threaded region

A_se = external thread shear pull out area:
D1_max = max minor diameter of internal threads
TD1 = tolerance on minor diameter of internal thread
Td2 = tol on pitch diameter of ext threads
es = allowance on etx threads

A_si = internal threads pull out shear area
d_min = min major diameter of ext threads
"""
import json
import numpy as np

import thread_fast.conversion_factors as cf
# import thread_fast.threads.iso_724_1993 as iso_724_1993
import thread_fast.threads.asme_b1_13M_2005 as asme_m_thread
# import thread_fast.threads.iso_5855_1_1999 as iso_5855_1_1999
from thread_fast.threads.process_metric_thread import process_metric_thread_input


def process_thread_input(input_dict: dict, verbose:bool=False):
    """Read and modify the input dict to ensure completeness and validity.
    
    Must supply:
    - type: 'Thread'
    - units: 'english' or 'metric'
    - name: descriptor
    - basic_major_diameter
    - pitch: thread pitch [mm/thread] or [in/thread]
    - beta_rad: Thread half angle in radians.
    - beta_deg (float): Thread half angle in degrees.
    - tolerance_grade (int): Tolerance grade indicator.
    - allowance_class (str): Allowance class indicator.
    - external (bool): Is this an External thread?
    - internal (bool): Is this an Internal thread?
    - profile (str): Thread profile (M or MJ).
    
    Optional:
    - r_m: mean radius of thread
    - psi_rad: thread lead angle, radians
    - basic_minor_diameter
    - basic_pitch_diameter
    - LE_min: minimum length of engagement
    - LE_max: maximum length of engagement
    """
    if verbose:
        print("Running process_thread_input(verbose=True)...")
    
    # check type:
    assert input_dict['type'] == 'Thread' or 'Metric_Thread'
    
    if input_dict['type'] == 'Metric_Thread':
        input_dict = process_metric_thread_input(input_dict, verbose)
        input_dict['type'] = 'Thread'
    
    # check if this data has already been processed:
    if input_dict.get('processed_bool') == True:
        return input_dict
    
    # check required inputs:
    assert input_dict.get('name') is not None
    assert input_dict['pitch'] > 0.0
    
    # assert 'external' in input_dict
    if input_dict.get('internal') is None:
        assert input_dict.get('external') is not None
    
    # assert 'internal' in input_dict
    if input_dict.get('external') is None:
        assert input_dict.get('internal') is not None
    
    # assert input_dict['external'] != input_dict['internal']
    
    # check / fill parameter:
    if 'beta_rad' in input_dict:
        assert input_dict['beta_rad'] >= 0.0
        input_dict['beta_deg'] = cf.rad_to_deg * input_dict['beta_rad']
    else:
        input_dict['beta_rad'] = cf.deg_to_rad * input_dict['beta_deg']
    
    # Make calculations:
    basic_major_diameter = input_dict['basic_major_diameter']
    beta_rad = input_dict['beta_rad']
    pitch = input_dict['pitch']
    
    if input_dict.get('internal') is None:
        external = input_dict['external']
        internal = not external
    elif input_dict.get('external') is None:
        internal = input_dict['internal']
        external = not internal
    else:
        external = input_dict['external']
        internal = input_dict['internal']
    
    # height of fundamental triangle, H:
    # from: iso 68
    if input_dict.get('H') is None:
        if verbose:
            print("calculating metric thread triangle height, H...")
        H = (np.sqrt(3.0) / 2.0) * pitch
        input_dict['H'] = H
    else:
        H = input_dict['H']
        # TODO: validity check...
    
    # length of engagement:
    LE_min, LE_max = asme_m_thread.eq_LE(
        P=pitch,
        d=basic_major_diameter,
    )
    input_dict['LE_min'] = LE_min
    input_dict['LE_max'] = LE_max
    
    # basic pitch diameter:
    # ISO 724:
    if input_dict.get('basic_pitch_diameter') is None:
        if verbose:
            print("calculating metric thread basic pitch diameter...")
        basic_pitch_diameter = basic_major_diameter - (3.0 / 4.0) * H
        input_dict['basic_pitch_diameter'] = basic_pitch_diameter
    else:
        basic_pitch_diameter = input_dict['basic_pitch_diameter']
        # TODO: validity check...
    
    # basic minor diameter:
    # depends on M vs MJ !!!
    # if input_dict.get('basic_minor_diameter') is None:
    #     if verbose:
    #         print("calculating metric thread basic minor diameter...")
    #     if profile == 'M':
    #         print("M Profile")
    #         # ISO 724:
    #         basic_minor_diameter = basic_major_diameter - (5.0 / 4.0) * H
    #     elif profile == 'MJ':
    #         print("MJ Profile")
    #         # ISO 5855:
    #         basic_minor_diameter = basic_major_diameter - (9.0 / 8.0) * H
    #     else:
    #         raise Exception("incorrect profile argument, M or MJ")
    #     input_dict['basic_minor_diameter'] = basic_minor_diameter
    # else:
    #     basic_minor_diameter = input_dict['basic_minor_diameter']
    #     # TODO: validity check...
    
    # mean thread radius (half of basic pitch diameter):
    if input_dict.get('r_m') is None:
        if verbose:
            print("calculating metric thread mean radius, r_m...")
        r_m = basic_pitch_diameter / 2.0
        input_dict['r_m'] = r_m
    else:
        r_m = input_dict['r_m']
    
    # thread lead angle, radians:
    if input_dict.get('psi_rad') is None:
        if verbose:
            print("calculating metric thread lead angle, psi_rad...")
        psi_rad = np.arctan(pitch / (2.0 * np.pi * r_m))
        input_dict['psi_rad'] = psi_rad
    else:
        psi_rad = input_dict['psi_rad']
    
    #########################
    # External Thread:
    #########################
    if external is True:
        # threads are external...
        
        
        
        # basic minor diameter (design profile) root?:
        if input_dict.get('d3') is None:
            pass
        
        # max_major_diameter:
        if input_dict.get('d_max') is None:
            pass
        
        # min_major_diameter:
        if input_dict.get('d_min') is None:
            pass
        
        # max_pitch_diameter:
        if input_dict.get('d2_max') is None:
            pass
        
        # min_pitch_diameter:
        if input_dict.get('d2_min') is None:
            pass
        
        # maximum root diameter:
        if input_dict.get('d3_max') is None:
            pass
        
        # minimum root diameter:
        if input_dict.get('d3_min') is None:
            pass
        
        # [mm^2], tensile area (min cross section area of bolt):
        # NASA-TM-106943, equation 4, pg 5
        # used for fastener strength
        if input_dict.get('A_t') is None:
            print("calculating external metric thread A_t...")
            A_t = (np.pi/4.0) * (basic_major_diameter - 0.9743*pitch)**2
            input_dict['A_t'] = A_t
        else:
            A_t = input_dict['A_t']
            # TODO: validity check...

        # [mm^2], mean area of threads:
        # used for fastener stiffness estimate
        if input_dict.get('A_mean') is None:
            print("calculating external metric thread A_mean...")
            A_mean = np.pi * r_m**2
            input_dict['A_mean'] = A_mean
        else:
            A_mean = input_dict['A_mean']
            # TODO: validity check...
    
    #########################
    # Internal Thread:
    #########################
    else:
        # threads are internal...
        
        # D_min = min_major_diameter:
        if input_dict.get('D_min') is None:
            pass
        
        # D3_max = maximum diameter to root:
        
        # D1_min = min_minor_diameter:
        if input_dict.get('D1_min') is None:
            pass
        
        # D1_max = max_minor_diameter:
        if input_dict.get('D1_max') is None:
            pass
        
        # D2_min = min_pitch_diameter:
        if input_dict.get('D2_min') is None:
            pass
        
        # D2_max = max_pitch_diameter:
        if input_dict.get('D2_max') is None:
            pass
    
    # add 'processed' tag:
    input_dict['processed_bool'] = True
    
    return input_dict


def main() -> None:
    
    input_dict = {
        'type': 'Thread',
        'units': 'metric: N, mm, MPa, C',
        'name': 'test_thread_input_dict',
        'basic_major_diameter': 6.0,
        'pitch': 1.0,
        'beta_deg': 30.0,
        'external': True,
        'internal': False,
    }
    print(f"input_dict: \n")
    print(json.dumps(input_dict, indent=4))
    
    output_dict = process_thread_input(input_dict, verbose=True)
    print(f"output_dict: \n")
    print(json.dumps(output_dict, indent=4))
    
    output_dict = process_thread_input(output_dict, verbose=True)
    print(f"output_dict: \n")
    print(json.dumps(output_dict, indent=4))
    
    ##################################
    # Test External Metric Thread:
    ##################################
    
    input_dict = {
        'type': 'Metric_Thread',
        'units': 'metric: N, mm, MPa, C',
        'name': 'test_input_dict',
        'basic_major_diameter': 6.0,
        'pitch': 1.0,
        'beta_deg': 30.0,  # deg
        'external': True,
        'internal': False,
        'profile': 'MJ',
        'tolerance_grade': 6,
        'allowance_class': 'h',
    }
    print(f"input_dict: \n")
    print(json.dumps(input_dict, indent=4))
    
    output_dict = process_metric_thread_input(input_dict, verbose=True)
    print(f"output_dict: \n")
    print(json.dumps(output_dict, indent=4))
    
    
    ##################################
    # Test Internal Metric Thread:
    ##################################
    
    metric_thread_input_dict = {
        'type': 'Metric_Thread',
        'units': 'metric: N, mm, MPa, C',
        'name': 'test_input_dict',
        'basic_major_diameter': 6.0,
        'pitch': 1.0,
        'beta_deg': 30.0,
        'external': False,
        'internal': True,
        'profile': 'MJ',
        'tolerance_grade': 6,
        'allowance_class': 'H',
    }
    print(f"metric_thread_input_dict: \n")
    print(json.dumps(metric_thread_input_dict, indent=4))
    
    output_dict = process_thread_input(metric_thread_input_dict, verbose=True)
    print(f"output_dict: \n")
    print(json.dumps(output_dict, indent=4))
    
    output_dict = process_thread_input(output_dict, verbose=True)
    print(f"output_dict: \n")
    print(json.dumps(output_dict, indent=4))
    

if __name__ == "__main__":
    main()
    