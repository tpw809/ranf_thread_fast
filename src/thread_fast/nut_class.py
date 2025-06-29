"""Fastener Class Definition

Timothy P Woodard, June 21, 2025

Nut consists of:

- body (length and outer diameter)
- thread
- material

"""
import numpy as np
from thread_fast.material_class import Material
from thread_fast.threads.metric_thread_class import InternalMetricThread
import thread_fast.conversion_factors as cf


class Nut:
    def __init__(
            self, 
            Do: float, 
            length: float,
            thread, 
            material,
        ):
        
        # outer bearing diameter (on abutment):
        self.Do = Do
        
        self.length = length
        
        self.thread = thread
        
        self.material = material
        
    def __str__(self):
        return "\n".join([
            "\nNut:",
            f"Do = {self.Do}",
            f"length = {self.length}",
            f"{self.thread}",
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
    
    thread = InternalMetricThread(
        name='M6x1.0',
        basic_major_diameter=6.0,
        pitch=1.0,
        tolerance_grade=4,
        allowance_class='H',
        # internal=True,
        profile='M',
        beta=30.0 * cf.deg_to_rad,
    )

    nut1 = Nut(
        Do=9.0,
        length=5.0,
        thread=thread,
        material=a286,
    )
    print(nut1)



if __name__ == "__main__":
    main()
    