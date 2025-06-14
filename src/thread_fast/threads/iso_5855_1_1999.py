"""Equations from ISO 5855-1:1999

Aerospace - MJ threads

Part 1: General requirements

Tolerances in accordance with ISO 965-1 or as defined by part designer.

Symbols:
-d: basic major diameter of external thread
-d_2: basic pitch diameter of external thread
-d_3: minor diameter of external thread
-D: basic major diameter of internal thread
-D_1: basic minor diameter of internal thread
-D_2: basic pitch diameter of internal thread
-T_d: tolerance for d
-T_D2: tolerance for D2
-es: upper deviation
-EI: lower deviation

EI + T = ES
es + T = ei ???

"""
import numpy as np



###############################
# 10 Calculation Formulae, pg 9
###############################

###############################
# 10.1 External Threads, pg 9
###############################


def eq_d_max(d: float, es: float) -> float:
    """Calculate external thread maximum major diameter, d_max.
    
    ISO 5855-1:1999, pg 9
    
    es in accordance with ISO 965-1
    
    Args:
        d: basic major diameter
        es:
    Returns:
        float: external thread maximum major diameter
    """
    assert d > 0.0
    d_max = d - es
    return d_max


def eq_d_min(d: float, T_d: float) -> float:
    """Calculate external thread minimum major diameter, d_min. 
    
    ISO 5855-1:1999, pg 9
    
    T_d in accordance with ISO 965-1
    
    Args:
        d: basic major diameter
        T_d:
    Returns:
        float: external thread minimum major diameter
    """
    assert d > 0.0
    d_min = d - T_d
    return d_min


def eq_d2_max(d_max: float, P: float) -> float:
    """Calculate 
    
    ISO 5855-1:1999, pg 9
    
    es in accordance with ISO 965-1
    
    Args:
        d_max:
        P: thread pitch
    Returns:
        float:
    """
    assert P > 0.0
    d2_max = d_max - 0.649519*P
    return d2_max


def eq_d2_min(d2_max: float, T_d2: float) -> float:
    """Calculate 
    
    ISO 5855-1:1999, pg 9
    
    T_d2 in accordance with ISO 965-1
    
    Args:
        
    Returns:
        float:
    """
    d2_min = d2_max - T_d2
    return d2_min




###############################
# 10.2 Internal Threads, pg 10 
###############################


def eq_D1_min(D: float, P: float, EI: float) -> float:
    """Calculate internal thread minimum minor diameter, D1_min.
    
    ISO 5855-1:1999, pg 10
    
    Args:
        D: basic major diameter
        P: thread pitch
        EI: 
    Returns:
        float: internal thread minimum minor diameter
    """
    assert D > 0.0
    assert P > 0.0
    D1_min = D - 0.97428 * P + EI
    return D1_min


def eq_D1_max(
        D: float, 
        P: float, 
        EI: float, 
        T_D1: float,
    ) -> float:
    """Calculate internal thread maximum minor diameter, D1_max.
    
    ISO 5855-1:1999, pg 10
    
    Args:
        D: basic major diameter
        P: thread pitch
        EI: 
        T_D1: 
    Returns:
        float: internal thread maximum minor diameter
    """
    assert D > 0.0
    assert P > 0.0
    D1_min = eq_D1_min(D, P, EI)
    D1_max = D1_min + T_D1
    return D1_max


def eq_D2_min(
        D: float, 
        P: float, 
        EI: float,
    ) -> float:
    """Calcuate
    
    ISO 5855-1:1999, pg 10
    
    Args:
        D: basic major diameter
        P: thread pitch
        EI: 
    Returns:
        float: 
    """
    assert D > 0.0
    assert P > 0.0
    D2_min = D - 0.649519 * P + EI
    return D2_min


def eq_D2_max(
        D: float, 
        P: float, 
        EI: float,
        T_D2: float,
    ) -> float:
    """Calculate 
    
    Args:
    
    Returns:
        float: 
    """
    assert D > 0.0
    assert P > 0.0
    D2_min = eq_D2_min(D, P, EI)
    D2_max = D2_min + T_D2
    return D2_max


###############################
# Table 2 Nominal diameter & pitch combinations, pg 11
###############################

# [diameter, pitch]:
diam_pitch_list = [
    [1.6, 0.35],
    [17.0, 1.0],
    [39, 2.0],
    [62, 2.0],
    [85, 3.0],
    [140, 6.0],
    [220, 3.0],
    [1.8, 0.35],
    [17, 1.5],
    [39, 3.0],
    [62, 3.0],
    [85, 4.0],
    [145, 2.0],
    [220, 4.0],
    [2.0, 0.4],
    [18, 1.0],
    [39, 4.0], 
    [62, 4.0],
    [85, 6.0], 
    [145, 3.0], 
    [220, 6.0],
    [2.2, 0.45], 
    [18, 1.5], 
    [40, 1.5], 
    [64, 1.5], 
    [88, 1.5], 
    [145, 4.0], 
    [225, 3.0],
    [2.5, 0.35], 
    [18, 2.0], 
    [40, 2.0], 
    [64, 2.0], 
    [90, 1.5], 
    [145, 6.0], 
    [225, 4.0],
    [2.5, 0.45], 
    [18, 2.5], 
    [40, 3.0], 
    [64, 3.0], 
    [90, 2.0], 
    [150, 2.0], 
    [225, 6.0],
    [3.0, 0.35], 
    [20, 1.0], 
    [42, 1.5], 
    [64, 4.0], 
    [90, 3.0], 
    [150, 3.0], 
    [230, 3.0],
    [3.0, 0.5],  
    [20, 1.5],  
    [42, 2.0], 
    [64, 6.0], 
    [90, 4.0], 
    [150, 4.0], 
    [230, 4.0],
    [3.5, 0.35],  
    [20, 2.0], 
    [42, 3.0], 
    [65, 1.5],  
    [90, 6.0], 
    [150, 6.0], 
    [230, 6.0],
    [3.5, 0.6],  
    [20, 2.5],  
    [42, 4.0], 
    [65, 2.0], 
    [95, 2.0], 
    [155, 3.0], 
    [235, 3.0],
    [4.0, 0.5],  
    [22, 1.0], 
    [42, 4.5],  
    [65, 3.0], 
    [95, 3.0], 
    [155, 4.0], 
    [235, 4.0],
    [4.0, 0.7],  
    [22, 1.5],  
    [45, 1.5],  
    [65, 4.0], 
    [95, 4.0], 
    [155, 6.0], 
    [235, 6.0],
    [4.5, 0.5],  
    [22, 2.0], 
    [45, 2.0], 
    [68, 1.5],  
    [95, 6.0], 
    [160, 3.0], 
    [240, 3.0],
    [4.5, 0.75],  
    [22, 2.5],  
    [45, 3.0], 
    [68, 2.0], 
    [100, 2.0], 
    [160, 4.0], 
    [240, 4.0],
    [5.0, 0.5],  
    [24, 1.0], 
    [45, 4.0], 
    [68, 3.0], 
    [100, 3.0], 
    [160, 6.0], 
    [240, 6.0],
    [5.0, 0.8],
    [24, 1.5],  
    [45, 4.5],  
    [68, 4.0], 
    [100, 4.0], 
    [165, 3.0], 
    [245, 3.0],
    [5.5, 0.5],  
    [24, 2.0], 
    [48, 1.5],  
    [68, 6.0], 
    [100, 6.0], 
    [165, 4.0], 
    [245, 4.0],
    [6.0, 0.75],  
    [24, 3.0], 
    [48, 2.0], 
    [70, 1.5],  
    [105, 2.0], 
    [165, 6.0], 
    [245, 6.0],
    [6.0, 1.0], 
    [25, 1.0], 
    [48, 3.0], 
    [70, 2.0], 
    [105, 3.0], 
    [170, 3.0], 
    [250, 3.0],
    [7.0, 0.75],  
    [25, 1.5],  
    [48, 4.0], 
    [70, 3.0], 
    [105, 4.0], 
    [170, 4.0], 
    [250, 4.0],
    [7.0, 1.0], 
    [25, 2.0], 
    [48, 5.0], 
    [70, 4.0], 
    [105, 6.0], 
    [170, 6.0], 
    [250, 6.0],
    [8.0, 0.75],  
    [26, 1.5],  
    [50, 1.5],  
    [70, 6.0], 
    [110, 2.0], 
    [175, 3.0], 
    [255, 4.0],
    [8.0, 1.0], 
    [27, 1.0], 
    [50, 2.0], 
    [72, 1.5],  
    [110, 3.0], 
    [175, 4.0], 
    [255, 6.0],
    [8.0,  1.25],  
    [27, 1.5],  
    [50, 3.0], 
    [72, 2.0], 
    [110, 4.0], 
    [175, 6.0], 
    [260, 4.0],
    [9.0, 0.75],  
    [27, 2.0], 
    [52, 1.5],  
    [72, 3.0], 
    [110, 6.0], 
    [180, 3.0], 
    [260, 6.0],
    [9.0, 1.0], 
    [27, 3.0], 
    [52, 2.0], 
    [72, 4.0], 
    [115, 2.0], 
    [180, 4.0], 
    [265, 4.0],
    [9.0, 1.25],  
    [28, 1.0], 
    [52, 3.0], 
    [72, 6.0], 
    [115, 3.0], 
    [180, 6.0], 
    [265, 6.0],
    [10.0, 0.75],  
    [28, 1.5],  
    [52, 4.0], 
    [75, 1.5],  
    [115, 4.0], 
    [185, 3.0], 
    [270, 4.0],
    [10.0, 1.0], 
    [28, 2.0], 
    [52, 5.0], 
    [75, 2.0], 
    [115, 6.0], 
    [185, 4.0], 
    [270, 6.0],
    [10.0, 1.25],  
    [30, 1.0], 
    [55, 1.5],  
    [75, 3.0], 
    [120, 2.0], 
    [185, 6.0], 
    [275, 4.0],
    [10.0, 1.5],  
    [30, 1.5],  
    [55, 2.0], 
    [75, 4.0], 
    [120, 3.0], 
    [190, 3.0], 
    [275, 6.0],
    [11.0, 0.75],  
    [30, 2.0], 
    [55, 3.0], 
    [76, 1.5],  
    [120, 4.0], 
    [190, 4.0], 
    [280, 4.0],
    [11.0, 1.0], 
    [30, 3.0], 
    [55, 4.0], 
    [76, 3.0], 
    [120, 6.0], 
    [190, 6.0], 
    [280, 6.0],
    [11.0, 1.25],  
    [30, 3.5],  
    [56, 1.5],  
    [76, 4.0], 
    [125, 2.0], 
    [195, 3.0], 
    [285, 4.0],
    [11.0, 1.5],  
    [32, 1.5],  
    [56, 2.0], 
    [76, 6.0], 
    [125, 3.0], 
    [195, 4.0], 
    [285, 6.0],
    [12.0, 1.0], 
    [32, 2.0], 
    [56, 3.0], 
    [78, 1.5],  
    [125, 4.0], 
    [195, 6.0], 
    [290, 4.0],
    [12.0, 1.25],  
    [33, 1.5],  
    [56, 4.0], 
    [78, 2.0], 
    [125, 6.0], 
    [200, 3.0], 
    [290, 6.0],
    [12.0, 1.5],
    [33, 2.0], 
    [56, 5.5],  
    [78, 3.0], 
    [130, 2.0],
    [200, 4.0], 
    [295, 4.0],
    [12.0, 1.75],  
    [33, 3.0], 
    [58, 1.5],  
    [80, 1.5],  
    [130, 3.0], 
    [200, 6.0], 
    [295, 6.0],
    [14.0, 1.0], 
    [33, 3.5],  
    [58, 2.0], 
    [80, 2.0], 
    [130, 4.0], 
    [205, 3.0], 
    [300, 4.0],
    [14.0, 1.25],  
    [35, 1.5],  
    [58, 3.0], 
    [80, 3.0], 
    [130, 6.0], 
    [205, 4.0], 
    [300, 6.0],
    [14.0, 1.5], 
    [35, 2.0], 
    [58, 4.0], 
    [80, 4.0], 
    [135, 2.0], 
    [205, 6.0],
    [14.0, 2.0], 
    [36, 1.5], 
    [60, 1.5], 
    [80, 6.0], 
    [135, 3.0], 
    [210, 3.0],
    [15.0, 1.0], 
    [36, 2.0], 
    [60, 2.0], 
    [82, 1.5], 
    [135, 4.0], 
    [210, 4.0],
    [15.0, 1.5], 
    [36, 3.0],
    [60, 3.0],
    [82, 2.0],
    [135, 6.0],
    [210, 6.0],
    [16.0, 1.0],
    [36, 4.0],
    [60, 4.0],
    [82, 3.0],
    [140, 2.0],
    [215, 3.0],
    [16.0, 1.5],
    [38, 1.5],
    [60, 5.5],
    [85, 1.5],
    [140, 3.0],
    [215, 4.0],
    [16.0, 2.0],
    [39.0, 1.5],
    [62.0, 1.5],
    [85.0, 2.0],
    [140.0, 4.0],
    [215.0, 6.0],
]


def main() -> None:
    
    print(f"diam_pitch_list = \n{diam_pitch_list}")
    
    # basis major diameter:
    D = 5.0
    
    # thread pitch:
    pitch = 0.8
    
    # upper deviation
    es = 1.0
    
    #
    T_d = 1.0
    
    # 
    EI = 1.0
    
    # 
    T_D2 = 1.0


if __name__ == "__main__":
    main()
    