import json

# Material Properties:
Material = {
    'E':200.0e3,  # modulus of elasticity
    'nu': 0.3,  # Poisson's ratio
    'sigma_ty': 85000.0 * psi_to_MPa,  # tensile yield strength
    'sigma_tu': 100000.0 * psi_to_MPa,  # tensile ultimate strength
    'cte': 16.9e-6,  # coefficient of thermal expansion
}

# Temperatures:
Temperature = {
    'T_amb': 20.0,  # ambient temperature
    'T_min': 0.0,  # minimum temperature
    'T_max': 40.0,  # maximum temperature
}

# Friction Assumptions:
Friction = {
    'mu_thread': 0.15,  # coefficient of friction between threads
    'mu_head': 0.15,  # coefficient of friction between bolt head or nut with abutment
}


# Fastener:
Fastener = {
    'D': 5.0,  # fastener nominal diameter
    'L': 20.0,  # length of clamped joint
    # length of shank
    # threaded length of fastener
}

# Fastener Thread:
bolt_thread = {
    'D_major': 4.976,  # fastener major (outer) diameter
    'D_minor': 4.134,  # fastener minor diameter
    'pitch': 0.8,  # thread screw pitch
    'alpha': 60.0 * deg_to_rad, # thread angle
}

# Design / Application Assumptions:
design = {
    'relaxation_ratio': 0.05,  # preload relaxation due to settling, embedment, etc.
    'preload_stress_ratio': 0.65,  # target yield stress ratio due to preload
    'u': 0.25,  # preload uncertainty_factor, due to preloading method
    'config': 1,  # through bolt with nut, or bolt into insert
    'threads_in_shear_plane': False, # are the threads in the shear plane? 
    'separation_critical': False, # is the application separation critical?
}

# Washer:
washer = {
    'L': 0.5,  # washer thickness (clamped length)
    'Material': Material,  # washer material
}

# External Loading:
Load = {
    'P_et': 100.0,  # total externally applied axial load
    # shear load
    # bending load
}


def generate_inputs(
        SF_u: float, 
        SF_y: float,
        SF_sep: float,
    ) -> dict:
    """
    
    Args:
        SF_u: ultimate safety factor
        SF_y: yield safety factor
        SF_sep: joint separation safety factor
    """
    assert SF_u >= 1.0
    assert SF_y >= 1.0
    
    # Safety Factors:
    safety_factors = {
        'SF_u': SF_u,
        'SF_y': SF_y,
        'SF_sep': SF_sep,  # safety factor against joint separation
    }
    
    input_dict = {
        'safety_factor': safety_factors,
    }
    return input_dict


def main() -> None:
    
    Sf_u = 1.2
    Sf_y = 1.1
    Sf_sep = 1.2
    
    
if __name__ == "__main__":
    main()
    