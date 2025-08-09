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

Symbols:

- P_su_allow_1: allowable ultimate shear load, threads NOT in shear plane
- P_su_allow_2: allowable ultimate shear load, threads in shear plane

"""
import numpy as np
import thread_fast.nsts_08307a as nsts_08307a
import thread_fast.nasa_tm_106943 as nasa_tm_106943
from thread_fast.material_class import Material
from thread_fast.threads.metric_thread_class import ExternalMetricThread
import thread_fast.conversion_factors as cf


class Fastener:
    """Fastener class.
    
    Contains material, threads, head and shank information.
    
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
            
        assert L_shank >= 0.0, "shank length must be >= 0"
        assert L_thread > 0.0, "thread length must be > 0"
        assert Do_shank > 0.0, "shank diameter must be > 0"
        assert Do_head > Do_shank, "head diameter must be > shank diameter"
        
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
        self.A_t = nsts_08307a.bolt_tensile_stress_area(
            D_e_bsc=self.thread.d, 
            n_0=None,  # tpi
            pitch=self.thread.pitch,
        )
        print(f"A_t_nsts08307a = {self.A_t}")
        print(f"A_t = {self.thread.A_t}")
        print(f"A_mean = {self.thread.A_mean}")
        
        # [N], allowable ultimate tensile load:
        # NSTS 08307A page A-4, ultimate tensile load:
        self.P_tu_allow = self.A_t * self.material.Stu_mpa
        self.P_ty_allow = self.A_t * self.material.Sty_mpa
        print(f"P_tu_allow = {self.P_tu_allow} [N]")
        print(f"P_ty_allow = {self.P_ty_allow} [N]")
        
        # [N], allowable ultimate shear load:
        # NASA-STD-5020B eq 12 & 13
        
        # NASA-STD-5020B eq 12:
        # F_su = allowable ultimate shear strength for the fastener material
        F_su = self.material.Ssu_mpa
        # For shank (not threads):
        A_bolt = np.pi  * self.thread.d**2 / 4.0
        print(f"A_bolt = {A_bolt}")
        
        # P_su_allow: allowable ultimate shear load
        # depends on if threads are in the shear plane...
        self.P_su_allow_1 = np.pi * self.thread.d**2 * F_su / 4.0
        # TODO: just use the eq in nasa_std_5020b: eq 12
        print("threads not in shear plane:")
        print(f"P_su_allow_1 = {self.P_su_allow_1}")
        
        # NASA-STD-5020B eq 13:
        self.P_su_allow_2 = F_su * self.A_t
        print("threads in shear plane:")
        print(f"P_su_allow_2 = {self.P_su_allow_2}")
    
    @property
    def P_su_allow(self) -> tuple[float, float]:
        """Allowable ultimate shear load"""
        # allowable ultimate shear strength for the fastener material:
        F_su = self.material.Ssu_mpa
        # threads NOT in shear plane:
        P_su_allow_1 = np.pi * self.thread.d**2 * F_su / 4.0
        # threads in shear plane:
        P_su_allow_2 = F_su * self.A_t
        return P_su_allow_1, P_su_allow_2
    
    def PA_s_08307a(self, A_se: float) -> float:
        """thread shear (pull out) load allowable, external thread
        
        NSTS 08307A, pg A-4
        """
        PA_s = nsts_08307a.external_thread_shear_load_allowable(
            A_se=A_se,
            F_su_bolt=self.material.Ssu_mpa,
        )
        return PA_s
    
    @property
    def Ro_shank(self) -> float:
        """Outer radius of fastener shank."""
        return self.Do_shank / 2.0
        
    @property
    def length(self) -> float:
        """fastener total length, mm."""
        return self.L_shank + self.L_thread
    
    def stiffness(self) -> float:
        """axial stiffness, N/mm
        
        NASA-TM-106943 eq 32, pg 12
        
        k = (A * E) / L
        
        Springs in series:
        
        Do we need a length argument? -> probably yes...
        """
        #TODO: finish this! add length argument...
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
        
        # compare against: NASA-TM-106943, equation 32, pg 12
        A_nom = np.pi * (self.thread.d / 2.0)**2
        
        K_b_106943 = nasa_tm_106943.eq32(
            A=A_nom,
            E_b=self.material.E_mpa,
            L=self.length,
        )
        print(f"K_b_106943 = {K_b_106943} [N/mm]")
        
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
            "L_thread": self.L_thread,
            "L_overall": self.length,
            'stiffness': self.stiffness(),
            # tensile and shear area
            # thread shear area
            "P_tu_allow": self.P_tu_allow,
            # P_su_allow (PA_su)
            "P_ty_allow": self.P_ty_allow,
            # P_sy_allow (PA_sy)
            # thread shear allowable
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
            f"stiffness = {self.stiffness()}",
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
        Sty_mpa=586.0,
        Stu_mpa=896.0,
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
    