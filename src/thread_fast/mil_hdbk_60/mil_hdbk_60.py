"""Equations from MIL-HDBK-60

Military Handbook 

Threaded Fastener - Tightening to Proper Tension
"""


# 6.2.1 Micrometer Method:


def bolt_elongation(
        f_t: float, 
        L_b: float, 
        E: float,
    ) -> float:
    """Calculate elongation of the bolt due to preload.
    
    MIL-HDBK-60, pg 12
    
    Args:
        f_t: axial stress (psi or MPa)
        L_b: effective bolt length (inch or mm)
        E: modulus of elasticity (psi or MPa)
    Returns:
        float: elongation of the bolt due to preload
    """
    delta_B = f_t * L_b / E
    return delta_B


# 6.2.4 Turn-of-nut method:


def nut_turns_deg(
        f_t: float, 
        L_b: float, 
        E: float, 
        lead: float,
    ) -> float:
    """Calculate turn of nut in degrees for desired preload.
    
    MIL-HDBK-60, pg 14
    
    Args:
        f_t: axial stress (psi or MPa)
        L_b: effective bolt length (inch or mm)
        E: modulus of elasticity (psi or MPa)
        lead: lead of the thread helix (inch or mm)
    Returns:
        float: turn of nut in degrees
    """
    theta = f_t * L_b / (E * lead)
    return theta


def main() -> None:
    pass


if __name__ == "__main__":
    main()
    