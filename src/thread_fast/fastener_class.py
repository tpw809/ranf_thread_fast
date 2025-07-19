"""Fastener Class Definition

Timothy P Woodard, June 21, 2025


Fastener consists of:

- head
- shank (un-threaded length)
- thread
- material

Shank definition:
[
    [Do, L]
    [Do, L]
    ...
    [Do, L]
]

"""
import numpy as np
import thread_fast.nsts_08307a as nsts_08307a
import thread_fast.nasa_tm_106943 as nasa_tm_106943
from thread_fast.material_class import Material
from thread_fast.threads.metric_thread_class import ExternalMetricThread
import thread_fast.conversion_factors as cf


class Fastener:
    """
    
    Args:
        name (str): Descriptive name of the fastener.
        thread (Thread): thread of the fastener.
        material (Material): material of the fastener.
        Do_head (float): outer diameter of the head (contacting the abutment).
        Do_shank (float): outer diameter of the fastener shank (unthreaded portion).
        L_shank (float): length of the shank (unthreaded portion).
        L_thread (float): threaded length of the fastener.
    """
    def __init__(
            self, 
            name: str,
            thread: ExternalMetricThread,
            material: Material,
            Do_head: float,
            Do_shank: float,
            L_shank: float,
            L_thread: float,
        ):
            
        assert L_shank >= 0.0
        assert L_thread > 0.0   
        assert Do_shank > 0.0
        assert Do_head > Do_shank
        
        self.name = name
        
        self.thread = thread
        
        self.material = material
        
        # head (bearing surface) outer diameter:
        self.Do_head = Do_head
        
        # shank outer diameter:
        self.Do_shank = Do_shank
        
        # shank (un-threaded) length:
        self.L_shank = L_shank
        
        # threaded length:
        self.L_thread = L_thread
        
        
        # [mm^2], minimum minor diameter area for the fastener threads:
        # NSTS 08307A, bolt_tensile_stress_area
        
        # TODO: this might not be the right area... need shear area...
        self.A_m = nsts_08307a.bolt_tensile_stress_area(
            D_e_bsc=self.thread.d, 
            n_0=None,
            pitch=self.thread.pitch,
        )
        print(f"A_m = {self.A_m}")
        print(f"A_t = {self.thread.A_t}")
        
        # [N], allowable ultimate shear load:
        # NASA-STD-5020B eq 12 & 13
        
        # NASA-STD-5020B eq 12:
        # F_su = allowable ultimate shear strength for the fastener material
        F_su = self.material.Ssu_mpa
        P_su_allow = np.pi * self.thread.d**2 * F_su / 4.0
        print(f"P_su_allow = {P_su_allow}")
        
        # NASA-STD-5020B eq 13:
        P_su_allow = F_su * self.A_m
        print(f"P_su_allow = {P_su_allow}")
        
    @property
    def Ro_shank(self) -> float:
        return self.Do_shank / 2.0
        
    @property
    def length(self) -> float:
        """length, mm."""
        return self.L_shank + self.L_thread
    
    def stiffness(self) -> float:
        """axial stiffness, N/mm
        
        NASA-TM-106943 eq 32, pg 12
        
        k = (A * E) / L
        
        Springs in series:
        
        Do we need a length argument?
        """
        #TODO: finish this!
        # need area
        # need to combine shank and threaded length
        A_shank = np.pi * self.Ro_shank**2
        # what to use for theaded length outer radius?
        # NASA-TM-106943, equation 32, pg 12
        A_thread = self.thread.A_mean
        k_shank = A_shank * self.material.E_mpa / self.L_shank
        k_thread = A_thread * self.material.E_mpa / self.L_thread
        
        # combined stiffness in series:
        k_total = 1.0 / (1.0 / k_shank + 1.0 / k_thread)
        print(f"k_b_total = {k_total} [N/mm]")
        
        # TODO: compare against: NASA-TM-106943, equation 32, pg 12
        A_nom = np.pi * (self.thread.d / 2.0)**2
        
        K_106943 = nasa_tm_106943.eq32(
            A=A_nom,
            E_b=self.material.E_mpa,
            L=self.length,
        )
        print(f"K_106943 = {K_106943} [N/mm]")
        
        # TODO: which stiffness is worst case? Kmax or Kmin?
        return k_total

    def to_dict(self) -> dict:
        return {
            "type": 'Fastener',
            "name": self.name,
            "material": self.material.to_dict(),
            "thread": self.thread.to_dict(),
            "Do_head": self.Do_head,
            "Do_shank": self.Do_shank,
            "L_shank": self.L_shank,
        }

    def __str__(self):
        return "\n".join([
            "\nFastener:",
            f"name = {self.name}",
            f"{self.thread}",
            f"Do_head = {self.Do_head}",
            f"Do_shank = {self.Do_shank}",
            f"L_shank = {self.L_shank}",
            f"L_thread = {self.L_thread}",
            f"L_overall = {self.length}",
            f"\n{self.material}",
            "",
        ])


def main() -> None:
    # Tests:
    
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
    
    thread = ExternalMetricThread(
        name='M6x1.0',
        basic_major_diameter=6.0,
        pitch=1.0,
        tolerance_grade=4,
        allowance_class='h',
        # external=True,
        profile='M',
        beta=30.0 * cf.deg_to_rad,
    )
    
    fast1 = Fastener(
        name='test_fastener',
        thread=thread,
        material=a286,
        Do_head=8.5,
        Do_shank=5.0,
        L_shank=10.0,
        L_thread=10.0,
    )
    print(fast1)
    
    # to dictionary:
    fast1_dict = fast1.to_dict()
    print(fast1_dict)


if __name__ == "__main__":
    main()
    