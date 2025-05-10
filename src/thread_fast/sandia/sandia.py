import json
import numpy as np



inputs = {
    'bolt': {
        'bolt_diameter': 5.0/8.0,
        'head_diameter': ,
        'elastic_modulus': 30.0e6,
        'yield_strength': ,
        'ultimate_strength': ,
        'tensile_area': ,
        'min_pitch_diameter_external': ,
        'min_major_diameter_external': ,
        'coefficient_thermal_expansion': 0.0000096,
    },
    'thread': {
        'threads_per_inch': 11,
        'lead_angle': ,
        'half_angle': ,  # 30 degrees for unified threads
    },
    'joint': {
        'n_layers': 2,
        'use_shigley': False,
        'threaded_layer': False,  # is bottom layer threaded or through?
    },
    'top_layer': {
        'elastic_modulus': 30.0e6,
        'yield_strength': 100000.0,
        'ultimate_strength': ,
        'thickness': ,
        'coefficient_thermal_expansion': 0.0000096,
    },
    'middle_layer': {
        'elastic_modulus': 30.0e6,
        'yield_strength': 100000.0,
        'ultimate_strength': ,
        'thickness': ,
        'coefficient_thermal_expansion': ,
    },
    'bottom_layer': {
        'elastic_modulus': 30.0e6,
        'yield_strength': 100000.0,
        'ultimate_strength': ,
        'thickness': ,
        'coefficient_thermal_expansion': ,
    },
    
    'preload': {
        'torque': 1.0,
        'uncertainty': 0.35,
        'preload_loss_percent': 0.05,
        'nut_factor_method': 'manual',
        'nut_factor_manual': 0.2,
    },
    'applied_load': {
        'F_axial': 0.0,
        'F_shear': 0.0,
        'M_bending': 0.0,
    },
    'environment': {
        'T_ambient': 20.0,
        'T_hot': 60.0,
        'T_cold': -24.0,
    }
    'factors_of_safety': {
        'yield': 1.2,
        'ultimate': 1.5,
    },
    'friction': {
        'mu_thread': 0.15,  # friction between threads
        'mu_head': 0.15,  # bearing surface on bolt head or nut
    },
}



def check_inputs(inputs):
    """Validate inputs.
    
    """
    
    
    # check temperatures:
    T_amb = inputs.environment.T_ambient
    T_hot = inputs.environment.T_hot
    T_cold = inputs.environment.T_cold

    assert T_hot >= T_amb
    assert T_amb >= T_cold
    
    
    SF_yield = inputs.factors_of_safety.yield
    SF_ultimate = inputs.factors_of_safety.ultimate

    assert SF_yield > 1.0
    assert SF_ultimate > 1.0
    
    
def main() -> None:
    
    check_inputs(inputs)


if __name__ == "__main__":
    main()
    