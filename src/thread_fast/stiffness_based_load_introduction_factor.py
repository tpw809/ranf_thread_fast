"""Stiffness Based Load Introduction Factor

From: NASA-TM-108377 The Mechanism of Bolt Loading

The load in a preloaded bolt, P_b, is:
P_b = PLD + n * phi * P_ext
where:
PLD = preload
n = load introduction factor
phi = stiffness factor
P_ext = externally applied tensile load

The stiffness factor, phi, is:
phi = k_b / (k_a + k_b)
where 
k_b = stiffness of the bolt
k_a = stiffness of the abutment

The stiffness based load introduction factor, n, is:
n = (B + C) / (B*C) = 1.0 - (A + D) / (A*D)
where:
1 / k_a = 1/(A*k_a) + 1/(B*k_a) + 1/(C*k_a) + 1/(D*k_a)
means that:
1 = 1/A + 1/B + 1/C + 1/D

What do A,B,C,D actually represent?
A,B,C,D = stiffness coefficients

A = portion of clamped joint compressed in loaded part 1
B = portion of clamped joint relieved in loaded part 1
C = portion of clamped joint relieved in loaded part 2
D = portion of clamped joint compressed in loaded part 2
"""
import numpy as np



def check_abcd(a: float,b: float,c: float,d: float) -> float:
    """Check validity of A,B,C,D for stiffness based load introduction factor, n.
    
    Result should equal 1.0
    """
    assert a >= 1.0
    assert b >= 1.0
    assert c >= 1.0
    assert d >= 1.0
    return 1.0/a + 1.0/b + 1.0/c + 1.0/d


def stiffness_based_load_introduction_factor(
        B: float, 
        C: float,
    ) -> float:
    """Calculate stiffness based load introduction factor, n.
    
    Constraint: 1 = 1/A + 1/B + 1/C + 1/D
    
    n = (B + C) / (B*C) = 1.0 - (A + D) / (A*D)
    
    """
    return (B + C) / (B * C)


def main() -> None:
    
    # one basic solution is a=b=c=d=4
    a = 4.0
    b = 4.0
    c = 4.0
    d = 4.0
    
    res = check_abcd(a,b,c,d)
    print(f"res = {res}")
    
    # abutment (clamped joint) stiffness:
    k_a = 12.0e2
    
    # TODO: confirm 1/k=1/ka+1/kb+1/kc+1/kd -> 1=1/a+1/b+1/c+1/d
    
    # say e,f,g,h = 1/a,1/b,1/c,1/d
    # e+f+g+h = 1.0
    
    # TODO: make examples using specific geometry and materials
    


if __name__ == "__main__":
    main()
    