"""
Use functional programming instead of object oriented...

focus on web-app interface...

Goal: user can input as little or as much as they want...

Also try going unitless...

Parameters:

- name: descriptor


"""
import numpy as np
import thread_fast.conversion_factors as cf
import thread_fast.threads.iso_724_1993 as iso_724_1993
import thread_fast.threads.asme_b1_13M_2005 as asme_m_thread
import thread_fast.threads.iso_5855_1_1999 as iso_5855_1_1999


def process_metric_thread_input(input_dict: dict):
    """
    modify the input dict to ensure completeness
    
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
    # check required inputs:
    
    assert input_dict['type'] == 'Metric_Thread'
    
    assert 'name' in input_dict
    
    assert input_dict['pitch'] > 0.0
    
    assert 'tolerance_grade' in input_dict
    
    assert 'allowance_class' in input_dict
    
    assert 'external' in input_dict
    
    assert 'internal' in input_dict
    
    assert input_dict['external'] != input_dict['internal']
    
    assert 'profile' in input_dict
    
    
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
    external = input_dict['external']
    internal = input_dict['internal']
    profile = input_dict['profile']
    
    # height of fundamental triangle:
    # from: iso 68
    H = (np.sqrt(3.0) / 2.0) * pitch
    input_dict['H'] = H
    
    # length of engagement:
    LE_min, LE_max = asme_m_thread.eq_LE(
        P=pitch,
        d=basic_major_diameter,
    )
    input_dict['LE_min'] = LE_min
    input_dict['LE_max'] = LE_max
    
    # basic pitch diameter:
    # ISO 724:
    basic_pitch_diameter = basic_major_diameter - (3.0 / 4.0) * H
    input_dict['basic_pitch_diameter'] = basic_pitch_diameter
    
    # basic minor diameter:
    # depends on M vs MJ !!!
    
    if profile == 'M':
        # ISO 724:
        basic_minor_diameter = basic_major_diameter - (5.0 / 4.0) * H
    elif profile == 'MJ':
        # ISO 5855:
        basic_minor_diameter = basic_major_diameter - (9.0 / 8.0) * H
    else:
        raise Exception("incorrect profile argument, M or MJ")
    input_dict['basic_minor_diameter'] = basic_minor_diameter
    
    # mean thread radius (half of basic pitch diameter)
    r_m = basic_pitch_diameter / 2.0
    input_dict['r_m'] = r_m
    
    # thread lead angle, radians:
    psi_rad = np.arctan(pitch / (2.0 * np.pi * r_m))
    input_dict['psi_rad'] = psi_rad
    
    
    if external is True:
        # threads are external...
        
        # Upper Deviation, External Thread Allowance (Fundamental Deviation)
        es = asme_m_thread.eq_es(
            P=pitch, 
            allowance_class=allowance_class,
        )
        input_dict['es'] = es
        
        # basic minor diameter (design profile) root?:
        d3 = iso_724_1993.eq_d_3(
            d=basic_major_diameter,
            H=H,
            P=pitch,
        )
        input_dict['d3'] = d3
        
        # major diameter tolerance:
        Td = asme_m_thread.eq_Td(
            P=pitch,
            tolerance_grade=tolerance_grade,
        )
        input_dict['Td'] = Td
        
        # pitch diameter tolerance:
        Td2 = asme_m_thread.eq_Td2(
            P=pitch,
            d=basic_major_diameter,
            tolerance_grade=tolerance_grade,
        )
        input_dict['Td2'] = Td2
        
        # maximum major diameter:
        d_max = iso_5855_1_1999.eq_d_max(
            d=basic_major_diameter,
            es=es,
        )
        input_dict['d_max'] = d_max
        
        # minimum major diameter:
        d_min = iso_5855_1_1999.eq_d_min(
            d_max=d_max,
            T_d=Td,
        )
        input_dict['d_min'] = d_min
        
        # maximum pitch diameter:
        d2_max = iso_5855_1_1999.eq_d2_max(
            d_max=d_max,
            P=pitch,
        )
        
        # minimum pitch diameter:
        d2_min = iso_5855_1_1999.eq_d2_min(
            d2_max=d2_max,
            T_d2=Td2,
        )
        input_dict['d2_min'] = d2_min
        
        # maximum root diameter:
        d3_max = iso_5855_1_1999.eq_d3_max(
            d2_max=d2_max,
            P=pitch,
            d3=d3,
        )
        input_dict['d3_max'] = d3_max
        
        # minimum root diameter:
        d3_min = iso_5855_1_1999.eq_d3_min(
            d2_min=d2_min,
            P=pitch,
        )
        input_dict['d3_min'] = d3_min
        
        # [mm^2], tensile area (min cross section area of bolt):
        # NASA-TM-106943, equation 4, pg 5
        # used for fastener strength
        A_t = (np.pi/4.0) * (basic_major_diameter - 0.9743*pitch)**2
        input_dict['A_t'] = A_t

        # [mm^2], mean area of threads:
        # used for fastener stiffness estimate
        A_mean = np.pi * r_m**2
        input_dict['A_mean'] = A_mean
    
    else:
        # threads are internal...
        
        # Lower Deviation, Internal Thread Allowance (Fundamental Deviation)
        EI = asme_m_thread.eq_EI(
            P=pitch, 
            allowance_class=allowance_class,
        )
        input_dict['EI'] = EI
        
        # D_min = minimum major diameter:
        D_min = basic_major_diameter + EI
        input_dict['D_min'] = D_min
        
        # TD1 = minor diameter tolerance:
        TD1 = asme_m_thread.eq_TD1(
            P=pitch,
            tolerance_grade=tolerance_grade,
        )
        input_dict['TD1'] = TD1
        
        # TD2 = pitch diameter tolerance:
        TD2 = asme_m_thread.eq_TD2(
            P=pitch,
            d=basic_major_diameter,
            tolerance_grade=tolerance_grade,
        )
        input_dict['TD2'] = TD2
        
        # D3_max = maximum diameter to root:
        # D3_max = iso_5855_1_1999.eq_D3_max(
        #     D=basic_major_diameter,
        #     P=pitch,
        #     EI=EI,
        #     T_D2=TD2,
        # )
        # input_dict['D3_max'] = D3_max
        
        # D1_min = minimum minor diameter:
        D1_min = iso_5855_1_1999.eq_D1_min(
            D=basic_major_diameter,
            P=pitch,
            EI=EI,
        )
        input_dict['D1_min'] = D1_min
        
        # D1_max = maximum minor diameter:
        D1_max = iso_5855_1_1999.eq_D1_max(
            D=basic_major_diameter,
            P=pitch,
            EI=EI,
            T_D1=TD1,
        )
        input_dict['D1_max'] = D1_max
        
        # D2_min = minimum pitch diameter:
        D2_min = iso_5855_1_1999.eq_D2_min(
            D=basic_major_diameter,
            P=pitch,
            EI=EI,
        )
        input_dict['D2_min'] = D2_min
        
        #check:
        print(f"D2_min = {D2_min}")
        D2_min = basic_pitch_diameter + EI
        print(f"D2_min = {D2_min}")
        
        # D2_max = maximum pitch diameter:
        D2_max = iso_5855_1_1999.eq_D2_max(
            D=basic_major_diameter,
            P=pitch,
            EI=EI,
            T_D2=TD2,
        )
        input_dict['D2_max'] = D2_max
        
        # check:
        print(f"D2_max = {D2_max}")
        D2_max = basic_pitch_diameter + TD2 + EI
        print(f"D2_max = {D2_max}")
    
    
    return input_dict


def main() -> None:
    
    input_dict = {
        'type': 'Metric_Thread',
        'name': 'test_input_dict',
        'basic_major_diameter': 6.0,
        'pitch': 1.0,
        'beta_deg': 30.0,
        'external': True,
        'internal': False,
        'profile': 'MJ',
        'tolerance_grade': 6,
        'allowance_class': 'h',
    }
    
    output_dict = process_metric_thread_input(input_dict)
    print(output_dict)
    
    
    input_dict = {
        'type': 'Metric_Thread',
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
    
    output_dict = process_metric_thread_input(input_dict)
    print(output_dict)
    
    

if __name__ == "__main__":
    main()
    