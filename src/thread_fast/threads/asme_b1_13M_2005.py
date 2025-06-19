"""ASME B1.13M 2005 (R2015) Metric Screw Threads: M Profile

Symbols:
-D: Major diameter internal thread
-D1: Minor diameter internal thread
-D2: Pitch diameter internal thread
-d: Major diameter external thread
-d1: Minor diameter external thread
-d2: Pitch diameter external thread
-d3: Rounded form minor diameter external thread
-P: Pitch
-r: External thread root radius
-T: Tolerance
-TD1, TD2: Tolerances for D1, D2
-Td, Td2: Tolerances for d, d2
-ES: Upper deviation, internal thread [equals the allowance (fundamental deviation)
-EI: Lower deviation, internal thread allowance (fundamental deviation).
-G, H: Letter designations for tolerance positions for lower deviation, internal thread
-g, h: Letter designations for tolerance positions
for upper deviation, external thread
-es: Upper deviation, external thread allowance (fundamental deviation). In the ISO System, es is always negative for an allowance fit or zero for no allowance.
-ei: Lower deviation, external thread [equals the allowance (fundamental deviation) plus the tolerance]. In the ISO system, ei is always negative for an allowance fit.
-H: Height of fundamental triangle
-LE: Length of engagement
-LH: Left hand thread

H = np.sqrt(3) / 2.0 * P
"""
import numpy as np


# Table 10 pitch list:
pitch_list = [
    0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.75,
    0.8, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.5, 4.0, 
    4.5, 5.0, 5.5, 6.0, 8.0,
]


def eq_EI(
        P: float, 
        allowance_class: str,
    ) -> float:
    """Calculate internal thread allowance (fundamental deviation), EI.
    
    ASME B1.13M-2005, pg 15
    
    Args:
        P: thread pitch
        allowance_class: 
    """
    assert P > 0.0
    
    EI_G = 0.015 + 0.011 * P
    EI_H = 0.0
    
    if allowance_class == 'G':
        return EI_G
    elif allowance_class == 'H':
        return EI_H
    else:
        raise Exception("allowance_class must be [G, H]")
    

def eq_es(
        P: float, 
        allowance_class: str,
    ) -> float:
    """Calculate external thread allowance (fundamental deviation), es.
    
    ASME B1.13M-2005, pg 15
    
    Args:
        P: thread pitch
        allowance_class: 
    """
    assert P > 0.0
    
    es_e = -(0.05 + 0.011 * P)
    es_f = -(0.03 + 0.011 * P)
    es_g = -(0.015 + 0.011 * P)
    es_h = 0.0
    
    if allowance_class == 'e':
        return es_e
    elif allowance_class == 'f':
        return es_f
    elif allowance_class == 'g':
        return es_g
    elif allowance_class == 'h':
        return es_h
    else:
        raise Exception("allowance_class must be [e,f,g,h]")


def eq_LE(P: float, d: float) -> tuple[float, float]:
    """Calculate length of thread engagement, LE.
    
    ASME B1.13M-2005, pg 15
    
    Args:
        P: thread pitch
        d: basic major diameter
    """
    assert P > 0.0
    assert d > 0.0
    
    LE_min = 2.24 * P * d**0.2
    LE_max = 6.7 * P * d**0.2
    return LE_min, LE_max


def eq_TD1_6(P: float) -> float:
    """Calculate tolerance , TD1_6.
    
    ASME B1.13M-2005, pg 15
    
    Args:
        P: thread pitch
    """
    assert P > 0.0
    
    TD1_6 = 0.433 * P - 0.19 * P**1.22

    if P >= 1.0:
        TD1_6 = 0.230 * P**0.7
    
    return TD1_6


def eq_TD1(P: float, tolerance_grade: int) -> float:
    """
    ASME B1.13M-2005, pg 15
    
    Args:
        P: thread pitch
        tolerance_grade:
    """
    assert P > 0.0
    
    TD1_6 = eq_TD1_6(P)
    
    TD1_4 = 0.63 * TD1_6
    TD1_5 = 0.8 * TD1_6
    TD1_7 = 1.25 * TD1_6
    TD1_8 = 1.6 * TD1_6
    
    if tolerance_grade == 4:
        return TD1_4
    elif tolerance_grade == 5:
        return TD1_5
    elif tolerance_grade == 6:
        return TD1_6
    elif tolerance_grade == 7:
        return TD1_7
    elif tolerance_grade == 8:
        return TD1_8
    else:
        raise Exception("tolerance_grade must be [4,6,8]")


def eq_Td_6(P: float) -> float:
    """Calculate tolerance for major diameter (external thread) at tolerance grade 6, Td_6. 
    
    ASME B1.13M-2005, pg 15
    
    Args:
        P: thread pitch
    """
    assert P > 0.0
    Td_6 = 0.18 * P**(2.0/3.0) - 0.00315 / np.sqrt(P)
    return Td_6


def eq_Td(P: float, tolerance_grade: int) -> float:
    """Calculate tolerance for major diameter (external thread), Td. 
    
    ASME B1.13M-2005, pg 15
    
    Args:
        P: thread pitch
        tolerance_grade:
    """
    assert P > 0.0
    
    Td_6 = eq_Td_6(P)
    Td_4 = 0.63 * Td_6
    Td_8 = 1.6 * Td_6
    
    if tolerance_grade == 4:
        return Td_4
    elif tolerance_grade == 6:
        return Td_6
    elif tolerance_grade == 8:
        return Td_8
    else:
        raise Exception("tolerance_grade must be [4,6,8]")


def eq_Td2_6(P: float, d: float) -> float:
    """Calculate tolerance for pitch diameter (external thread) at tolerance grade 6, Td2_6.
    
    ASME B1.13M-2005, pg 18
    
    Args:
        P: thread pitch
        d: basic major diameter
    """
    assert P > 0.0
    assert d > 0.0
    
    Td2_6 = 0.09 * P**0.4 * d**0.1
    return Td2_6


def eq_Td2(
        P: float, 
        d: float, 
        tolerance_grade: int,
    ) -> float:
    """Calculate tolerance for pitch diameter (external thread), Td2.
    
    ASME B1.13M-2005, pg 18
    
    Args:
        P: thread pitch
        d: basic major diameter
        tolerance_grade:
    """
    assert P > 0.0
    assert d > 0.0
    
    Td2_6 = eq_Td2_6(P, d)
    
    Td2_3 = 0.5 * Td2_6
    Td2_4 = 0.63 * Td2_6
    Td2_5 = 0.8 * Td2_6
    Td2_7 = 1.25 * Td2_6
    Td2_8 = 1.6 * Td2_6
    Td2_9 = 2.0 * Td2_6
    
    if tolerance_grade == 4:
        return Td2_4
    elif tolerance_grade == 5:
        return Td2_5
    elif tolerance_grade == 6:
        return Td2_6
    elif tolerance_grade == 7:
        return Td2_7
    elif tolerance_grade == 8:
        return Td2_8
    else:
        raise Exception("tolerance_grade must be [3,4,5,6,7,8,9]")


def eq_TD2(
        P: float, 
        d: float, 
        tolerance_grade: int,
    ) -> float:
    """Calculate tolerance for pitch diameter (internal thread), TD2.
    
    ASME B1.13M-2005, pg 19
    
    Args:
        P: thread pitch
        d: basic major diameter
        tolerance_grade:
    """
    assert P > 0.0
    assert d > 0.0
    
    Td2_6 = eq_Td2_6(P, d)
    
    TD2_4 = 0.85 * Td2_6
    TD2_5 = 1.06 * Td2_6
    TD2_6 = 1.32 * Td2_6
    TD2_7 = 1.7 * Td2_6
    TD2_8 = 2.12 * Td2_6

    if tolerance_grade == 4:
        return TD2_4
    elif tolerance_grade == 5:
        return TD2_5
    elif tolerance_grade == 6:
        return TD2_6
    elif tolerance_grade == 7:
        return TD2_7
    elif tolerance_grade == 8:
        return TD2_8
    else:
        raise Exception("tolerance_grade must be [4,5,6,7,8]")


def main() -> None:
    # Tests:
    
    print(f"\npitch list:")
    print(pitch_list)
    
    # Reproduce Table 9, pg 14:
    print("\nTable 9, pg 14:")
    for pitch in pitch_list:
        TD1_6 = eq_TD1_6(P=pitch)
        TD1_4 = eq_TD1(P=pitch, tolerance_grade=4)
        TD1_5 = eq_TD1(P=pitch, tolerance_grade=5)
        TD1_7 = eq_TD1(P=pitch, tolerance_grade=7)
        TD1_8 = eq_TD1(P=pitch, tolerance_grade=8)
        print(f"pitch: {pitch:.2f}, TD1_4: {TD1_4:.3f}, TD1_5: {TD1_5:.3f}, TD1_6: {TD1_6:.3f}, TD1_7: {TD1_7:.3f}, TD1_8: {TD1_8:.3f}")
    
    # Reproduce Table 10, pg 15:
    print("\nTable 10, pg 15:")
    for pitch in pitch_list:
        Td_6 = eq_Td_6(P=pitch)
        Td_4 = eq_Td(P=pitch, tolerance_grade=4)
        Td_8 = eq_Td(P=pitch, tolerance_grade=8)
        print(f"pitch: {pitch:.2f}, Td_4: {Td_4:.3f}, Td_6: {Td_6:.3f}, Td_8: {Td_8:.3f}")

    d = 1.0

    # Reproduce Table 11, pg 16:
    print("\nTable 11, pg 16:")
    for pitch in pitch_list:
        Td2_6 = eq_Td2_6(P=pitch, d=d)
        Td2_4 = eq_Td2(P=pitch, d=d, tolerance_grade=4)
        Td2_5 = eq_Td2(P=pitch, d=d, tolerance_grade=5)
        Td2_7 = eq_Td2(P=pitch, d=d, tolerance_grade=7)
        Td2_8 = eq_Td2(P=pitch, d=d, tolerance_grade=8)
        print(f"pitch: {pitch:.2f}, Td2_4: {Td2_4:.3f}, Td2_5: {Td2_5:.3f}, Td2_6: {Td2_6:.3f}, Td2_7: {Td2_7:.3f}, Td2_8: {Td2_8:.3f}")

    # Reproduce Table 12, pg 17:
    print("\nTable 12, pg 17:")
    for pitch in pitch_list:
        TD2_6 = eq_TD2(P=pitch, d=d, tolerance_grade=6)
        TD2_4 = eq_TD2(P=pitch, d=d, tolerance_grade=4)
        TD2_5 = eq_TD2(P=pitch, d=d, tolerance_grade=5)
        TD2_7 = eq_TD2(P=pitch, d=d, tolerance_grade=7)
        TD2_8 = eq_TD2(P=pitch, d=d, tolerance_grade=8)
        print(f"pitch: {pitch:.2f}, TD2_4: {TD2_4:.3f}, TD2_5: {TD2_5:.3f}, TD2_6: {TD2_6:.3f}, TD2_7: {TD2_7:.3f}, TD2_8: {TD2_8:.3f}")

    # Reproduce Table 13, pg 18:
    print("\nTable 13, pg 18:")
    for pitch in pitch_list:
        EI_G = eq_EI(P=pitch, allowance_class='G')
        EI_H = eq_EI(P=pitch, allowance_class='H')
        es_e = eq_es(P=pitch, allowance_class='e')
        es_f = eq_es(P=pitch, allowance_class='f')
        es_g = eq_es(P=pitch, allowance_class='g')
        es_h = eq_es(P=pitch, allowance_class='h')
        print(f"p: {pitch:.2f}, EI_G: {EI_G:.3f}, EI_H: {EI_H:.1f}, es_e: {es_e:.3f}, es_f: {es_f:.3f}, es_g: {es_g:.3f}, es_h: {es_h:.1f}")


if __name__ == "__main__":
    main()
    