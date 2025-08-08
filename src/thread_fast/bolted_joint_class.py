"""BoltedJoint class definition.

Timothy P Woodard, June 22, 2025

BoltedJoint contains:

- Fastener
- Washers
- Clamped Parts
- Nut / Insert / Tapped Hole
- External Load
- Temperatures
- Preload
- Design
- Coefficients of Friction
"""
import json
import numpy as np
from pathlib import Path

import thread_fast.nsts_08307a as nsts_08307a
import thread_fast.nasa_tm_106943 as nasa_tm_106943
import thread_fast.nasa_std_5020.nasa_std_5020b as nasa_std_5020b
from thread_fast.kubler_bulten_nut_factor import kubler_bulten_nut_factor
from thread_fast.nut_class import Nut
from thread_fast.material_class import Material
from thread_fast.fastener_class import Fastener
from thread_fast.washer_class import Washer
from thread_fast.clamped_part_class import ClampedPart
from thread_fast.threads.metric_thread_class import MetricThread
from thread_fast.threads.metric_thread_class import ExternalMetricThread
from thread_fast.threads.metric_thread_class import InternalMetricThread
import thread_fast.conversion_factors as cf


class BoltedJoint:
    """BoltedJoint class.
    
    Args:
        name (str): Descriptive name of the bolted joint.
        fastener (Fastener): Fastener in the bolted joint.
        clamped_parts (List): List of clamped parts in the bolted joint.
        nut (Nut): Nut used to thread onto the fastener.
        mu_thread (float): Coefficient of friction between mating threads.
        mu_abutment (float): Coefficient of friction between fastener head or nut against abutment (washer if present).
        separation_safety_factor (float): Factor of Safety for joint separation.
        yield_safety_factor (float): yield safety factor
        ultimate_safety_factor (float): ultimate safety factor
        fitting_factor (float): fitting factor
        preload_stress_ratio (float): stress in fastener target at nominal preload
        preload_uncertainty_factor (float): preload uncertainty
        relaxation_ratio (float): ratio of preload lost due to settling / relaxation
        ambient_temperature (float): ambient temperature
        max_temperature (float): maximum temeprature
        min_temperature (float): minimum temperature
        limit_tensile_load (float): applied limit tensile load (external)
        limit_shear_load (float): applied limit shear load (external)
        loaded_part_index (list[int]): list of indices indicating which clamped parts are loaded in the clmaped_parts list
        nut_torqued (bool): is the nut torqued? (else the fastener head is torqued), determines what geometry is used for nut factor estimation
        override_nut_factor (list[float]): nut factor, this value is used if it is provided, else it is estimated
        override_applied_torque (float): applied torque to create preload, this value is used if provided, else the preload stress ratio and nut factor are used to calculate a preload torque.
        distance_between_load_planes (float): Distance between load planes in the loaded clamped parts, used for load introduction factor.
    """
    def __init__(
            self, 
            name: str,
            fastener: Fastener,
            clamped_parts,
            nut: Nut=None,
            insert=None,
            mu_thread: float=0.15,
            mu_abutment: float=0.15,
            separation_safety_factor: float=1.2,
            yield_safety_factor: float=1.1,
            ultimate_safety_factor: float=1.4,
            fitting_factor: float=1.15,
            preload_stress_ratio: float=0.65,
            preload_uncertainty_factor: float=0.25,
            upper_preload_tolerance_factor: float=1.1,
            lower_preload_tolerance_factor: float=0.9,
            relaxation_ratio: float=0.05,
            ambient_temperature: float=20.0,
            max_temperature: float=20.0,
            min_temperature: float=20.0,
            limit_tensile_load: float=0.0,
            limit_shear_load: float=0.0,
            loaded_part_index: list[int]=[1,2],
            nut_torqued: bool=False, # is nut or head torqued?
            override_nut_factor: list=None, # [K_min, K_nom, K_max]
            override_applied_torque: float=None,
            distance_between_load_planes: float=None,
            preload_loss_due_to_material_creep: float=0.0,
        ):
        
        self.name = name
        
        self.fastener = fastener
        
        self.clamped_parts = clamped_parts
        
        self.nut = nut
        
        self.insert = insert
        
        self.override_nut_factor = override_nut_factor
        
        self.override_applied_torque = override_applied_torque
        
        # coefficient of friction at threads:
        assert mu_thread >= 0.0, "coefficient of friction must be >= 0.0"
        self.mu_thread = mu_thread
        
        # coefficient of friction under head or nut:
        assert mu_abutment >= 0.0, "coefficient of friction must be >= 0.0"
        self.mu_abutment = mu_abutment
        
        #################################
        # Safety Factors:
        #################################
        assert yield_safety_factor >= 1.0, "factors of safety must be >= 1.0"
        self.SF_y = yield_safety_factor
        
        assert ultimate_safety_factor >= 1.0, "factors of safety must be >= 1.0"
        self.SF_u = ultimate_safety_factor
        
        assert separation_safety_factor >= 1.0, "factors of safety must be >= 1.0"
        self.SF_sep = separation_safety_factor
        
        # Fitting Factor:
        assert fitting_factor >= 1.0, "fitting factor must be >= 1.0"
        self.FF = fitting_factor
        
        #################################
        # Temperatures:
        #################################
        assert max_temperature >= min_temperature, "max temperature must be > min temperature"
        #TODO: should these be argments to functions?
        self.T_amb_C = ambient_temperature
        self.T_min_C = min_temperature
        self.T_max_C = max_temperature
        
        # [C], change in temperature:
        self.delta_T_min = self.T_min_C - self.T_amb_C
        self.delta_T_max = self.T_max_C - self.T_amb_C
        
        #################################
        # Check Externally Applied Loads:
        #################################
        assert limit_tensile_load >= 0.0, "externally applied limit tensile load must be >= 0.0"
        assert limit_shear_load >= 0.0, "externally applied limit shear load must be >= 0.0"
        
        
        assert len(loaded_part_index) >= 2, "there must be at least 2 loaded parts (equal and opposite reaction)"
        self.loaded_part_index = loaded_part_index
        
        #################################
        # Preloading:
        #################################
        #TODO: should these be argments to functions?
        self.preload_stress_ratio = preload_stress_ratio
        
        assert relaxation_ratio >= 0.0, "relaxation ratio must be >= 0.0"
        self.relaxation_ratio = relaxation_ratio
        
        assert preload_uncertainty_factor >= 0.0
        self.preload_uncertainty_factor = preload_uncertainty_factor
        
        # TODO: validity check:
        self.lower_preload_tolerance_factor = lower_preload_tolerance_factor
        
        # TODO: validity check:
        self.upper_preload_tolerance_factor = upper_preload_tolerance_factor
    
        # [bool], is the nut or fastener head torqued?
        # TODO: validity check:
        self.nut_torqued = nut_torqued
        
        assert preload_loss_due_to_material_creep >= 0.0
        self.preload_loss_due_to_material_creep = preload_loss_due_to_material_creep
        
        ###############################
        # Joint Length:
        ###############################
        
        # Check length of clamped parts puts threads at the nut or insert...
        
        L_total_fast = self.fastener.length
        print(f"L_total_fast = {L_total_fast} [mm]")
        
        self.L_total_clamped_parts = 0.0
        for part in clamped_parts:
            self.L_total_clamped_parts += part.length
        
        print(f"L_total_clamped_parts = {self.L_total_clamped_parts} [mm]")
        
        # TODO: include length of nut or insert
        # must extent past by 1 full thread
        # must engage 3 full threads
        
        if L_total_fast < self.L_total_clamped_parts:
            # only matters for config #1:
            raise Exception("clamped parts length exceeds fastener length")
            
        
        # TODO: check shank length < clamped parts length
        # plus some margin...
        # what margin? 2 threads?
        if self.fastener.L_shank + 2.0*self.fastener.thread.pitch > self.L_total_clamped_parts:
            raise Exception("fastener shank longer than clamped parts")
        
        # TODO: check later that bolt stretch is < 2 threads...
        
        # Length of engagement:
        # TODO: deal with inserts or tapped holes:
        self.L_e = self.nut.length
        
        
        ###############################
        # Joint Stiffness:
        ###############################
        
        # [N/mm], fastener (bolt) stiffness:
        self.K_b = self.fastener.stiffness()
        print(f"K_b, bolt stiffness = {self.K_b} [N/mm]")
        
        L_list = []
        E_list = []
        
        for part in clamped_parts:
            L_list.append(part.length)
            E_list.append(part.material.E_mpa)
        
        # joint modulus:
        E_j = nasa_tm_106943.eq34mod(
            L_list=L_list,
            E_list=E_list,
        )
        
        # [N/mm], estimated clamped parts (joint) stiffness:
        K_j_106943 = nasa_tm_106943.eq33(
            E_j=E_j,
            D=self.fastener.thread.d,
            L=self.L_total_clamped_parts,
        )
        print(f"K_j_106943 = {K_j_106943} [N/mm]")
        
        # joint stiffness:
        self.K_j = K_j_106943
        
        ###############################
        # Joint Stiffness Factor, phi:
        ###############################
        
        # NASA-TM-106943 eq 29
        # NASA-STD-5020B eq 9:
        self.phi = nasa_std_5020b.eq9(
            k_b=self.K_b,
            k_c=self.K_j,
        )
        print(f"phi = {self.phi}")
        
        ###############################
        # Load Introduction Factor, n:
        ###############################
        
        # depends on configuration !!!
        # start with configs 1 and 3...
        
        # distance between load planes in clamped parts
        # used for load introduction factor, n
        
        if distance_between_load_planes is not None:
            assert distance_between_load_planes >= 0.0
            assert distance_between_load_planes <= self.L_total_clamped_parts
            self.distance_between_load_planes = distance_between_load_planes
        else:
            # use loaded_part_index...
            # assumes load is applied at middle of the loaded part
            self.distance_between_load_planes = 0.0
            
            if nut is not None:
                # configuration 1:
                for i, part in enumerate(clamped_parts):
                    if i == self.loaded_part_index[0]:
                        self.distance_between_load_planes += clamped_parts[i].length / 2.0
                    
                    if self.loaded_part_index[0] < i < self.loaded_part_index[1]:
                        self.distance_between_load_planes += clamped_parts[i].length
                    
                    if i == self.loaded_part_index[1]:
                        self.distance_between_load_planes += clamped_parts[i].length / 2.0
        
                # NASA-TM-106943 eq 18, pg 10:
                self.n = nasa_tm_106943.eq18(
                    d=self.distance_between_load_planes, 
                    t=self.L_total_clamped_parts,
                )
        
            if insert is not None:
                # configuration 3:
                raise Exception("insert not implemented yet...")
        
            # configuration 2 & 4 = flat head screws
        
        # NASA-STD-5020B, eq 37, pg 52:
        # NASA-STD-5020B, eq 48, pg 56:
        # NASA-STD-5020B, eq 52, pg 56:
        # NASA-STD-5020B, eq 57, pg 57:
        
        # NASA-TM-106943 eq 35, pg 12:
        # NASA-TM-106943 eq 46, pg 12:
        
        print(f"load introduction factor, n = {self.n}")
        
        
        ###############################
        # Nut Factor, K:
        ###############################
        
        if override_nut_factor is None:
        
            # what is mean thread diameter for K?
            #TODO: update to be average of ext and int:
            self.mean_thread_diameter = self.fastener.thread.d2
            
            # TODO: change based on nut_torqued:
            
            # head mean diameter for friction:
            #TODO: refine with hole diameter, not thread major d:
            self.mean_head_diameter = (self.fastener.Do_head + self.fastener.thread.d) / 2.0
            
            self.K_kb = kubler_bulten_nut_factor(
                P=self.fastener.thread.pitch, 
                d_2=self.mean_thread_diameter, 
                mu_t=self.mu_thread, 
                mu_b=self.mu_abutment, 
                d_w=self.mean_head_diameter, 
                d=self.fastener.thread.d,
            )
            
            self.K_08307 = nsts_08307a.nut_factor(
                R_t=self.mean_thread_diameter/2.0,  # mean radius of thread
                R_e=self.mean_head_diameter/2.0,  # mean head or nut radius
                mu_t_min=self.mu_thread,
                mu_t_typ=self.mu_thread, 
                mu_t_max=self.mu_thread,
                mu_b_min=self.mu_abutment,
                mu_b_typ=self.mu_abutment, 
                mu_b_max=self.mu_abutment,
                alpha=self.fastener.thread.psi, 
                beta=self.fastener.thread.beta, 
                D=self.fastener.thread.d,
            )[1]
            
            # nut factor: NASA-TM-106943 eq 2:
            self.K_106943 = nasa_tm_106943.eq2(
                D_p=self.mean_thread_diameter, 
                D=self.fastener.thread.d, 
                psi=self.fastener.thread.psi, 
                alpha=self.fastener.thread.beta, 
                mu=self.mu_thread, 
                mu_c=self.mu_abutment,
            )
            
            print(f"K_kb = {self.K_kb}")
            print(f"K_08307 = {self.K_08307}")
            print(f"K_106943 = {self.K_106943}")
            
            self.K_min = np.min([
                self.K_kb, 
                self.K_08307, 
                self.K_106943,
            ])
            
            self.K_max = np.max([
                self.K_kb, 
                self.K_08307, 
                self.K_106943,
            ])
            
            self.K_nom = (self.K_min + self.K_max)/2.0
        
        else:
            self.K_min = np.min(override_nut_factor)
            self.K_max = np.max(override_nut_factor)
            self.K_nom = override_nut_factor[1]
        
        print(f"K_min = {self.K_min}")
        print(f"K_nom = {self.K_nom}")
        print(f"K_max = {self.K_max}")
        
        ###############################
        # Applied Installation Torque:
        ###############################
        
        # TODO: change based on torque_override:
        
        # target 0.65 tensile yield stress / strength 
        # NASA-TM-106943 eq 3:
        # TODO: is there a 5020 equation?
        self.T_applied_nom = nasa_tm_106943.eq3(
            D=self.fastener.thread.d,  # major diameter
            K=self.K_nom,  # nut factor
            A_t=self.fastener.thread.A_t,  # A_t = tensile area
            F_ty=self.fastener.material.Sy_mpa,  # F_ty = material tensile yield strength
            preload_stress_ratio=self.preload_stress_ratio,
        )
        print(f"T_applied_nom = {self.T_applied_nom}")
        
        self.T_applied_min = nasa_tm_106943.eq3(
            D=self.fastener.thread.d,  # major diameter
            K=self.K_min,  # nut factor
            A_t=self.fastener.thread.A_t,  # A_t = tensile area
            F_ty=self.fastener.material.Sy_mpa,  # F_ty = material tensile yield strength
            preload_stress_ratio=self.preload_stress_ratio,
        )
        print(f"T_applied_min = {self.T_applied_min}")
        
        self.T_applied_max = nasa_tm_106943.eq3(
            D=self.fastener.thread.d,  # major diameter
            K=self.K_max,  # nut factor
            A_t=self.fastener.thread.A_t,  # A_t = tensile area
            F_ty=self.fastener.material.Sy_mpa,  # F_ty = material tensile yield strength
            preload_stress_ratio=self.preload_stress_ratio,
        )
        print(f"T_applied_max = {self.T_applied_max}")
        
        
    
        ###############################
        # Predicted Initial Preload: 
        ###############################
        
        # P_i: initial predicted nominal preload:
        # NASA-STD-5020B, eq 24:
        self.P_i_nom = nasa_std_5020b.eq24(
            T=self.T_applied_nom,
            K_nom=self.K_nom,
            D=self.fastener.thread.d,
        )
        print(f"P_i_nom = {self.P_i_nom}")
        
        self.P_i_min = nasa_std_5020b.eq4(
            c_min=lower_preload_tolerance_factor,
            gamma=self.preload_uncertainty_factor,
            P_pi_nom=self.P_i_nom,
        )
        print(f"P_i_min = {self.P_i_min}")
        
        self.P_i_max = nasa_std_5020b.eq3(
            c_max=upper_preload_tolerance_factor,
            gamma=self.preload_uncertainty_factor,
            P_pi_nom=self.P_i_nom,
        )
        print(f"P_i_max = {self.P_i_max}")
        
        # delta_b = 
        
        # delta_j = 
        
    
        ###############################
        # axial bolt load due to thermal effects: 
        ###############################
        
        # eq 10
        L = self.L_total_clamped_parts

        # TODO: fix joint coefficient of thermal expansion !!!
        # need a combined joint CTE !!!
        # alpha_j = self.clamped_parts[1].material.cte_mm_mm_C
        
        # NASA-TM-106943 eq10:
        self.P_th_min = nasa_tm_106943.eq10(
            K_b=self.K_b, 
            K_j=self.K_j, 
            L=self.L_total_clamped_parts, 
            delta_T=self.delta_T_min, 
            alpha_j=self.clamped_parts[1].material.cte_mm_mm_C, 
            alpha_b=self.fastener.material.cte_mm_mm_C,
        )
        
        # NASA-TM-106943 eq10:
        self.P_th_max = nasa_tm_106943.eq10(
            K_b=self.K_b, 
            K_j=self.K_j, 
            L=self.L_total_clamped_parts, 
            delta_T=self.delta_T_max, 
            alpha_j=self.clamped_parts[1].material.cte_mm_mm_C, 
            alpha_b=self.fastener.material.cte_mm_mm_C,
        )
        
        # which is worst case? min or max?
        # self.P_th = np.min([self.P_th_min, self.P_th_max])
        # print(f"P_th = {self.P_th} [N]")
        
        P_th_min_temp = np.min([self.P_th_min, self.P_th_max])
        self.P_th_max = np.max([self.P_th_min, self.P_th_max])
        self.P_th_min = P_th_min_temp
        
        print(f"P_th_min = {self.P_th_min} [N]")
        print(f"P_th_max = {self.P_th_max} [N]")
        
        
        #################################
        # Final Predicted Preload
        #################################
        
        # includes changes due to thermal conditions
        
        # NASA-STD-5020B eq1:
        self.P_max = nasa_std_5020b.eq1(
            P_pi_max=self.P_i_max,
            P_deltat_max=self.P_th_max,
        )
        
        # NASA-STD-5020B eq2mod:
        # self.P_min = self.P_i_min - self.preload_loss_due_to_material_creep
        self.P_min = nasa_std_5020b.eq2mod(
            P_pi_min=self.P_i_min,
            P_deltat_min=self.P_th_min,
            P_pc=self.preload_loss_due_to_material_creep,
            relaxation_ratio=self.relaxation_ratio,
        )
        
        assert self.P_min <= self.P_max, "error in final preload prediction"
        
        print(f"P_min = {self.P_min} [N]")
        print(f"P_max = {self.P_max} [N]")


        ######################################
        # Margins
        ######################################
        
        ######################################
        # Tension only fastener strength:
        ######################################
        # yield axial load: NASA-STD-5020B eq16:
        
        # bolt load (ultimate):
        P_b_u = nsts_08307a.bolt_axial_load_for_strength(
            PLD_max=self.P_max, 
            n=self.n, 
            phi=self.phi, 
            SF=self.SF_u, 
            P=limit_tensile_load,
        )
        
        # NSTS08307A: bolt_tensile_margin:
        MS_tu_08307a = nsts_08307a.bolt_tensile_margin(
            PA_t=self.fastener.P_tu_allow, 
            SF=self.SF_u, 
            P=limit_tensile_load, 
            P_b=P_b_u,
        )
        print(f"MS_tu_08307a = {MS_tu_08307a}")
        
        # TODO: override for P_tu_allow, P_ty_allow
        
        # applied tensile load that causes the bolt load to exceed the allowable ultimate tensile load
        P_prime_tu = nasa_std_5020b.eq10(
            n=self.n, 
            phi=self.phi, 
            P_tu_allow=self.fastener.P_tu_allow, 
            P_p_max=self.P_max,
        )
        print(f"P_prime_tu = {P_prime_tu}")
        
        P_prime_sep = nasa_std_5020b.eq11(
            P_p_max=self.P_max, 
            n=self.n, 
            phi=self.phi,
        )
        print(f"P_prime_sep = {P_prime_sep}")
        
        # ultimate tensile load: NASA-STD-5020B eq6:
        # ultimate tensile margin of safety:
        MS_tu_5020b = nasa_std_5020b.eq6(
            P_tu_allow=self.fastener.P_tu_allow, 
            FS_u=self.SF_u, 
            P_tL=limit_tensile_load,
            FF=self.FF,
        )
        print(f"MS_tu_5020b = {MS_tu_5020b}")
        
        # ultimate tensile load: NASA-STD-5020B eq7:
        # ultimate tensile margin of safety:
        MS_tu_5020b = nasa_std_5020b.eq7(
            P_prime_tu=P_prime_tu, 
            FS_u=self.SF_u, 
            P_tL=limit_tensile_load,
            FF=self.FF,
        )
        print(f"MS_tu_5020b = {MS_tu_5020b}")
        
        # yield axial load: NASA-STD-5020B eq15:
        # yield tensile margin of safety:
        MS_ty_5020b = nasa_std_5020b.eq15(
            P_ty_allow=self.fastener.P_ty_allow, 
            FS_y=self.SF_y, 
            P_tL=limit_tensile_load,
            FF=self.FF,
        )
        print(f"MS_ty_5020b = {MS_ty_5020b}")
        
        P_prime_ty = nasa_std_5020b.eq17(
            n=self.n, 
            phi=self.phi, 
            P_ty_allow=self.fastener.P_ty_allow, 
            P_p_max=self.P_max,
        )
        print(f"P_prime_ty = {P_prime_ty}")
        
        MS_ty_5020b = nasa_std_5020b.eq16(
            P_prime_ty=P_prime_ty, 
            FS_y=self.SF_y, 
            P_tL=limit_tensile_load,
            FF=self.FF,
        )
        print(f"MS_ty_5020b = {MS_ty_5020b}")
        
        ######################################
        # Shear only fastener strength:
        ######################################
        # ultimate shear load: nasa_std_5020b eq14:
        # NASA-TM-106943 eq54:
        # NSTS08307A shear_margin:
        
        # NASA-TM-106943, pg 16, F_sy = 0.577 * F_ty
        
        # TODO: fix:
        P_su_allow = self.fastener.P_su_allow
        print(P_su_allow)
        
        # ultimate shear margin of safety:
        MS_su_5020b = nasa_std_5020b.eq14(
            P_su_allow=P_su_allow[1], 
            FS_u=self.SF_u, 
            P_sL=limit_shear_load, 
            FF=self.FF,
        )
        print(f"MS_su_5020b = {MS_su_5020b}")
        
        # Bending Only Margin:
        # NSTS08307A bending_margin:
        # NSTS08307A bolt_bending_margin:
        
        # Tension and shear fastener strength:
        # NASA-TM-106943 eq59:
        
        ######################################
        # Tension, shear, bending fastener strength:
        ######################################
        # ultimate combined load: NASA-STD-5020B eq20mod:
        # ultimate combined load: NASA-STD-5020B eq21mod:
        # ultimate combined load: NASA-STD-5020B eq22mod:
        # ultimate combined load: NASA-STD-5020B eq23mod:
        # NASA-TM-106943 eq62:
        # NSTS08307A combined_load_margin:
        
        ######################################
        # Joint Separation Margin:
        ######################################
        # NASA-TM-106943 eq68:
        # NSTS08307A joint_separation_margin_of_safety:
        
        # NASA-STD-5020B eq19:
        MS_sep_5020b = nasa_std_5020b.eq19(
            P_p_min=self.P_min, 
            SF_sep=self.SF_sep, 
            P_tL=limit_tensile_load,
            FF=self.FF, 
        )
        print(f"MS_sep_5020b = {MS_sep_5020b}")
        
        
        
        ######################################
        # Joint slip:
        ######################################
        
        # NASA-STD-5020B eq86:
        
        
        ######################################
        # Shear Pull Out of Threads:
        ######################################
        
        # external threads pull out shear area:
        A_se = nsts_08307a.external_thread_shear_area(
            L_e=self.L_e,
            K_i_max=self.nut.thread.D1_max,  # max minor diam of int threads
            n_0=None,
            TK_i=,  # tol on minor diam of int threads
            TE_e=,  # tol on pitch diam of ext threads
            G_e=,  # allowance on ext threads
            pitch=self.fastener.thread.pitch,
        )
        
        # internal threads pull out shear area:
        A_si = nsts_08307a.internal_thread_shear_area(
            L_e=self.L_e,
            D_e_min=,  # min major diam of ext threads
            n_0=None,
            TD_e=,  # tol on major diam ext threads
            TE_i=,  # tol on pitch diam int threads
            G_e=,  # allowance on ext threads
            pitch=self.fastener.thread.pitch,
        )
        
        
        # NSTS08307A: thread_shear_pull_out_margin (ultimate)
        MS_thread_shear_pull_out_u_08307a = nsts_08307a.thread_shear_pull_out_margin(
            PA_s=self.fastener.PA_s_08307a, 
            SF=self.SF_u, 
            P=limit_tensile_load, 
            P_b=P_b_u,
        )
        print(f"MS_thread_shear_pull_out_u_08307a = {MS_thread_shear_pull_out_u_08307a}")
        
        
        # Bolt Thread Shear:
        # NASA-TM-106943 eq65:
        
        # Shear Tear Out:
        # NASA-TM-106943 eq71:
        
        # Bolt Bearing (Shank Shear):
        # NASA-TM-106943 eq74:
        
        # Bearing under Bolt Head or Nut:
        # NASA-TM-106943 eq75:
        
        # Threaded Insert Thread:
        # NASA-TM-106943 eq77:
        
        # Nut Strength:
        # NASA-TM-106943 eq81:
        


    def sep_margin_tm106943(self) -> float:
        """Joint separation margin.
        
        NASA-TM-106943 eq68
        
        P_0_min: minimum preload
        P_sep: separating external load
        SF_sep: separation safety factor
        """
        # TODO: just use the function in tm_106943...
        MS_sep = (P_0_min / (self.SF_sep * P_sep)) - 1.0
        return MS_sep
    
    def ultimate_shear_margin_5020b(self) -> float:
        """Calculate ultimate shear margin.
        
        NASA-STD-5020B eq 14
        
        FS_u: ultimate factor of safety
        P_su_allow: shear load that exceed ultimate strength
        P_sL: limit shear load acting on the shear plane
        """
        MS_u_shear = thread_fast.nasa_std_5020b.eq14(
            P_su_allow=P_su_allow,
            FS_u=self.SF_u,
            P_sL=P_sL,
            FF=self.fitting_factor,
        )
        return MS_u_shear
    

    # TODO: constructor with all basic parameters:
    
    # TODO: 
    def to_dict(self):
        return {
            "type": 'BoltedJoint',
            "name": self.name,
            "fastener": self.fastener.to_dict(),
            "nut": self.nut.to_dict(),
            "separation_safety_factor": self.SF_sep,
            "yield_safety_factor": self.SF_y,
            "ultimate_safety_factor": self.SF_u,
            "fitting_factor": self.FF,
            "distance_between_load_planes": self.distance_between_load_planes,
            # calculated values:
            "load_introduction_factor": self.n,
            "stiffness_factor": self.phi,
            "bolt_stiffness": self.K_b,
            "joint_stiffness": self.K_j,
            # environment:
            "ambient_temperature": self.T_amb_C,
            "min_temperature": self.T_min_C,
            "max_temperature": self.T_max_C,
            # Preloading:
            "relaxation_ratio": self.relaxation_ratio,
            "preload_stress_ratio": self.preload_stress_ratio,
            "preload_uncertainty_factor": self.preload_uncertainty_factor,
            "override_nut_factor": self.override_nut_factor,
            "override_applied_torque": self.override_applied_torque,
            "K_nut_factor_min": self.K_min,
            "K_nut_factor_nom": self.K_nom,
            "K_nut_factor_max": self.K_max,
            "L_total_clamped_parts": self.L_total_clamped_parts,
            "thermal_preload_min": self.P_th_min,
            "thermal_preload_max": self.P_th_max,
            "preload_min": self.P_min,
            "preload_max": self.P_max,
        }
    
    def to_json(self):
        """Returns json object from dictionary."""
        return json.dumps(self.to_dict())
    
    def write_to_json(self, filename: str or Path):
        """Save json data to a file."""
        with open(filename, "w") as f:
            f.write(self.to_json())
    
    def __str__(self):
        return "\n".join([
            "\nBoltedJoint:",
            f"name = {self.name}",
            f"SF_y = {self.SF_y}",
            f"SF_u = {self.SF_u}",
            f"SF_sep = {self.SF_sep}",
            f"FF = {self.FF}",
            f"T_amb = {self.T_amb_C}",
            f"T_min = {self.T_min_C}",
            f"T_max = {self.T_max_C}",
            "",
        ])



def main() -> None:
    # Tests:
    
    # Basic case: socket head screw with nut
    
    ######################################
    # Define Materials:
    ######################################
    
    #TODO: move these to a material database:
    
    # Fastener material:
    a286 = Material(
        name='a286',
        E_mpa=200.0e3,
        nu=0.3,
        rho_gcc=7.93,
        cte_mm_mm_C=16.5e-6,
        tc_w_mK=15.1,
        hc_J_gC=420.0/1000.0,
        Sy_mpa=586.0,
        Su_mpa=896.0,
    )
    
    # Washer material:
    inconel_718 = Material(
        name='inconel_718',
        E_mpa=200.0e3,
        nu=0.29,
        rho_gcc=8.19,
        cte_mm_mm_C=13.0e-6,
        tc_w_mK=11.4,
        hc_J_gC=0.435,
        Sy_mpa=1100.0,
        Su_mpa=1375.0,
    )
    
    # Nut material:
    stainless_steel_18_8 = Material(
        name='stainless_steel_18_8',
        E_mpa=200.0e3,
        nu=0.29,
        rho_gcc=8.0,
        cte_mm_mm_C=17.5e-6,
        tc_w_mK=16.2,
        hc_J_gC=0.5,
        Sy_mpa=215.0,
        Su_mpa=505.0,
    )
    
    # Clamped parts materials:
    ti6al4v = Material(
        name='ti6al4v',
        E_mpa=114.0e3,
        nu=0.342,
        rho_gcc=4.43,
        cte_mm_mm_C=8.6e-6,
        tc_w_mK=6.7,
        hc_J_gC=0.526,
        Sy_mpa=880.0,
        Su_mpa=950.0,
    )
    
    ######################################
    # Define Threads:
    ######################################
    
    # fastener thread:
    fast_thread = ExternalMetricThread(
        name='M6x1.0',
        basic_major_diameter=6.0,
        pitch=1.0,
        tolerance_grade=4,
        allowance_class='h',
        profile='M',
        beta=30.0 * cf.deg_to_rad,
    )
    
    # nut thread:
    nut_thread = InternalMetricThread(
        name='M6x1.0',
        basic_major_diameter=6.0,
        pitch=1.0,
        tolerance_grade=4,
        allowance_class='H',
        profile='M',
        beta=30.0 * cf.deg_to_rad,
    )
    
    ######################################
    # Define Fastener:
    ######################################
    
    fastener = Fastener(
        name='fastener',
        thread=fast_thread,
        material=a286,
        Do_head=10.0,
        Do_shank=6.0,
        L_shank=20.0,
        L_thread=10.0,
    )
    
    ######################################
    # Define Design Requirements:
    ######################################
    
    # yield safety factor:
    SF_y = 1.1
    
    # ultimate safety factor:
    SF_u = 1.4
    
    # separation safety factor:
    SF_sep = 1.2
    
    # fitting factor:
    FF = 1.15
    
    
    ######################################
    # Define External Loading:
    ######################################
    
    # should these be arguments to margin functions?
    
    # [N], externally applied tensile load:
    P_et = 100.0
    
    # [N], limit shear load acting on the shear plane:
    P_sL = 100.0
    
    # TODO: bending load...
    
    
    ######################################
    # Define Clamped Parts:
    ######################################
    
    # washers under head:
    washer1 = Washer(
        nominal_size=6.0,
        D_hole = 6.4,
        D_outer=12.0,
        thickness=1.4,
        material=inconel_718,
        # chamfer=True,
    )
    
    # loaded part 1
    part1 = ClampedPart(
        name='part1',
        D_hole = 6.4,
        D_outer=12.0,
        thickness=10.0,
        material=ti6al4v,
    )
    
    # loaded part 2
    part2 = ClampedPart(
        name='part2',
        D_hole = 6.4,
        D_outer=12.0,
        thickness=10.0,
        material=ti6al4v,
    )
    
    # washers under nut:
    washer2 = Washer(
        nominal_size=6.0,
        D_hole = 6.4,
        D_outer=12.0,
        thickness=1.4,
        material=inconel_718,
        # chamfer=True,
    )
    
    ######################################
    # Define Nut:
    ######################################
    
    nut = Nut(
        Do=10.0,
        length=5.0,
        thread=nut_thread,
        material=a286,
    )
    
    ######################################
    # Define Bolted Joint:
    ######################################
    
    bj1 = BoltedJoint(
        name='bj1',
        fastener=fastener,
        clamped_parts=[
            washer1,
            part1,
            part2,
            washer2,
        ],
        nut=nut,
        insert=None,
        mu_thread=0.2,
        mu_abutment=0.2,
        separation_safety_factor=SF_sep,
        yield_safety_factor=SF_y,
        ultimate_safety_factor=SF_u,
        fitting_factor=1.15,
        preload_stress_ratio=0.65,
        preload_uncertainty_factor=0.25,
        relaxation_ratio=0.05,
        ambient_temperature=20.0,
        max_temperature=25.0,
        min_temperature=15.0,
        limit_tensile_load=1000.0,
        limit_shear_load=100.0,
        loaded_part_index=[1,2],
        nut_torqued=False, # is nut or head torqued?
        #override_nut_factor=[0.1, 0.15, 0.2],
    )
    
    # export to dictionary:
    bj1_dict = bj1.to_dict()
    print(bj1_dict)
    
    # test to_json:
    


if __name__ == "__main__":
    main()
    