"""Helix Angle.

From Wikipedia:
helix angle is the angle between any helix and an axial line on its right, circular cylinder or cone

the helix angle can be found by unraveling the helix from the screw, representing the section as a right triangle, and calculating the angle that is formed

What is used in the calculations (NASA-TM-106943) is actually lead angle, not helix angle.
"""
import numpy as np


def helix_angle(r_m: float, lead: float) -> float:
    """Calculate helix angle of the screw threads.
    
    Angle between axis of screw and thread.
    
    Args:
        r_m: mean radius of the screw thread
        lead: lead of the screw thread
    Returns:
        float: helix angle of screw threads
    """
    return np.arctan(2.0 * np.pi * r_m / lead)


def lead_angle(r_m: float, lead: float) -> float:
    """Calculate lead angle of the screw threads.
    
    Angle from line perpendicular to axis to thread.
    
    Args:
        r_m: mean radius of the screw thread
        lead: lead of the screw thread
    Returns:
        float: lead angle of screw threads
    """
    return np.arctan(lead / (2.0 * np.pi * r_m))
    

def main() -> None:
    # screw thread pitch:
    pitch = 0.8
    
    # screw thread mean radius:
    r_m = 2.3
    
    psi = lead_angle(r_m=r_m, lead=pitch)
    print(f"psi = {psi} [rad]")


if __name__ == "__main__":
    main()
    