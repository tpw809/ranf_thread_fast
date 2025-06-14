"""Equation from Machinery Handbook, 29th Edition.



"""
import numpy as np

# conversion factors:
deg_to_rad = np.pi / 180.0

# constants:
cos30 = np.cos(30.0 * deg_to_rad)


# standard unified thread diameter pitch combinations (UN/UNR):
# [diameter in inches, threads per inch]:
# pg 1816:
unc_diam_pitch_list = [
    [0.073, 64.0],  # size 1, coarse
    [0.086, 56.0],  # size 2, coarse
    [0.099, 48.0],  # size 3, coarse
    [0.112, 40.0],  # size 4, coarse
    [0.125, 40.0],  # size 5, coarse
    [0.138, 32.0],  # size 6, coarse
    [0.164, 32.0],  # size 8, coarse
    [0.190, 24.0],  # size 10, coarse
    [0.216, 24.0],  # size 12, coarse
    [0.250, 20.0],  # size 1/4, coarse
    [0.3125, 18.0],  # size 5/16, coarse
    [0.3750, 16.0],  # size 3/8, coarse
    [0.4375, 14.0],  # size 7/16, coarse
    [0.5000, 13.0],  # size 1/2, coarse
    [0.5625, 12.0],  # size 9/16, coarse
    [0.6250, 11.0],  # size 5/8, coarse
    [0.7500, 10.0],  # size 3/4, coarse
    [0.8750, 9.0],  # size 7/8, coarse
    #TODO: finish...
]

# fine threads, UNF, UNRF:
unf_diam_pitch_list = [
    [0.0600, 80.0],  # size 0, fine
    [0.0730, 72.0],  # size 1, fine
    [0.0860, 64.0],  # size 2, fine
    [0.0990, 56.0],  # size 3, fine
    [0.1120, 48.0],  # size 4, fine
    [0.1250, 44.0],  # size 5, fine
    [0.1380, 40.0],  # size 6, fine
    [0.1640, 36.0],  # size 8, fine
    [0.1900, 32.0],  # size 10, fine
    [0.2160, 28.0],  # size 12, fine
    [0.2500, 28.0],  # size 1/4, fine
    [0.3125, 24.0],  # size 5/16, fine
    [0.3750, 24.0],  # size 3/8, fine
    [0.4375, 20.0],  # size 7/16, fine
    [0.5000, 20.0],  # size 1/2, fine
    [0.5625, 18.0],  # size 9/16, fine
    [0.6250, 18.0],  # size 5/8, fine
    [0.7500, 16.0],  # size 3/4, fine
    [0.8750, 14.0],  # size 7/8, fine
    [1.0000, 12.0],  # size 1", fine
    [1.1250, 12.0],  # size 1 1/8, fine
    [1.2500, 12.0],  # size 1 1/4, fine
    [1.3750, 12.0],  # size 1 3/8, fine
    [1.5000, 12.0],  # size 1 1/2, fine
    #TODO: finish...
]

# extra fine threads, UNEF, UNREF: Table 4c. pg 1846
unef_diam_pitch_list = [
    [0.2160, 32.0],  # size 12, extra fine
    [0.2500, 32.0],  # size 1/4, extra fine
    [0.3125, 32.0],  # size 5/16, extra fine
    #TODO: finish...
]




# constant pitch series:
# 4-thread series:
# 6-thread series:
# 8-thread series:
# 12-thread series:
# 16-thread series:
# 20-thread series:
# 28-thread series:
# 32-thread series:
# Unified Miniature Screw Threads:


# Thread Classes: tolerance and allowance
# Classes 1A, 2A, 3A apply to external threads
# Classes 1B, 2B, 3B apply to internal threads

# Classes 3A & 3B: no no allowance or clearance for assembly



def eq_d(p: float) -> float:
    """V-thread, sharp V-thread:
    
    machinery handbook 29th ed, pg 1806
    """
    d = p * cos30
    return d



def eq_d_max(d_bsc: float, es: float) -> float:
    """Calculate max external major diameter, d_max.
    
    machinery handbook 29th ed, pg 1869
    
    Args:
        d_bsc: basic major diameter
        es: basic allowance
    Returns:
        float: max external major diameter
    """
    assert d_bsc > 0.0
    assert es >= 0.0
    d_max = d_bsc - es
    return d_max


def eq_d_min(d_max: float, Td: float) -> float:
    """Calculate min external major diameter, d_min.
    
    machinery handbook 29th ed, pg 1869
    """
    d_min = d_max - Td
    return d_min


# Unified Screw Threads - UNJ Profile:
# British Standard BS 4084: 1978
# MIL-S-8879
# ISO 3161-1977
# The ASME B1.15-1995
# ASME B1.1 Unified Inch Screw Threads
# ASME B1.30 Screw Threads: Standard Practice for Calculating and Rounding Dimensions


# Metric Screw Threads:
# ANSI/ASME B1.13M-2005 Metric Screw Threads
# ANSI B1.18M-1982 (R1987)
# ANSI/ASME B1.21M
# ISO 68
# ISO 965/1


# Metric Screw Threads - MJ Profile:
# ANSI/ASME B1.15 UNJ Thread
# MIL-S-8879
# ANSI/ASME B1.21M-1997 (R2003)
# ANSI/ASME B1.30M
# ISO 261



def main() -> None:
    
    # cosine of 30 degrees:
    print(f"cos30 = {cos30}")
    
    # [mm/thread], thread pitch:
    pitch = 1.0
    
    d = eq_d(pitch)
    print(f"d = {d}")
    
    
    
    # Table 3 example, pg 1869:
    
    # basic major diameter:
    d_bsc = 0.5
    
    # pitch:
    P = 1.0 / 28.0
    
    # basic allowance:
    es = 1.0
    
    # maximum external major diameter:
    d_max = d_bsc - es
    print(f"d_max = {d_max}")
    
    d_max = eq_d_max(d_bsc, es)
    print(f"d_max = {d_max}")
    
    
    
    
    

if __name__ == "__main__":
    main()
    