"""
Use functional programming instead of object oriented...

focus on web-app interface...

Goal: user can input as little or as much as they want...

Also try going unitless...

Parameters:

- name: material descriptor
- E: modulus of elasticity
- nu: Poisson's ratio
- rho: density (not really needed)
- cte: coefficient of thermal expansion
- tc: thermal conductance (not really needed)
- hc: heat capacity (not really needed)
- Sty: tensile yield strength (stress)
- Stu: tensile ultimate strength (stress)
- Ssy: shear yield strength (stress)
- Ssu: shear ultimate strength (stress)
- Scy: contact (bearing) yield strength (stress)
- Scu: contact (bearing) ultimate strength (stress)
"""
import numpy as np


def calc_Scy(Sty: float) -> float:
    """Max contact stress yield allowable (bearing strength)
    based on von Mises yield criterion => Ss_max < 0.577 * Sty_all
    
    Ss_max = 0.335 * Sc_max
    
    Ss_max: max subsurface shear stress
    
    Sty_all: allowable tensile yield strength
    
    Sc_max: max applied contact surface stress
    
    0.577 / 0.335 = 1.723
    
    Just use RP-1228, pg 21.
    """
    return 1.5 * Sty


def calc_Scu(Stu: float) -> float:
    """Max contact stress ultimate allowable (bearing strength) 
    
    Just use RP-1228, pg 21.
    """
    return 1.5 * Stu


def calc_Ssy_mpa(Sty: float) -> float:
    """Yield shear strength, in MPa.
    
    Shear yield strength may be assumed to be 0.577 * tensile yield strength, per von Mises criterion.
    
    1 / sqrt(3) = 0.57735
    """
    return Sty / np.sqrt(3.0)

def calc_Ssu_mpa(Stu: float) -> float:
    """Ultimate shear strength, in MPa.
    
    Shear yield strength may be assumed to be 0.577 * tensile yield strength, per von Mises criterion.
    
    1 / sqrt(3) = 0.57735
    """
    return Stu / np.sqrt(3.0)


def process_material_input(input_dict: dict):
    """
    modify the input dict to ensure completeness
    
    Must supply:
    - name: descriptor
    - E: modulus of elasticity
    - nu: Poisson's ratio
    - cte: coefficient of thermal expansion
    - Sty: tensile yield strength
    - Stu: tensile ultimate strength
    
    Optional:
    - Ssy: shear yield strength
    - Ssu: shear ultimate strength
    - Scy: contact (bearing) yield strength
    - Scu: contact (bearing) ulimate strength
    """
    assert input_dict['type'] == 'Material', "material type must be Material"
    
    assert input_dict.get('name') is not None
    
    assert input_dict['E'] > 0.0
    
    assert input_dict['nu'] > 0.0
    
    assert input_dict['cte'] >= 0.0
    
    assert input_dict['Sty'] > 0.0
    
    assert input_dict['Stu'] > 0.0
    
    # check / fill contact yield strength:
    if input_dict.get('Scy') is None:
        input_dict['Scy'] = calc_Scy(input_dict['Sty'])
    else:
        assert input_dict['Scy'] >= 0.0
    
    # check / fill contact ultimate strength:
    if input_dict.get('Scu') is None:
        input_dict['Scu'] = calc_Scu(input_dict['Stu'])
    else:
        assert input_dict['Scu'] >= 0.0
    
    # check / fill shear yield strength:
    if input_dict.get('Ssy') is None:
        input_dict['Ssy'] = input_dict['Sty'] / np.sqrt(3.0)
    else:
        assert input_dict['Ssy'] >= 0.0
    
    # check / fill shear ultimate strength:
    if input_dict.get('Ssu') is None:
        input_dict['Ssu'] = input_dict['Stu'] / np.sqrt(3.0)
    else:
        assert input_dict['Ssu'] >= 0.0
    
    return input_dict


def main() -> None:
    
    input_dict = {
        'type': 'Material',
        'name': 'test_input_dict',
        'E': 200000.0,  # modulus of elasticity
        'nu': 0.3,  # Poisson's ratio
        # 'rho': 8.0,  # density
        'cte': 2.0e-6,  # coefficient of thermal expansion
        #'tc': 12.0,  # thermal conductance
        #'hc': 0.5,  # heat capacity
        'Sty': 600.0,  # tensile yield strength
        'Stu': 800.0,  # tensile ultimate strength
        'Ssy': 340.0,  # shear yield strength
        'Ssu': 520.0,  # shear ultimate strength
        'Scy': 900.0,  # contact (bearing) yield strength
        'Scu': 1200.0,  # contact (bearing) ultimate strength
    }
    print(f"\ninput_dict = \n{input_dict}\n")
    
    output_dict = process_material_input(input_dict)
    print(f"\noutput_dict = \n{output_dict}\n")
    
    input_dict = {
        'type': 'Material',
        'name': 'test_input_dict',
        'E': 200000.0,  # modulus of elasticity
        'nu': 0.3,  # Poisson's ratio
        # 'rho': 8.0,  # density
        'cte': 2.0e-6,  # coefficient of thermal expansion
        #'tc': 12.0,  # thermal conductance
        #'hc': 0.5,  # heat capacity
        'Sty': 600.0,  # tensile yield strength
        'Stu': 800.0,  # tensile ultimate strength
        # 'Ssy': 340.0,  # shear yield strength
        # 'Ssu': 520.0,  # shear ultimate strength
        # 'Scy': 900.0,  # contact (bearing) yield strength
        # 'Scu': 1200.0,  # contact (bearing) ultimate strength
    }
    print(f"\ninput_dict = \n{input_dict}\n")
    
    output_dict = process_material_input(input_dict)
    print(f"\noutput_dict = \n{output_dict}\n")
    
    input_dict = {
        'type': 'Material',
        'name': 'test_input_dict',
        'E': 200000.0,  # modulus of elasticity
        'nu': 0.3,  # Poisson's ratio
        # 'rho': 8.0,  # density
        'cte': 2.0e-6,  # coefficient of thermal expansion
        #'tc': 12.0,  # thermal conductance
        #'hc': 0.5,  # heat capacity
        'Sty': 600.0,  # tensile yield strength
        'Stu': 800.0,  # tensile ultimate strength
        'Ssy': None,  # shear yield strength
        'Ssu': None,  # shear ultimate strength
        'Scy': None,  # contact (bearing) yield strength
        'Scu': None,  # contact (bearing) ultimate strength
    }
    print(f"\ninput_dict = \n{input_dict}\n")
    
    output_dict = process_material_input(input_dict)
    print(f"\noutput_dict = \n{output_dict}\n")
    
    
if __name__ == "__main__":
    main()
    