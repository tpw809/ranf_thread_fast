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

From NASA-RP-1228 Fastener Design Manual (1990), pg 21:

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

Units (trying to go unitless):

Metric:
length: mm
load: N
E: MPa
nu: n/a
cte: mm/mm/C
rho: gcc = gram/cubic centimeter
tc: W/(m-K)
hc: J/(g-C)
Sty: MPa = N/mm^2
Stu: MPa = N/mm^2
Scy: MPa = N/mm^2
Scu: MPa = N/mm^2
Ssy: MPa = N/mm^2
Ssu: MPa = N/mm^2

English:
length: in
load: lb
E: psi
nu: n/a
cte: in/in/F
rho:
tc:
hc:
Sty:psi
Stu: psi
Scy: psi
Scu: psi
Ssy: psi
Ssu: psi
"""
import json
import numpy as np
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Material:
    name: str
    E: float  # modulus of elastcity
    nu: float  # Poisson's ratio
    cte: float  # coefficient of thermal expansion
    rho: float  # density
    tc: float  # thermal conductivity
    hc: float  # heat capacity
    Sty: float  # tensile yield strength
    Stu: float  # tensile ultimate strength
    # override bearing or contact strength ???
    # override shear strength ???
    # hardness ??? (hardness - strength conversion, DIN-50150)
    Scy: float=None  # contact yield strength
    Scu: float=None  # contact ultimate strength
    Ssy: float=None  # shear yield strength
    Ssu: float=None  # shear ultimate strength
    
    def __post_init__(self):
        if self.Scy is None:
            self.Scy = self.calc_Scy()
        if self.Scu is None:
            self.Scu = self.calc_Scu()
        if self.Ssy is None:
            self.Ssy = self.calc_Ssy()
        if self.Ssu is None:
            self.Ssu = self.calc_Ssu()
    
    def calc_Scy(self) -> float:
        """Max contact stress yield allowable (bearing strength)
        based on von Mises yield criterion => Ss_max < 0.577 * Sy_all
        
        Ss_max = 0.335 * Sc_max
        
        Ss_max: max subsurface shear stress
        
        Sy_all: allowable tensile yield strength
        
        Sc_max: max applied contact surface stress
        
        0.577 / 0.335 = 1.723
        
        Just use NASA-RP-1228, pg 21.
        """
        # return (1.0/np.sqrt(3.0)) / 0.335 * self.Sy
        return 1.5 * self.Sty
    
    def calc_Scu(self) -> float:
        """Max contact stress ultimate allowable (bearing strength) 
        
        Just use NASA-RP-1228, pg 21.
        """
        return 1.5 * self.Stu
        
    def calc_Ssy(self) -> float:
        """Yield shear strength.
        
        Shear yield strength may be assumed to be 0.577 * tensile yield strength, per von Mises criterion.
        
        1 / sqrt(3) = 0.57735
        """
        return self.Sty / np.sqrt(3.0)

    def calc_Ssu(self) -> float:
        """Ultimate shear strength.
        
        Shear yield strength may be assumed to be 0.577 * tensile yield strength, per von Mises criterion.
        
        1 / sqrt(3) = 0.57735
        """
        return self.Stu / np.sqrt(3.0)

    @classmethod
    def from_dict(cls, input_dict):
        """Create a Material object from input dictionary.
        
        Mandatory items:
        - name
        - E: modulus of elasticity
        - nu: Poisson's ratio
        - cte: coefficient of thermal expansion
        - Sty: tensile yield strength
        - Stu: tensile ultimate strength
        - rho: density
        - tc: thermal conductivity
        - hc: heat capacity
        
        Optional:
        - Scy:
        - Scu:
        - Ssy:
        - Ssu:
        """
        assert input_dict['type'] == 'Material'
        
        if 'Scy' in input_dict:
            Scy = input_dict['Scy']
        else:
            Scy = None
        
        if 'Scu' in input_dict:
            Scu = input_dict['Scu']
        else:
            Scu = None
        
        if 'Ssy' in input_dict:
            Ssy = input_dict['Ssy']
        else:
            Ssy = None
        
        if 'Ssu' in input_dict:
            Ssu = input_dict['Ssu']
        else:
            Ssu = None
        
        mat = Material(
            name=input_dict['name'],
            E=input_dict['E'],
            nu=input_dict['nu'],
            rho=input_dict['rho'],
            cte=input_dict['cte'],
            tc=input_dict['tc'],
            hc=input_dict['hc'],
            Sty=input_dict['Sty'],
            Stu=input_dict['Stu'],
            Scy=Scy,
            Scu=Scu,
            Ssy=Ssy,
            Ssu=Ssu,
        )
        return mat
        
    def to_dict(self) -> dict:
        """Create dictionary with material data."""
        return {
            'type': 'Material',
            'name': self.name,
            'E': self.E,  # modulus of elasticity
            'nu': self.nu,  # Poisson's ratio
            'cte': self.cte,  # coefficient of thermal expansion
            'rho': self.rho,  # density
            'tc': self.tc,  # thermal conductance
            'hc': self.hc,  # heat capacity
            'Sty': self.Sty,  # tensile yield
            'Stu': self.Stu,  # tensile ultimate 
            'Ssy': self.Ssy,  # shear yield
            'Ssu': self.Ssu,  # shear ultimate
            'Scy': self.Scy,  # contact yield
            'Scu': self.Scu,  # contact ultimate
        }
        
    def to_json(self):
        """Returns json object from dictionary."""
        return json.dumps(self.to_dict())

    def write_to_json(self, filename: str or Path):
        """Save json data to a file."""
        with open(filename, "w") as f:
            f.write(self.to_json())


def main() -> None:
    
    a286 = Material(
        name='a286',
        E=200.0e3,
        nu=0.3,
        rho=7.93,
        cte=16.5e-6,
        tc=15.1,
        hc=420.0/1000.0,
        Sty=586.0,
        Stu=896.0,
    )
    print(a286)
    
    inconel_718 = Material(
        name='inconel_718',
        E=200.0e3,
        nu=0.29,
        rho=8.19,
        cte=13.0e-6,
        tc=11.4,
        hc=0.435,
        Sty=1100.0,
        Stu=1375.0,
    )
    print(inconel_718)
    
    stainless_steel_18_8 = Material(
        name='stainless_steel_18_8',
        E=200.0e3,
        nu=0.29,
        rho=8.0,
        cte=17.5e-6,
        tc=16.2,
        hc=0.5,
        Sty=215.0,
        Stu=505.0,
    )
    print(stainless_steel_18_8)
    
    ti6al4v = Material(
        name='ti6al4v',
        E=114.0e3,
        nu=0.342,
        rho=4.43,
        cte=8.6e-6,
        tc=6.7,
        hc=0.526,
        Sty=880.0,
        Stu=950.0,
    )
    print(ti6al4v)
    print(ti6al4v.Scy)
    
    ti6al4v_material_dict = {
        'type': 'Material',
        'name': 'ti6al4v',
        'E': 114.0e3,  # modulus of elasticity
        'nu': 0.342,  # Poisson's ratio
        'cte': 8.6e-6,  # coefficient of thermal expansion
        'Sty': 880.0,  # tensile yield strength
        'Stu': 950.0,  # tensile ultimate strength
    }
    
    # MP35N:
    
    
    # test to_dict:
    output_dict = a286.to_dict()
    print(output_dict)
    
    mat_copy = Material.from_dict(output_dict)
    print(mat_copy)
    
    input_dict = {
        'type': 'Material',
        'name': 'test_input_dict',
        'E': 200000.0,
        'nu': 0.3,
        'rho': 8.0,
        'cte': 2.0e-6,
        'tc': 12.0,
        'hc': 0.5,
        'Sty': 600.0,
        'Stu': 800.0,
        'Ssy': 340.0,
        'Ssu': 520.0,
        'Scy': 900.0,
        'Scu': 1200.0,
    }
    
    test_input_dict_mat = Material.from_dict(input_dict)
    print(test_input_dict_mat)
    

if __name__ == "__main__":
    main()
    