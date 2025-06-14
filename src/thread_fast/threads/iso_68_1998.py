"""Equations from ISO 68:1998

ISO general purpose screw threads - Basic profile

Part 1: Metric screw threads
Part 2: Inch screw threads

Standards:
-ISO 965-1:1998, ISO general purpose metric screw threads — Tolerances — Part 1: Principles and basic data
-ISO 5408:1983, Cylindrical screw threads — Vocabulary

Symbols:
-D: basic major diameter of internal thread (nominal diameter)
-d: basic major diameter of external thread (nominal diameter)
-D2:basic pitch diameter of internal thread
-d2: basic pitch diameter of external thread
-D1: basic minor diameter of internal thread
-d1: basic minor diameter of external thread
-H: height of fundamental triangle
-P: thread pitch

#TODO: add figure
"""
import numpy as np


def eq_H(P: float) -> float:
    """Calculate height of fundamental triangle, H.
    
    ISO 68
    
    Args:
        P: thread pitch
    Returns:
        float: height of fundamental triangle
    """
    assert P > 0.0
    H = (np.sqrt(3.0) / 2.0) * P
    return H


def main() -> None:
    # [mm/thread], thread pitch:
    pitch = 1.0
    
    # [mm], height of fundamental triangle:
    H = eq_H(pitch)
    print(f"H = {H} [mm]")
    
    print(f"5/8H = {(5.0/8.0)*H}")
    print(f"3/8H = {(3.0/8.0)*H}")
    print(f"H/4 = {H/4.0}")
    print(f"H/8 = {H/8.0}")


if __name__ == "__main__":
    main()
    