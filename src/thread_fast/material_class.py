"""Material Class

Critical Material Parameters:
-modulus of elasticity
-tensile yield strength
-tensile ultimate strength
-shear yield strength
-shear ultimate strength
-bearing (contact) yield strength
-bearing (contact) ultimate strength
-coefficient of thermal expansion

shear yield strength may be assumed to be 0.577 * tensile yield strength, per von Mises criterion

From RP-1228 Fastener Design Manual:

Approximate Bearing and Allowables:

S_bu = 1.5 * S_tu

S_by = 1.5 * S_ty

where S_bu is ultimate bearing stress, S_by is yeild bearing stress, and S_ty is tensile yield stress.

Subscript keys:
S for stress or strength
_t = tensile
_s = shear
_c or _b = contact or bearing
_y = yield
_u = ultimate

"""
import json
import numpy as np
from dataclasses import dataclass


@dataclass
class Material:
    name: str
    E_mpa: float  # modulus of elastcity [MPa] = [N/mm^2]
    nu: float  # Poisson's ratio [-]
    Sy_mpa: float  # tensile yield strength [MPa] = [N/mm^2]
    Su_mpa: float  # tensile ultimate strength [MPa] = [N/mm^2]
    cte_mm_mm_C: float  # coefficient of thermal expansion [mm/mm/C]
    rho_gcc: float  # density [g/cm^3]
    tc_w_mK: float  # thermal conductivity [W/m-K]
    hc_J_gC: float  # heat capacity [J/g-C]
    
    @property
    def Sc_mpa(self) -> float:
        """Max contact stress allowable (bearing strength)
        based on von Mises yield criterion => Ss_max < 0.577 * Sy_all
        
        Ss_max = 0.335 * Sc_max
        
        Ss_max = max subsurface shear stress
        
        Sy_all = allowable tensile yield strength
        
        Sc_max = max applied contact surface stress
        """
        return (1.0/np.sqrt(3.0)) / 0.335 * self.Sy_mpa

    def to_dict(self) -> dict:
        """Create dictionary with material data."""
        return {
            'name': self.name,
            'E_mpa': self.E_mpa,
            'nu': self.nu,
            'Sy_mpa': self.Sy_mpa,
            'Su_mpa': self.Su_mpa,
            'cte_mm_mm_C': self.cte_mm_mm_C,
            'rho_gcc': self.rho_gcc,
            'tc_w_mK': self.tc_w_mK,
            'hc_J_gc': self.hc_J_gC,
        }
    
    
def main() -> None:
    
    a286 = Material(
        name='a286',
        E_mpa='200.0e3',
        nu=0.3,
        rho_gcc=7.93,
        cte_mm_mm_C=16.5e-6,
        tc_w_mK=15.1,
        hc_J_gC=420.0/1000.0,
        Sy_mpa=586.0,
        Su_mpa=896.0,
    )
    print(a286)
    

if __name__ == "__main__":
    main()
    