"""Equations from ISO 724-1993

ISO general-purpose metric screw threads - Basic dimensions

Dimensions in millimeters.

Symbols:
-D: basic major diameter of internal thread (nominal diameter)
-d: basic major diameter of external thread (nominal diameter)
-D_2: basic pitch diameter of internal thread
-d_2: basic pitch diameter of external thread
-D_1: basic minor diameter of internal thread
-d_1: basic minor diameter of external thread
-H: height of fundamental triangle
-P: pitch
"""
import numpy as np
from thread_fast.threads.iso_68_1998 import eq_H

# list of metric diameter and pitch combinations:
# [diameter, pitch]
metric_thread_list = [
    [1.0, 0.25],
    [1.0, 0.2],
    [1.1, 0.25],
    [1.1, 0.2],
    [1.2, 0.25],
    [1.2, 0.2],
    [1.4, 0.3],
    [1.4, 0.2],
    [1.6, 0.35],
    [1.6, 0.2],
    [1.8, 0.35],
    [1.8, 0.2],
    [2.0, 0.4],
    [2.0, 0.25],
    [2.2, 0.45],
    [2.2, 0.25],
    [2.5, 0.45],
    [2.5, 0.35],
    [3.0, 0.5],
    [3.0, 0.35],
    [3.5, 0.6],
    [3.5, 0.35],
    [4.0, 0.7],
    [4.0, 0.5],
    [4.5, 0.75],
    [4.5, 0.5],
    [5.0, 0.8],
    [5.0, 0.5],
    [5.5, 0.5],
    [6.0, 1.0],
    [6.0, 0.75],
    [7.0, 1.0],
    [7.0, 0.75],
    [8.0, 1.25],
    [8.0, 1.0],
    [8.0, 0.75],
    [9.0, 1.25],
    [9.0, 1.0],
    [9.0, 0.75],
    [10.0, 1.5],
    [10.0, 1.25],
    [10.0, 1.0],
    [10.0, 0.75],
]
# TODO: finish the list!!!

# a better data structure?
metric_thread_dict = {
    '5.0': {'0.8', '0.5'}
}



def eq_D_2(D: float, H: float, P: float=None) -> float:
    """Calculate basic pitch diameter of internal thread, D_2.
    
    ISO 724
    
    Args:
        D: basic major diameter of internal thread (nominal diameter)
        H: height of fundamental triangle
        P: thread pitch
    Returns:
        float:
    """
    if H is None:
        assert P is not None
        H = eq_H(P)
    # D_2 = D - 2.0 * (3.0 / 8.0) * H
    D_2 = D - (3.0 / 4.0) * H
    return D_2


def eq_d_2(d: float, H: float, P: float=None) -> float:
    """Calculate basic pitch diameter of external thread, d_2.
    
    ISO 724
    
    Args:
        d: basic major diameter of external thread (nominal diameter)
        H: height of fundamental triangle
        P: thread pitch
    Returns:
        float:
    """
    if H is None:
        assert P is not None
        H = eq_H(P)
    # d_2 = d - 2.0 * (3.0 / 8.0) * H
    d_2 = d - (3.0 / 4.0) * H
    return d_2


def eq_D_1(D: float, H: float, P: float=None) -> float:
    """Calculate basic minor diameter of internal thread, D_1.
    
    ISO 724
    
    Args:
        D: basic major diameter of internal thread (nominal diameter)
        H: height of fundamental triangle
        P: thread pitch
    Returns:
        float:
    """
    if H is None:
        assert P is not None
        H = eq_H(P)
    # D_1 = D - 2.0 * (5.0 / 8.0) * H
    D_1 = D - (5.0 / 4.0) * H
    return D_1


def eq_d_1(d: float, H: float, P: float=None) -> float:
    """Calculate basic minor diameter of external thread, d_1.
    
    ISO 724
    
    Args:
        d: basic major diameter of external thread (nominal diameter)
        H: height of fundamental triangle
        P: thread pitch
    Returns:
        float:
    """
    if H is None:
        assert P is not None
        H = eq_H(P)
    # d_1 = d - 2.0 * (5.0 / 8.0) * H
    d_1 = d - (5.0 / 4.0) * H
    return d_1


def main() -> None:
    print(metric_thread_list)
    print(metric_thread_dict)
    
    for thread in metric_thread_list:
        print(f"thread = {thread}")
        d2 = eq_d_2(thread[0], None, thread[1])
        print(f"d2 = {d2}")
    
    
if __name__ == "__main__":
    main()
    