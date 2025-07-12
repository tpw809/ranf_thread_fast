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
import numpy as np
import thread_fast.nsts_08307a as nsts_08307a
import thread_fast.nasa_tm_106943 as nasa_tm_106943
import thread_fast.nasa_std_5020 as nasa_std_5020
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
    """
    def __init__(
            self, 
            name: str,
            fastener: Fastener,
            clamped_parts,
            nut: Nut,
            mu_thread: float=0.15,
            mu_abutment: float=0.15,
            separation_safety_factor: float=1.2,
            yield_safety_factor: float=1.1,
            ultimate_safety_factor: float=1.4,
            fitting_factor: float=1.15,
            preload_stress_ratio: float=0.65,
            preload_uncertainty_factor: float=0.25,
            relaxation_ratio: float=0.05,
            ambient_temperature: float=20.0,
            max_temperature: float=20.0,
            min_temperature: float=20.0,
            nut_torqued: bool=False, # is nut or head torqued?
            override_nut_factor: float=None, # [K_min, K_max]
            override_applied_torque: float=None,
        ):
        
        self.name = name
        
        self.fastener = fastener
        
        self.clamped_parts = clamped_parts
        
        self.nut = nut
        
        self.override_nut_factor = override_nut_factor
        
        self.override_applied_torque = override_applied_torque
        
        # coefficient of friction at threads:
        assert mu_thread >= 0.0
        self.mu_thread = mu_thread
        
        # coefficient of friction under head or nut:
        assert mu_abutment >= 0.0
        self.mu_abutment = mu_abutment
        
        # Safety Factors:
        assert yield_safety_factor >= 1.0
        self.SF_y = yield_safety_factor
        
        assert ultimate_safety_factor >= 1.0
        self.SF_u = ultimate_safety_factor
        
        assert separation_safety_factor >= 1.0
        self.SF_sep = separation_safety_factor
        
        # Fitting Factor:
        assert fitting_factor >= 1.0
        self.FF = fitting_factor
        
        # Temperatures:
        assert max_temperature >= min_temperature
        #TODO: should these be argments to functions?
        self.T_amb_C = ambient_temperature
        self.T_min_C = min_temperature
        self.T_max_C = max_temperature
        
        # [C], change in temperature:
        self.delta_T_min = self.T_min_C - self.T_amb_C
        self.delta_T_max = self.T_max_C - self.T_amb_C
        
        # Preloading:
        #TODO: should these be argments to functions?
        self.preload_stress_ratio = preload_stress_ratio
        
        assert relaxation_ratio >= 0.0
        self.relaxation_ratio = relaxation_ratio
        
        assert preload_uncertainty_factor >= 0.0
        self.preload_uncertainty_factor = preload_uncertainty_factor
    
        # [bool], is the nut or fastener head torqued?
        self.nut_torqued = nut_torqued
        
        
        ###############################
        # Joint Length:
        ###############################
        
        # Check length of clamped parts puts threads at the nut or insert...
        
        L_total_fast = self.fastener.length
        print(f"L_total_fast = {L_total_fast} [mm]")
        
        L_total_clamped_parts = 0.0
        for part in clamped_parts:
            L_total_clamped_parts += part.length
        
        print(f"L_total_clamped_parts = {L_total_clamped_parts} [mm]")
        
        # TODO: include length of nut or insert
        # must extent past by 1 full thread
        # must engage 3 full threads
        
        if L_total_fast < L_total_clamped_parts:
            raise Exception("clamped parts length exceeds fastener length")
        
        # TODO: check shank length < clamped parts length
        # plus some margin...
        
        
        ###############################
        # Joint Stiffness:
        ###############################
        
        # [N/mm], fastener (bolt) stiffness:
        K_b = self.fastener.stiffness()
        print(f"K_b = {K_b} [N/mm]")
        
        # joint modulus:
        #E_j = nasa_tm_106943.eq34()
        E_j = clamped_parts[1].material.E_mpa
        
        # [N/mm], estimated clamped parts (joint) stiffness:
        K_j_106943 = nasa_tm_106943.eq33(
            E_j=E_j,
            D=self.fastener.thread.d,
            L=L_total_clamped_parts,
        )
        print(f"K_j_106943 = {K_j_106943} [N/mm]")
        
        K_j = K_j_106943
        
        ###############################
        # Joint Stiffness Factor:
        ###############################
        
        # NASA-TM-106943 eq 29
        # NASA-STD-5020B eq 9
        phi = K_b / (K_b + K_j)
        print(f"phi = {phi}")
        
        
        
        ###############################
        # Load Introduction Factor, n:
        ###############################
        
        # NASA-STD-5020B, eq 37, pg 52:
        # NASA-STD-5020B, eq 48, pg 56:
        # NASA-STD-5020B, eq 52, pg 56:
        # NASA-STD-5020B, eq 57, pg 57:
        
        
        # NASA-TM-106943 eq 35, pg 12:
        
        # NASA-TM-106943 eq 46, pg 12:
        
        
        ###############################
        # Nut Factor, K:
        ###############################
        
        # what is mean thread diameter for K?
        #TODO: update to be average of ext and int:
        self.mean_thread_diameter = self.fastener.thread.d2
        
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
        
        print(f"K_min = {self.K_min}")
        print(f"K_max = {self.K_max}")
        
        ###############################
        # Applied Installation Torque:
        ###############################
        
        # target 0.65 tensile yield stress / strength 
        # NASA-TM-106943 eq 3:
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
        # axial bolt load due to thermal effects: 
        ###############################
        
        # eq 10
        L = L_total_clamped_parts
        alpha_b = self.fastener.material.cte_mm_mm_C
        alpha_j = self.clamped_parts[1].material.cte_mm_mm_C
        
        #TODO: where is this from? just use that function...
        P_th_min = ((K_b * K_j) / (K_b + K_j)) * L * self.delta_T_min * (alpha_j - alpha_b)
        
        #TODO: where is this from? just use that function...
        P_th_max = ((K_b * K_j) / (K_b + K_j)) * L * self.delta_T_max * (alpha_j - alpha_b)
        
        # which is worst case? min or max?
        P_th = np.min([P_th_min, P_th_max])
        print(f"P_th = {P_th} [N]")


    def sep_margin_tm106943(self) -> float:
        """
        NASA-TM-106943 eq68
        
        P_0_min = 
        P_sep = 
        """
        MS_sep = (P_0_min / (self.SF_sep * P_sep)) - 1.0
        return MS_sep
    
    def ultimate_shear_margin_5020b(self) -> float:
        """
        NASA-STD-5020B eq 14
        
        P_su_allow = 
        P_sL = limit shear load acting on the shear plane
        """
        MS_u_shear = thread_fast.nasa_std_5020b.eq14(
            P_su_allow=P_su_allow,
            FS_u=self.SF_u,
            P_sL=P_sL,
            FF=self.fitting_factor,
        )
        return MS_u_shear
    

    # TODO: constructor with all basic parameters:
    
    # TODO: to_dict()
    
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
        max_temperature=20.0,
        min_temperature=20.0,
        nut_torqued=False, # is nut or head torqued?
    )
    


if __name__ == "__main__":
    main()
    