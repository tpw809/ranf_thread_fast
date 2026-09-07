"""ClampedPart class definition.

ClampedPart consists of:

- material
- length (thickness)
- minimum distance of edge to bolt hole


"""
import numpy as np
from thread_fast.materials.material_class import Material


class ClampedPart:
    def __init__(
            self, 
            name: str, 
            D_hole: float, 
            D_outer: float, 
            thickness: float,
            material: Material,
        ):
        
        assert D_hole >= 0.0
        assert D_outer > D_hole
        assert thickness > 0.0
        
        self.name = name
        
        # diameter of the fastener hole:
        self.D_hole = D_hole
        
        self.D_outer = D_outer
        
        self.thickness = thickness
        
        self.material = material
        
    @property
    def length(self) -> float:
        """length, mm or in."""
        return self.thickness
        
    def area(self) -> float:
        """area, mm^2 or in^2"""
        ro = self.D_outer / 2.0
        ri = self.D_hole / 2.0
        return np.pi * (ro**2 - ri**2)
        
    def stiffness(self) -> float:
        """axial stiffness, N/mm or lb/in.
        
        k = (A * E) / L
        """
        # TODO: fix stiffness (frustum volume)
        return (self.area() * self.material.E) / self.thickness

    def __str__(self):
        return "\n".join([
            "\nClampedPart:",
            f"name = {self.name}",
            f"D_hole = {self.D_hole}",
            f"D_outer = {self.D_outer}",
            f"thickness = {self.thickness}",
            f"\n{self.material}",
            "",
        ])


def main() -> None:
    # Tests:
    
    ti6al4v = Material(
        name='ti6al4v',
        E=114.0e3,
        nu=0.342,
        rho=4.43,
        cte=8.6e-6,
        tc=6.7,
        hc=0.526,
        Sy=880.0,
        Su=950.0,
    )
    
    part1 = ClampedPart(
        name='part1',
        D_hole = 5.2,
        D_outer=8.5,
        thickness=0.4,
        material=ti6al4v,
    )
    
    print(part1)
    print(part1.area())
    print(part1.material.E)
    print(part1.stiffness())


if __name__ == "__main__":
    main()
    