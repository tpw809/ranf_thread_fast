"""Fastener Class Definition

Timothy P Woodard, June 21, 2025


Fastener consists of:
-head
-shank (un-threaded length)
-thread
-material

Shank definition:
[
    [Do, L]
    [Do, L]
    ...
    [Do, L]
]

"""
import numpy as np
from thread_fast import Material
from thread_fast import MetricThread
import thread_fast.conversion_factors as cf


class Fastener:
    def __init__(
            self, 
            name: str,
            thread: MetricThread,
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
        
    @property
    def length(self) -> float:
        """length, mm."""
        return self.L_shank + self.L_thread
    
    def stiffness(self) -> float:
        """axial stiffness, N/mm
        
        k = (A * E) / L
        """
        return self.material.E_mpa / self.length

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
    
    thread = MetricThread(
        name='M6x1.0',
        basic_major_diameter=6.0,
        pitch=1.0,
        tolerance_grade=4,
        allowance_class='h',
        external=True,
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


if __name__ == "__main__":
    main()
    