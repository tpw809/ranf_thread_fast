"""Washer class definition.

Standards:

- ISO 7089
- ISO 7416
- MS 14183
- DIN 125
- DIN 125A (Not chamfered)

"""
import numpy as np
from thread_fast.material_class import Material


class Washer:
    def __init__(
            self, 
            nominal_size, 
            D_hole: float, 
            D_outer: float, 
            thickness: float,
            material: Material,
            # chamfer: bool=True,
        ):
        
        assert D_hole >= 0.0
        assert D_outer > D_hole
        assert thickness > 0.0
        
        self.nominal_size = nominal_size
        
        self.D_hole = D_hole
        
        self.D_outer = D_outer
        
        self.thickness = thickness
        
        self.material = material
        
        # self.chamfer = chamfer

    @property
    def length(self) -> float:
        """length, mm."""
        return self.thickness
        
    def area(self) -> float:
        """area, mm^2"""
        ro = self.D_outer / 2.0
        ri = self.D_hole / 2.0
        return np.pi * (ro**2 - ri**2)
        
    def stiffness(self) -> float:
        """axial stiffness, N/mm.
        
        k = (A * E) / L
        """
        return (self.area() * self.material.E_mpa) / self.thickness

    def __str__(self):
        return "\n".join([
            "\nWasher:",
            f"nominal_size = {self.nominal_size}",
            f"D_hole = {self.D_hole}",
            f"D_outer = {self.D_outer}",
            f"thickness = {self.thickness}",
            f"area = {self.area}",
            f"stiffness = {self.stiffness}",
            f"\n{self.material}",
            "",
        ])


def main() -> None:
    # Tests:
    
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
    
    washer1 = Washer(
        nominal_size=5.0,
        D_hole = 5.2,
        D_outer=8.5,
        thickness=0.4,
        material=inconel_718,
        # chamfer=True,
    )
    
    print(washer1)
    print(washer1.area())
    print(washer1.material.E_mpa)
    print(washer1.stiffness())


if __name__ == "__main__":
    main()
    