"""Process input and return validated and completed data.

Parameters:

- type: 'ClampedPart'
- name: descriptor
- material: 
- thickness:
- D_hole: hole (inner) diameter
- D_outer: outer diameter

Processed Outputs:

- area
- stiffness
"""
import json
import numpy as np

import thread_fast.conversion_factors as cf
from thread_fast.materials.material_class import Material
from thread_fast.materials.process_material_input import process_material_input


def process_clamped_part_input(input_dict: dict):
    """Read and modify the input dict to ensure completeness and validity.
    
    Must supply:
    - type: 'ClampedPart'
    - name: description
    - material: material data dictionary
    - thickness: thickness of the part
    - D_hole: hole (inner) diameter
    - D_outer: outer diameter (bearing area)
    """
    # check type:
    assert input_dict['type'] == 'ClampedPart'
    
    # check if this data has already been processed:
    if input_dict.get('processed_bool') == True:
        return input_dict
    
    # check required inputs:
    assert 'name' in input_dict
    assert 'material' in input_dict
    assert 'D_hole' in input_dict
    assert 'D_outer' in input_dict
    assert 'thickness' in input_dict
    
    D_hole = input_dict['D_hole']
    D_outer = input_dict['D_outer']
    thickness = input_dict['thickness']
    
    # hole diameter:
    assert D_hole > 0.0, "clamped part hole diamter must be > 0"
    
    # outer diameter:
    assert D_outer > D_hole, "clamped part outer diamter must be > hole diameter"
    
    assert thickness > 0.0, "clamped part thickness must be > 0"
    
    # TODO: limit area to under head or nut...
    if input_dict.get('area') is None:
        print("calculating area for clamped part...")
        ro = D_outer / 2.0
        ri = D_hole / 2.0
        area = np.pi * (ro**2 - ri**2)
        input_dict['area'] = area
    else:
        assert input_dict['area'] > 0.0
    
    # TODO: update stiffness estimate... frustum volume
    
    # estimated stiffness: k = (A * E) / L
    if input_dict.get('stiffness') is None:
        print("calculating stiffness for clamped part...")
        stiffness = input_dict['area'] * input_dict['material']['E'] / thickness
        input_dict['stiffness'] = stiffness
    else:
        assert input_dict['stiffness'] > 0.0
    
    # add 'processed' tag:
    input_dict['processed_bool'] = True
    
    return input_dict


def main() -> None:
    
    print("\nMaterial:")
    material_dict = {
        'type': 'Material',
        'name': 'test_input_dict',
        'E': 200000.0,  # modulus of elasticity
        'nu': 0.3,  # Poisson's ratio
        'cte': 2.0e-6,  # coefficient of thermal expansion
        'Sty': 600.0,  # tensile yield strength
        'Stu': 800.0,  # tensile ultimate strength
    }

    material_dict = process_material_input(material_dict)
    print(f"\nmaterial_dict: \n")
    print(json.dumps(material_dict, indent=4))
    
    print("\nClampedPart:")
    input_dict = {
        'type': 'ClampedPart',
        'name': 'clamped_part_test_input_dict',
        'material': material_dict,
        'D_hole': 6.1,
        'D_outer': 8.5,
        'thickness': 5.0,
    }

    output_dict = process_clamped_part_input(input_dict)
    print(f"\noutput: \n")
    print(json.dumps(output_dict, indent=4))
    

if __name__ == "__main__":
    main()
    