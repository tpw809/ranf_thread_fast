"""Process input and return validated and completed data.

Mandatory Parameters:

- type: Metric_Thread
- name: descriptor
- basic_major_diameter
- pitch: thread pitch
- beta_rad: thread half angle in radians

Calculated / Optional Parameters:

- H: fundamental triangle height
"""
import json
import numpy as np

import thread_fast.conversion_factors as cf
import thread_fast.threads.iso_724_1993 as iso_724_1993
import thread_fast.threads.asme_b1_13M_2005 as asme_m_thread
import thread_fast.threads.iso_5855_1_1999 as iso_5855_1_1999


def process_metric_thread_input(
        input_dict: dict,
        verbose:bool=False,
    ):
    """Read and modify the input dict to ensure completeness and validity.
    
    Must supply:
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
        print("Running process_metric_thread_input(verbose=True)...")
    
    # check type:
    assert input_dict['type'] == 'Metric_Thread'
    
    # check if this data has already been processed:
    if input_dict.get('processed_bool') == True:
        return input_dict
    
    # check required inputs:
    assert input_dict.get('name') is not None
    assert input_dict['pitch'] > 0.0
    assert input_dict.get('tolerance_grade') is not None
    assert input_dict.get('allowance_class') is not None
    assert input_dict.get('profile') is not None
    
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
    tolerance_grade = input_dict['tolerance_grade']
    allowance_class = input_dict['allowance_class']
    
    if input_dict.get('internal') is None:
        external = input_dict['external']
        internal = not external
    elif input_dict.get('external') is None:
        internal = input_dict['internal']
        external = not internal
    else:
        external = input_dict['external']
        internal = input_dict['internal']
    
    profile = input_dict['profile']
    
    # height of fundamental triangle, H, from ISO 68:
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
    
    # basic pitch diameter, from ISO 724:
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
    if input_dict.get('basic_minor_diameter') is None:
        if verbose:
            print("calculating metric thread basic minor diameter...")
        if profile == 'M':
            if verbose:
                print("M Profile")
            # ISO 724:
            basic_minor_diameter = basic_major_diameter - (5.0 / 4.0) * H
        elif profile == 'MJ':
            if verbose:
                print("MJ Profile")
            # ISO 5855:
            basic_minor_diameter = basic_major_diameter - (9.0 / 8.0) * H
        else:
            raise Exception("incorrect profile argument, M or MJ")
        input_dict['basic_minor_diameter'] = basic_minor_diameter
    else:
        basic_minor_diameter = input_dict['basic_minor_diameter']
        # TODO: validity check...
    
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
    
    ###########################
    # External Thread
    ###########################
    if external is True:
        # threads are external...
        
        # Upper Deviation, External Thread Allowance (Fundamental Deviation):
        if input_dict.get('es') is None:
            if verbose:
                print("calculating external metric thread es...")
            es = asme_m_thread.eq_es(
                P=pitch, 
                allowance_class=allowance_class,
            )
            input_dict['es'] = es
        else:
            es = input_dict['es']
            # TODO: validity check...
        
        # basic minor diameter (design profile) root?:
        if input_dict.get('d3') is None:
            if verbose:
                print("calculating external metric thread d3...")
            d3 = iso_724_1993.eq_d_3(
                d=basic_major_diameter,
                H=H,
                P=pitch,
            )
            input_dict['d3'] = d3
        else:
            d3 = input_dict['d3']
            # TODO: validity check...
        
        print(input_dict['basic_minor_diameter'] == d3)
        print(f"d3 = {d3}")
        print(f"basic_minor_diameter = {input_dict['basic_minor_diameter']}")
        
        # major diameter tolerance:
        if input_dict.get('Td') is None:
            if verbose:
                print("calculating external metric thread Td...")
            Td = asme_m_thread.eq_Td(
                P=pitch,
                tolerance_grade=tolerance_grade,
            )
            input_dict['Td'] = Td
        else:
            Td = input_dict['Td']
            # TODO: validity check...
        
        # pitch diameter tolerance:
        if input_dict.get('Td2') is None:
            if verbose:
                print("calculating external metric thread Td2...")
            Td2 = asme_m_thread.eq_Td2(
                P=pitch,
                d=basic_major_diameter,
                tolerance_grade=tolerance_grade,
            )
            input_dict['Td2'] = Td2
        else:
            Td2 = input_dict['Td2']
            # TODO: validity check...
        
        # maximum major diameter:
        if input_dict.get('d_max') is None:
            if verbose:
                print("calculating external metric thread d_max...")
            d_max = iso_5855_1_1999.eq_d_max(
                d=basic_major_diameter,
                es=es,
            )
            input_dict['d_max'] = d_max
        else:
            d_max = input_dict['d_max']
            # TODO: validity check...
            
        print(f"max_major_diameter = {d_max}")
        input_dict['max_major_diameter'] = d_max
        
        # minimum major diameter:
        if input_dict.get('d_min') is None:
            if verbose:
                print("calculating external metric thread d_min...")
            d_min = iso_5855_1_1999.eq_d_min(
                d_max=d_max,
                T_d=Td,
            )
            input_dict['d_min'] = d_min
        else:
            d_min = input_dict['d_min']
            # TODO: validity check...
        
        print(f"min_major_diameter = {d_min}")
        input_dict['min_major_diameter'] = d_min
        
        # maximum pitch diameter:
        if input_dict.get('d2_max') is None:
            if verbose:
                print("calculating external metric thread d2_max...")
            d2_max = iso_5855_1_1999.eq_d2_max(
                d_max=d_max,
                P=pitch,
            )
            input_dict['d2_max'] = d2_max
        else:
            d2_max = input_dict['d2_max']
            # TODO: validity check...
        
        print(f"max_pitch_diameter = {d2_max}")
        input_dict['max_pitch_diameter'] = d2_max
        
        # minimum pitch diameter:
        if input_dict.get('d2_min') is None:
            if verbose:
                print("calculating external metric thread d2_min...")
            d2_min = iso_5855_1_1999.eq_d2_min(
                d2_max=d2_max,
                T_d2=Td2,
            )
            input_dict['d2_min'] = d2_min
        else:
            d2_min = input_dict['d2_min']
            # TODO: validity check...
        
        print(f"min_pitch_diameter = {d2_min}")
        input_dict['min_pitch_diameter'] = d2_min
        
        # maximum root diameter:
        if input_dict.get('d3_max') is None:
            if verbose:
                print("calculating external metric thread d3_max...")
            d3_max = iso_5855_1_1999.eq_d3_max(
                d2_max=d2_max,
                P=pitch,
                d3=d3,
            )
            input_dict['d3_max'] = d3_max
        else:
            d3_max = input_dict['d3_max']
            # TODO: validity check...
        
        print(f"max_root_diameter = {d3_max}")
        input_dict['max_root_diameter'] = d3_max
        
        # minimum root diameter:
        if input_dict.get('d3_min') is None:
            if verbose:
                print("calculating external metric thread d3_min...")
            d3_min = iso_5855_1_1999.eq_d3_min(
                d2_min=d2_min,
                P=pitch,
            )
            input_dict['d3_min'] = d3_min
        else:
            d3_min = input_dict['d3_min']
            # TODO: validity check...
        
        print(f"min_root_diameter = {d3_min}")
        input_dict['min_root_diameter'] = d3_min
        
        # [mm^2], tensile area (min cross section area of bolt):
        # NASA-TM-106943, equation 4, pg 5
        # used for fastener strength
        if input_dict.get('A_t') is None:
            if verbose:
                print("calculating external metric thread A_t...")
            A_t = (np.pi/4.0) * (basic_major_diameter - 0.9743*pitch)**2
            input_dict['A_t'] = A_t
        else:
            A_t = input_dict['A_t']
            # TODO: validity check...

        print(f"min_tensile_area = {A_t}")

        # [mm^2], mean area of threads:
        # used for fastener stiffness estimate
        if input_dict.get('A_mean') is None:
            if verbose:
                print("calculating external metric thread A_mean...")
            A_mean = np.pi * r_m**2
            input_dict['A_mean'] = A_mean
        else:
            A_mean = input_dict['A_mean']
            # TODO: validity check...
    
    ###########################
    # Internal Thread
    ###########################
    else:
        # threads are internal...
        
        # Lower Deviation, Internal Thread Allowance (Fundamental Deviation)
        if input_dict.get('EI') is None:
            if verbose:
                print("calculating internal metric thread EI...")
            EI = asme_m_thread.eq_EI(
                P=pitch, 
                allowance_class=allowance_class,
            )
            input_dict['EI'] = EI
        else:
            EI = input_dict['EI']
            # TODO: validity check...
        
        # D_min = minimum major diameter:
        if input_dict.get('D_min') is None:
            if verbose:
                print("calculating internal metric thread D_min...")
            D_min = basic_major_diameter + EI
            input_dict['D_min'] = D_min
        else:
            D_min = input_dict['D_min']
            # TODO: validity check...
        
        print(f"min_major_diameter = {D_min}")
        input_dict['min_major_diameter'] = D_min
        
        # TD1 = minor diameter tolerance:
        if input_dict.get('TD1') is None:
            if verbose:
                print("calculating internal metric thread TD1...")
            TD1 = asme_m_thread.eq_TD1(
                P=pitch,
                tolerance_grade=tolerance_grade,
            )
            input_dict['TD1'] = TD1
        else:
            TD1 = input_dict['TD1']
            # TODO: validity check...
        
        # TD2 = pitch diameter tolerance:
        if input_dict.get('TD2') is None:
            if verbose:
                print("calculating internal metric thread TD2...")
            TD2 = asme_m_thread.eq_TD2(
                P=pitch,
                d=basic_major_diameter,
                tolerance_grade=tolerance_grade,
            )
            input_dict['TD2'] = TD2
        else:
            TD2 = input_dict['TD2']
            # TODO: validity check...
        
        # D3_max = maximum diameter to root:
        # D3_max = iso_5855_1_1999.eq_D3_max(
        #     D=basic_major_diameter,
        #     P=pitch,
        #     EI=EI,
        #     T_D2=TD2,
        # )
        # input_dict['D3_max'] = D3_max
        
        # D1_min = minimum minor diameter:
        if input_dict.get('D1_min') is None:
            if verbose:
                print("calculating internal metric thread D1_min...")
            D1_min = iso_5855_1_1999.eq_D1_min(
                D=basic_major_diameter,
                P=pitch,
                EI=EI,
            )
            input_dict['D1_min'] = D1_min
        else:
            D1_min = input_dict['D1_min']
            # TODO: validity check...
        
        print(f"min_minor_diameter = {D1_min}")
        input_dict['min_minor_diameter'] = D1_min
        
        # D1_max = maximum minor diameter:
        if input_dict.get('D1_max') is None:
            if verbose:
                print("calculating internal metric thread D1_max...")
            D1_max = iso_5855_1_1999.eq_D1_max(
                D=basic_major_diameter,
                P=pitch,
                EI=EI,
                T_D1=TD1,
            )
            input_dict['D1_max'] = D1_max
        else:
            D1_max = input_dict['D1_max']
            # TODO: validity check...
        
        print(f"max_minor_diameter = {D1_max}")
        input_dict['max_minor_diameter'] = D1_max
        
        # D2_min = minimum pitch diameter:
        if input_dict.get('D2_min') is None:
            if verbose:
                print("calculating internal metric thread D2_min...")
            D2_min = iso_5855_1_1999.eq_D2_min(
                D=basic_major_diameter,
                P=pitch,
                EI=EI,
            )
            input_dict['D2_min'] = D2_min
        else:
            D2_min = input_dict['D2_min']
            # TODO: validity check...
        
        print(f"min_pitch_diameter = {D2_min}")
        input_dict['min_pitch_diameter'] = D2_min
        
        # check:
        # print(f"D2_min = {D2_min}")
        # D2_min = basic_pitch_diameter + EI
        # print(f"D2_min = {D2_min}")
        
        # D2_max = maximum pitch diameter:
        if input_dict.get('D2_max') is None:
            if verbose:
                print("calculating internal metric thread D2_max...")
            D2_max = iso_5855_1_1999.eq_D2_max(
                D=basic_major_diameter,
                P=pitch,
                EI=EI,
                T_D2=TD2,
            )
            input_dict['D2_max'] = D2_max
        else:
            D2_max = input_dict['D2_max']
            # TODO: validity check...
        
        print(f"max_pitch_diameter = {D2_max}")
        input_dict['max_pitch_diameter'] = D2_max
        
        # check:
        # print(f"D2_max = {D2_max}")
        # D2_max = basic_pitch_diameter + TD2 + EI
        # print(f"D2_max = {D2_max}")
    
    # add 'processed' tag:
    input_dict['processed_bool'] = True
    
    return input_dict


def main() -> None:
    
    thread_dict = {
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
    print(f"\nthread_dict: \n")
    print(json.dumps(thread_dict, indent=4))
    
    output_dict = process_metric_thread_input(thread_dict, verbose=True)
    print(f"output_dict: \n")
    print(json.dumps(output_dict, indent=4))
    
    output_dict = process_metric_thread_input(output_dict, verbose=True)
    print(f"output_dict: \n")
    print(json.dumps(output_dict, indent=4))
    
    
    input_dict = {
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
    print(f"input_dict: \n")
    print(json.dumps(input_dict, indent=4))
    
    output_dict = process_metric_thread_input(input_dict, verbose=True)
    print(f"output_dict: \n")
    print(json.dumps(output_dict, indent=4))
    
    output_dict = process_metric_thread_input(output_dict, verbose=True)
    print(f"output_dict: \n")
    print(json.dumps(output_dict, indent=4))
    

if __name__ == "__main__":
    main()
    