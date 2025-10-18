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
from thread_fast.kubler_bulten_nut_factor import kubler_bulten_nut_factor
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
    
    assert input_dict.get('name') is not None
    
    # assert 'fastener' in input_dict
    assert input_dict.get('fastener') is not None
    
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
        assert 'threaded_hole' not in input_dict
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
    # assert 'mu_thread' in input_dict
    assert input_dict.get('mu_thread') is not None
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
    
    # Minimum Service Temperature:
    assert 'min_temperature' in input_dict
    T_min = input_dict['min_temperature']
    
    # Maximum Service Temperature:
    assert 'max_temperature' in input_dict
    T_max = input_dict['max_temperature']
    
    # Ambient (Installation) Temperature:
    assert 'ambient_temperature' in input_dict
    T_amb = input_dict['ambient_temperature']
    
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
    else:
        assert input_dict['L_e'] > 0.0
        L_e = input_dict['L_e']
    
    print(f"Length of Engagement = {L_e}")
    
    ###############################
    # Joint Stiffness:
    ###############################
    
    # [N/mm], fastener (bolt) stiffness:
    K_b = fastener['stiffness']
    print(f"K_b, bolt stiffness = {K_b}")
    
    
    # joint modulus:
    if input_dict.get('E_j') is None:
    
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
        
        E_j = nasa_tm_106943.eq34mod(
            L_list=L_list,
            E_list=E_list,
        )
        
        input_dict['E_j'] = E_j
    else:
        E_j = input_dict['E_j']
        # TODO: check E_j validity...
    
    
    # [N/mm], estimated clamped parts (joint) stiffness:
    if input_dict.get('K_j') is None:
        print("estimating joint stiffness...")
        K_j_106943 = nasa_tm_106943.eq33(
            E_j=E_j,
            D=fastener['thread']['basic_major_diameter'],
            L=L_total_clamped_parts,
        )
        print(f"K_j_106943 = {K_j_106943}")
        
        # joint stiffness:
        K_j = K_j_106943
        input_dict['K_j'] = K_j
    else:
        K_j = input_dict['K_j']
        # TODO: check K_j validity...
    
    
    ###############################
    # Joint Stiffness Factor, phi:
    ###############################
    
    if input_dict.get('phi') is None:
        print("estimating joint stiffness factor, phi...")
        # NASA-TM-106943 eq 29:
        # NASA-STD-5020B eq 9:
        phi = nasa_std_5020b.eq9(
            k_b=K_b,
            k_c=K_j,
        )
        input_dict['phi'] = phi
    else:
        print("joint stiffness factor, phi provided")
        phi = input_dict['phi']
        assert phi > 0.0
    
    print(f"joint stiffness factor, phi = {phi}")
    
    
    ###############################
    # Load Introduction Factor, n:
    ###############################
    
    # depends on configuration !!!
    # start with configs 1 and 3...
    
    # distance between load planes in clamped parts:
    # used for load introduction factor, n
    
    if input_dict.get('distance_between_load_planes') is None:
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
    else:
        distance_between_load_planes = input_dict['distance_between_load_planes']
        assert 0.0 <= distance_between_load_planes <= L_total_clamped_parts
    
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
    
    if input_dict.get('n') is None:
        # NASA-TM-106943 eq 18, pg 10:
        n = nasa_tm_106943.eq18(
            d=distance_between_load_planes, 
            t=L_total_clamped_parts,
        )
        input_dict['n'] = n
    else:
        assert 0.0 < input_dict['n'] < 1.0
        n = input_dict['n']
    
    print(f"load introduction factor, n = {n}")
    
    
    ###############################
    # Nut Factor, K:
    ###############################
    
    if input_dict.get('nut_factor') is None:
        print("calculating nut factors...")
        
        # what is mean thread diameter for K?
        #TODO: update to be average of ext and int:
        mean_thread_diameter = fastener['thread']['basic_pitch_diameter']
        
        # TODO: change based on nut_torqued:
        
        # head mean diameter for friction:
        #TODO: refine with hole diameter, not thread major d:
        mean_head_diameter = (fastener['Do_head'] + fastener['thread']['basic_major_diameter']) / 2.0
        
        K_kb = kubler_bulten_nut_factor(
            P=fastener['thread']['pitch'], 
            d_2=mean_thread_diameter, 
            mu_t=mu_thread, 
            mu_b=mu_abutment, 
            d_w=mean_head_diameter, 
            d=fastener['thread']['basic_major_diameter'],
        )
        
        K_08307 = nsts_08307a.nut_factor(
            R_t=mean_thread_diameter/2.0,  # mean radius of thread
            R_e=mean_head_diameter/2.0,  # mean head or nut radius
            mu_t_min=mu_thread,
            mu_t_typ=mu_thread, 
            mu_t_max=mu_thread,
            mu_b_min=mu_abutment,
            mu_b_typ=mu_abutment, 
            mu_b_max=mu_abutment,
            alpha=fastener['thread']['psi_rad'], 
            beta=fastener['thread']['beta_rad'], # thread half angle
            D=fastener['thread']['basic_major_diameter'],
        )[1]
        
        # nut factor: NASA-TM-106943 eq 2:
        K_106943 = nasa_tm_106943.eq2(
            D_p=mean_thread_diameter, 
            D=fastener['thread']['basic_major_diameter'], 
            psi=fastener['thread']['psi_rad'], 
            alpha=fastener['thread']['beta_rad'], # thread half angle
            mu=mu_thread, 
            mu_c=mu_abutment,
        )
        
        print(f"K_kb = {K_kb}")
        print(f"K_08307 = {K_08307}")
        print(f"K_106943 = {K_106943}")
        
        K_min = np.min([
            K_kb, 
            K_08307, 
            K_106943,
        ])
        
        K_max = np.max([
            K_kb, 
            K_08307, 
            K_106943,
        ])
        
        # nominal nut factor = mean of min and max:
        K_nom = (K_min + K_max) / 2.0
        
    else:
        # provided as [K_min, K_nom, K_max]
        K = input_dict['nut_factor'] 
        K_min = np.min(K)
        K_max = np.max(K)
        K_nom = K[1]
    
    
    print(f"K_min = {K_min}")
    print(f"K_nom = {K_nom}")
    print(f"K_max = {K_max}")
    
    
    
    
    ###############################
    # Applied Installation Torque:
    ###############################
    
    # TODO: change based on torque_override:
    
    # target 0.65 tensile yield stress / strength 
    # NASA-TM-106943 eq 3:
    # TODO: is there a 5020 equation?
    T_applied_nom = nasa_tm_106943.eq3(
        D=fastener['thread']['basic_major_diameter'],  # major diameter
        K=K_nom,  # nut factor
        A_t=fastener['thread']['A_t'],  # A_t = tensile area
        F_ty=fastener['material']['Sty'],  # F_ty = material tensile yield strength
        preload_stress_ratio=preload_stress_ratio,
    )
    print(f"T_applied_nom = {T_applied_nom}")
    
    T_applied_min = nasa_tm_106943.eq3(
        D=fastener['thread']['basic_major_diameter'],  # major diameter
        K=K_min,  # nut factor
        A_t=fastener['thread']['A_t'],  # A_t = tensile area
        F_ty=fastener['material']['Sty'],  # F_ty = material tensile yield strength
        preload_stress_ratio=preload_stress_ratio,
    )
    print(f"T_applied_min = {T_applied_min}")
    
    T_applied_max = nasa_tm_106943.eq3(
        D=fastener['thread']['basic_major_diameter'],  # major diameter
        K=K_max,  # nut factor
        A_t=fastener['thread']['A_t'],  # A_t = tensile area
        F_ty=fastener['material']['Sty'],  # F_ty = material tensile yield strength
        preload_stress_ratio=preload_stress_ratio,
    )
    print(f"T_applied_max = {T_applied_max}")
    
    ###############################
    # Predicted Initial Preload: 
    ###############################
    
    # P_i: initial predicted nominal preload:
    # NASA-STD-5020B, eq 24:
    P_i_nom = nasa_std_5020b.eq24(
        T=T_applied_nom,
        K_nom=K_nom,
        D=fastener['thread']['basic_major_diameter'],
    )
    print(f"P_i_nom = {P_i_nom}")
    
    P_i_min = nasa_std_5020b.eq4(
        c_min=lower_preload_tolerance_factor,
        gamma=preload_uncertainty_factor,
        P_pi_nom=P_i_nom,
    )
    print(f"P_i_min = {P_i_min}")
    
    P_i_max = nasa_std_5020b.eq3(
        c_max=upper_preload_tolerance_factor,
        gamma=preload_uncertainty_factor,
        P_pi_nom=P_i_nom,
    )
    print(f"P_i_max = {P_i_max}")
    
    # delta_b = 
    
    # delta_j = 
    
    
    ###############################
    # axial bolt load due to thermal effects: 
    ###############################
    
    # eq 10
    L = L_total_clamped_parts

    # TODO: fix joint coefficient of thermal expansion !!!
    # need a combined joint CTE !!!
    # alpha_j = self.clamped_parts[1].material.cte_mm_mm_C
    
    # NASA-TM-106943 eq10:
    P_th_min = nasa_tm_106943.eq10(
        K_b=K_b, 
        K_j=K_j, 
        L=L_total_clamped_parts, 
        delta_T=delta_T_min, 
        alpha_j=clamped_parts[1]['material']['cte'], 
        alpha_b=fastener['material']['cte'],
    )
    
    # NASA-TM-106943 eq10:
    P_th_max = nasa_tm_106943.eq10(
        K_b=K_b, 
        K_j=K_j, 
        L=L_total_clamped_parts, 
        delta_T=delta_T_max, 
        alpha_j=clamped_parts[1]['material']['cte'], 
        alpha_b=fastener['material']['cte'],
    )
    
    # which is worst case? min or max?
    # self.P_th = np.min([self.P_th_min, self.P_th_max])
    # print(f"P_th = {self.P_th} [N]")
    
    P_th_min_temp = np.min([P_th_min, P_th_max])
    P_th_max = np.max([P_th_min, P_th_max])
    P_th_min = P_th_min_temp
    
    print(f"P_th_min = {P_th_min} [N]")
    print(f"P_th_max = {P_th_max} [N]")
    
    
    #################################
    # Final Predicted Preload
    #################################
    
    # includes changes due to thermal conditions
    
    if input_dict.get('P_max') is None:
        print("calculating max preload...")
    
        # NASA-STD-5020B eq1:
        P_max = nasa_std_5020b.eq1(
            P_pi_max=P_i_max,
            P_deltat_max=P_th_max,
        )
        
        input_dict['P_max'] = P_max
    
    else:
        P_max = input_dict['P_max']
    
    if input_dict.get('P_min') is None:
        print("calculating min preload...")
    
        # NASA-STD-5020B eq2mod:
        # P_min = P_i_min - preload_loss_due_to_material_creep
        P_min = nasa_std_5020b.eq2mod(
            P_pi_min=P_i_min,
            P_deltat_min=P_th_min,
            P_pc=preload_loss_due_to_material_creep,
            relaxation_ratio=relaxation_ratio,
        )
        
        input_dict['P_min'] = P_min
    
    else:
        P_min = input_dict['P_min']
    
    assert P_min >= 0.0, 'min preload must be >= 0'
    assert P_max >= 0.0, 'max preload must be >= 0'
    assert P_min <= P_max, "error in final preload prediction"
    
    print(f"P_min = {P_min} [N]")
    print(f"P_max = {P_max} [N]")
    
    
    ######################################
    # Margins
    ######################################
    
    ######################################
    # Tension only fastener strength:
    ######################################
    # yield axial load: NASA-STD-5020B eq16:
    
    # bolt load (ultimate):
    if input_dict.get('P_b_u') is None:
        print("calculating ultimate bolt load...")
        P_b_u = nsts_08307a.bolt_axial_load_for_strength(
            PLD_max=P_max, 
            n=n, 
            phi=phi, 
            SF=SF_u, 
            P=applied_tensile_load,
        )
        input_dict['P_b_u'] = P_b_u
    else:
        P_b_u = input_dict['P_b_u']
    
    
    # NSTS08307A: bolt_tensile_margin:
    
    MS_tu_nsts08307a = nsts_08307a.bolt_tensile_margin(
        PA_t=fastener['P_tu_allow'], 
        SF=SF_u, 
        P=applied_tensile_load, 
        P_b=P_b_u,
    )
    print(f"MS_tu_nsts08307a = {MS_tu_nsts08307a}")
    
    # TODO: override for P_tu_allow, P_ty_allow: implemented at fastener level...
    
    # applied tensile load that causes the bolt load to exceed the allowable ultimate tensile load
    
    P_prime_tu = nasa_std_5020b.eq10(
        n=n, 
        phi=phi, 
        P_tu_allow=fastener['P_tu_allow'], 
        P_p_max=P_max,
    )
    print(f"P_prime_tu = {P_prime_tu}")
    
    P_prime_sep = nasa_std_5020b.eq11(
        P_p_max=P_max, 
        n=n, 
        phi=phi,
    )
    print(f"P_prime_sep = {P_prime_sep}")
    
    # ultimate tensile load: NASA-STD-5020B eq6:
    # ultimate tensile margin of safety:
    MS_tu_5020b_crit1 = nasa_std_5020b.eq6(
        P_tu_allow=fastener['P_tu_allow'], 
        FS_u=SF_u, 
        P_tL=applied_tensile_load,
        FF=FF,  # fitting factor
    )
    print(f"MS_tu_5020b_crit1 = {MS_tu_5020b_crit1}")
    
    # ultimate tensile load: NASA-STD-5020B eq7:
    # ultimate tensile margin of safety:
    MS_tu_5020b_crit2 = nasa_std_5020b.eq7(
        P_prime_tu=P_prime_tu, 
        FS_u=SF_u, 
        P_tL=applied_tensile_load,
        FF=FF,  # fitting factor
    )
    print(f"MS_tu_5020b = {MS_tu_5020b_crit2}")
    
    # yield axial load: NASA-STD-5020B eq15:
    # yield tensile margin of safety:
    MS_ty_5020b_crit1 = nasa_std_5020b.eq15(
        P_ty_allow=fastener['P_ty_allow'], 
        FS_y=SF_y, 
        P_tL=applied_tensile_load,
        FF=FF,  # fitting factor
    )
    print(f"MS_ty_5020b = {MS_ty_5020b_crit1}")
    
    P_prime_ty = nasa_std_5020b.eq17(
        n=n, 
        phi=phi, 
        P_ty_allow=fastener['P_ty_allow'], 
        P_p_max=P_max,
    )
    print(f"P_prime_ty = {P_prime_ty}")
    
    MS_ty_5020b_crit2 = nasa_std_5020b.eq16(
        P_prime_ty=P_prime_ty, 
        FS_y=SF_y, 
        P_tL=applied_tensile_load,
        FF=FF,  # fitting factor
    )
    print(f"MS_ty_5020b = {MS_ty_5020b_crit2}")
    
    ######################################
    # Shear only fastener strength:
    ######################################
    # ultimate shear load: nasa_std_5020b eq14:
    # NASA-TM-106943 eq54:
    # NSTS08307A shear_margin:
    
    # NASA-TM-106943, pg 16: F_sy = 0.577 * F_ty
    
    # TODO: fix:
    # depends on whether threads are in shear plane:
    
    # NASA-STD-5020B eq 12:
    # threads NOT in shear plane:
    P_su_allow_1 = fastener['P_su_allow_1']
    print("threads NOT in shear plane:")
    print(f"fastener P_su_allow_1 = {P_su_allow_1}")
    
    # NASA-STD-5020B eq 13:
    # threads in shear plane:
    P_su_allow_2 = fastener['P_su_allow_2']
    print("threads in shear plane:")
    print(f"fastener P_su_allow_2 = {P_su_allow_2}")
    
    # ultimate fastener shear margin of safety:
    
    MS_su_5020b_1 = nasa_std_5020b.eq14(
        P_su_allow=P_su_allow_1, 
        FS_u=SF_u, 
        P_sL=applied_shear_load, 
        FF=FF,  # fitting factor
    )
    print(f"MS_su_5020b_1 = {MS_su_5020b_1}")
    
    
    MS_su_5020b_2 = nasa_std_5020b.eq14(
        P_su_allow=P_su_allow_2, 
        FS_u=SF_u, 
        P_sL=applied_shear_load, 
        FF=FF,  # fitting factor
    )
    print(f"MS_su_5020b_2 = {MS_su_5020b_2}")
    
    
    
    ######################################
    # Bending Only Margin:
    ######################################
    # NSTS08307A bending_margin:
    # NSTS08307A bolt_bending_margin:
    
    # Tension and shear fastener strength:
    # NASA-TM-106943 eq59:
    
    ######################################
    # Tension, shear, bending fastener strength:
    ######################################
    # NSTS08307A combined_load_margin: (deprecated)
    # NASA-TM-106943 eq62: (deprecated)
    # ultimate combined load: NASA-STD-5020B eq20mod:
    # ultimate combined load: NASA-STD-5020B eq21mod:
    # ultimate combined load: NASA-STD-5020B eq22mod:
    # ultimate combined load: NASA-STD-5020B eq23mod:
    
    
    
    ######################################
    # Joint Separation Margin:
    ######################################
    
    # NASA-TM-106943, eq68:
    
    P_sep_106943 = nasa_tm_106943.eq67(
        n=n, 
        phi=phi, 
        P_et=applied_tensile_load,
    )
    input_dict['P_sep_106943'] = P_sep_106943
    
    
    MS_sep_106943 = nasa_tm_106943.eq68(
        P_0_min=P_min, 
        P_sep=P_sep_106943,
        SF=SF_sep,
    )
    print(f"MS_sep_106943 = {MS_sep_106943}")
    
    
    # NASA-STD-5020B, eq19:
    MS_sep_5020b = nasa_std_5020b.eq19(
        P_p_min=P_min, 
        SF_sep=SF_sep, 
        P_tL=applied_tensile_load,
        FF=FF, 
    )
    print(f"MS_sep_5020b = {MS_sep_5020b}")
    
    # NSTS08307A, joint_separation_margin_of_safety:
    P_sep_nsts08307a = nsts_08307a.joint_separation_load(
        P=applied_tensile_load, 
        SF_sep=SF_sep,
    )
    
    MS_sep_nsts08307a = nsts_08307a.joint_separation_margin_of_safety(
        PLD_min=P_min, 
        n=n, 
        phi=phi,
        P_sep=P_sep_nsts08307a,
    )
    print(f"MS_sep_nsts08307a = {MS_sep_nsts08307a}")
    
    
    ######################################
    # Joint slip:
    ######################################
    
    # NASA-STD-5020B eq86:
    
    
    ######################################
    # Shear Pull Out of Threads:
    ######################################
    
    # TODO: rederive the thread shear area...
    
    # external threads pull out shear area:
    A_se = nsts_08307a.external_thread_shear_area(
        L_e=L_e,
        K_i_max=nut['thread']['D1_max'],  # max minor diam of int threads
        n_0=None,
        TK_i=nut['thread']['TD1'],  # tol on minor diam of int threads
        TE_e=fastener['thread']['Td2'],  # tol on pitch diam of ext threads
        G_e=fastener['thread']['es'],  # allowance on ext threads
        pitch=fastener['thread']['pitch'],
    )
    print(f"A_se = {A_se}")
    
    # TODO: fix A_se
    A_se = 1.0
    
    
    # internal threads pull out shear area:
    A_si = nsts_08307a.internal_thread_shear_area(
        L_e=L_e,
        D_e_min=fastener['thread']['d_min'],  # min major diam of ext threads
        n_0=None,
        TD_e=fastener['thread']['Td'],  # tol on major diam ext threads
        TE_i=nut['thread']['TD2'],  # tol on pitch diam int threads
        G_e=fastener['thread']['es'],  # allowance on ext threads
        pitch=fastener['thread']['pitch'],
    )
    print(f"A_si = {A_si}")
    
    # TODO: fix A_si
    A_si = 1.0
    
    
    # NSTS08307A: thread_shear_pull_out_margin (ultimate)
    # for fastener external threads:
    MS_thread_shear_pull_out_u_08307a = nsts_08307a.thread_shear_pull_out_margin(
        PA_s=fastener.PA_s_08307a(A_se), 
        SF=SF_u, 
        P=applied_tensile_load, 
        P_b=P_b_u,
    )
    print(f"MS_thread_shear_pull_out_u_08307a = {MS_thread_shear_pull_out_u_08307a}")
    
    # for nut internal threads:
    MS_thread_shear_pull_out_u_08307a = nsts_08307a.thread_shear_pull_out_margin(
        PA_s=nut.PA_s_08307a(A_si), 
        SF=SF_u, 
        P=applied_tensile_load, 
        P_b=P_b_u,
    )
    print(f"MS_thread_shear_pull_out_u_08307a = {MS_thread_shear_pull_out_u_08307a}")
    
    input_dict['MS_thread_shear_pull_out_u_08307a'] = MS_thread_shear_pull_out_u_08307a
    
    
    # Bolt Thread Shear:
    
    
    
    # NASA-TM-106943 eq65:
    A_s_min = nasa_tm_106943.eq63(
        L_e=L_e, 
        D_minor_int=nut['thread']['D1_min'],  # D1 min or max?
    )
    
    A_s_max = nasa_tm_106943.eq63(
        L_e=L_e, 
        D_minor_int=nut['thread']['D1_max'],  # D1 min or max?
    )
    
    P_ult_thread_shear = nasa_tm_106943.eq64(
        F_su=nut['material']['Ssu'], 
        A_s=A_s,
    )
    print(f"P_ult_thread_shear = {P_ult_thread_shear}")
    
    input_dict['P_ult_thread_shear'] = P_ult_thread_shear
    
    
    
    MS_thread_shear_106943 = nasa_tm_106943.eq65(
        P_ult=P_ult_thread_shear, 
        P_b=P_b_u,
    )
    print(f"MS_thread_shear_106943 = {MS_thread_shear_106943}")
    
    input_dict['MS_thread_shear_106943'] = MS_thread_shear_106943
    
    
    # Threaded Insert Thread:
    # NASA-TM-106943 eq77:
    
    # Nut Strength:
    # NASA-TM-106943 eq81:
    
    # Part Shear Tear Out:
    # NASA-TM-106943 eq71:
    
    # Bolt Bearing (Shank Shear Bearing):
    # NASA-TM-106943 eq74:
    
    # Bearing under Bolt Head or Nut:
    # NASA-TM-106943 eq75:
    
    
    
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
    