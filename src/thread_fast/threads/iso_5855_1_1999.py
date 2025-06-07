"""Equations from ISO 5855-1:1999



"""
import numpy as np



###############################
# 10 Calculation Formulae, pg 9
###############################

###############################
# 10.1 External Threads, pg 9
###############################


def eq_d_max(d, es) -> float:
    """
    
    ISO 5855-1:1999, pg 9
    
    es in accordance with ISO 965-1
    """
    d_max = d - es
    return d_max


def eq_d_min(d, T_d) -> float:
    """
    
    ISO 5855-1:1999, pg 9
    
    T_d in accordance with ISO 965-1
    """
    d_min = d - T_d
    return d_min


def eq_d2_max(d_max, P) -> float:
    """
    
    ISO 5855-1:1999, pg 9
    
    es in accordance with ISO 965-1
    """
    d2_max = d_max - 0.649519*P
    return d2_max


def eq_d2_min(d2_max, T_d2) -> float:
    """
    
    ISO 5855-1:1999, pg 9
    
    T_d2 in accordance with ISO 965-1
    """
    d2_min = d2_max - T_d2
    return d2_min




###############################
# 10.2 Internal Threads, pg 10 
###############################




###############################
# Table 2 Nominal diameter & pitch combinations, pg 11
###############################

#TODO: add table...


def main() -> None:
    pass


if __name__ == "__main__":
    main()
    