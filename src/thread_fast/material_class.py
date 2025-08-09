"""Material Class Definition.

Critical Material Parameters:

- modulus of elasticity
- tensile yield strength
- tensile ultimate strength
- shear yield strength
- shear ultimate strength
- bearing (contact) yield strength
- bearing (contact) ultimate strength
- coefficient of thermal expansion

From NASA-TM-106943, pg 16:

Shear yield strength may be assumed to be 0.577 * tensile yield strength, per von Mises criterion.

From RP-1228 Fastener Design Manual (1990), pg 21:

Approximate Bearing Strength Allowables:

S_bu = 1.5 * S_tu (ultimate)

S_by = 1.5 * S_ty (yield)

where S_bu is ultimate bearing stress, S_by is yield bearing stress, and S_ty is tensile yield stress.

Subscript keys:

- S for stress or strength (sigma)
- _t = tensile
- _s = shear
- _c or _b = contact or bearing
- _y = yield
- _u = ultimate

"""
import json
import numpy as np
from dataclasses import dataclass


@dataclass
class Material:
    name: str
    E_mpa: float  # modulus of elastcity [MPa] = [N/mm^2]
    nu: float  # Poisson's ratio [-]
    Sty_mpa: float  # tensile yield strength [MPa] = [N/mm^2]
    Stu_mpa: float  # tensile ultimate strength [MPa] = [N/mm^2]
    cte_mm_mm_C: float  # coefficient of thermal expansion [mm/mm/C]
    rho_gcc: float  # density [g/cm^3]
    tc_w_mK: float  # thermal conductivity [W/m-K]
    hc_J_gC: float  # heat capacity [J/g-C]
    # override bearing or contact strength ???
    # override shear strength ???
    # hardness ??? (hardness - strength conversion, DIN-50150)
    
    @property
    def Scy_mpa(self) -> float:
        """Max contact stress yield allowable (bearing strength)
        based on von Mises yield criterion => Ss_max < 0.577 * Sy_all
        
        Ss_max = 0.335 * Sc_max
        
        Ss_max: max subsurface shear stress
        
        Sy_all: allowable tensile yield strength
        
        Sc_max: max applied contact surface stress
        
        0.577 / 0.335 = 1.723
        
        Just use RP-1228, pg 21.
        """
        # return (1.0/np.sqrt(3.0)) / 0.335 * self.Sy_mpa
        return 1.5 * self.Sty_mpa
    
    @property
    def Scu_mpa(self) -> float:
        """Max contact stress ultimate allowable (bearing strength) 
        
        Just use RP-1228, pg 21.
        """
        return 1.5 * self.Stu_mpa
        
    @property
    def Ssy_mpa(self) -> float:
        """Yield shear strength, in MPa.
        
        Shear yield strength may be assumed to be 0.577 * tensile yield strength, per von Mises criterion.
        
        1 / sqrt(3) = 0.57735
        """
        return self.Sty_mpa / np.sqrt(3.0)

    @property
    def Ssu_mpa(self) -> float:
        """Ultimate shear strength, in MPa.
        
        Shear yield strength may be assumed to be 0.577 * tensile yield strength, per von Mises criterion.
        
        1 / sqrt(3) = 0.57735
        """
        return self.Stu_mpa / np.sqrt(3.0)

    # TODO: from_dict()

    def to_dict(self) -> dict:
        """Create dictionary with material data."""
        return {
            'type': 'Material',
            'name': self.name,
            'E_mpa': self.E_mpa,  # modulus of elasticity
            'nu': self.nu,  # Poisson's ratio
            'cte_mm_mm_C': self.cte_mm_mm_C,  # coefficient of thermal expansion
            'rho_gcc': self.rho_gcc,  # density
            'tc_w_mK': self.tc_w_mK,  # thermal conductance
            'hc_J_gc': self.hc_J_gC,  # heat capacity
            'Sty_mpa': self.Sty_mpa,  # tensile yield
            'Stu_mpa': self.Stu_mpa,  # tensile ultimate 
            'Ssy_mpa': self.Ssy_mpa,  # shear yield
            'Ssu_mpa': self.Ssu_mpa,  # shear ultimate
            'Scy_mpa': self.Scy_mpa,  # contact yield
            'Scu_mpa': self.Scu_mpa,  # contact ultimate
        }
    
    
def main() -> None:
    
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
    print(a286)
    
    inconel_718 = Material(
        name='inconel_718',
        E_mpa=200.0e3,
        nu=0.29,
        rho_gcc=8.19,
        cte_mm_mm_C=13.0e-6,
        tc_w_mK=11.4,
        hc_J_gC=0.435,
        Sty_mpa=1100.0,
        Stu_mpa=1375.0,
    )
    print(inconel_718)
    
    stainless_steel_18_8 = Material(
        name='stainless_steel_18_8',
        E_mpa=200.0e3,
        nu=0.29,
        rho_gcc=8.0,
        cte_mm_mm_C=17.5e-6,
        tc_w_mK=16.2,
        hc_J_gC=0.5,
        Sty_mpa=215.0,
        Stu_mpa=505.0,
    )
    print(stainless_steel_18_8)
    
    ti6al4v = Material(
        name='ti6al4v',
        E_mpa=114.0e3,
        nu=0.342,
        rho_gcc=4.43,
        cte_mm_mm_C=8.6e-6,
        tc_w_mK=6.7,
        hc_J_gC=0.526,
        Sty_mpa=880.0,
        Stu_mpa=950.0,
    )
    print(ti6al4v)
    print(ti6al4v.Scy_mpa)
    
    # test to_dict:
    print(a286.to_dict())
    

if __name__ == "__main__":
    main()
    