"""Nut Class Definition

Timothy P Woodard, June 21, 2025

Nut consists of:

- body (length and outer diameter)
- thread
- material

"""
import numpy as np
import thread_fast.nsts_08307a as nsts_08307a
from thread_fast.materials.material_class import Material
from thread_fast.threads.metric_thread_class import InternalMetricThread
import thread_fast.conversion_factors as cf


class Nut:
    """Nut class.
    
    Contains internal threads to mate with a fastener.
    
    Args:
        Do (float): outer bearing (abutment) diameter.
        length (float): nut length.
        thread (InternalMetricThread): nut thread.
        material (Material): nut material.
    """
    def __init__(
            self, 
            Do: float, 
            length: float,
            thread: InternalMetricThread, 
            material: Material,
        ):
        
        # outer bearing diameter (on abutment):
        assert Do > 0.0, "nut outer diamter must be > 0"
        self.Do = Do
        
        assert length > 0.0, "nut length must be > 0"
        self.length = length
        
        self.thread = thread
        
        self.material = material
    
    def PA_s_08307a(self, A_si: float) -> float:
        """Thread shear (pull out) load allowable, internal thread, PA_s.
        
        NSTS 08307A, pg A-4
        
        Args:
            A_si (float): 
        Returns:
            float: thread shear pull-out load allowable (internal thread)
        """
        PA_s = nsts_08307a.internal_thread_shear_load_allowable(
            A_si=A_si,
            F_su_nut=self.material.Ssu_mpa,
        )
        return PA_s
    
    def to_dict(self) -> dict:
        return {
            "type": 'Nut',
            "Do": self.Do,
            "length": self.length,
            "thread": self.thread.to_dict(),
            "material": self.material.to_dict(),
        }
    
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
        Sty_mpa=586.0,
        Stu_mpa=896.0,
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
    
    # to dictionary:
    nut1_dict = nut1.to_dict()
    print(nut1_dict)


if __name__ == "__main__":
    main()
    