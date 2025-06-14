"""MetricThread class definition.

machinery handbook 29th ed, pg 1878

60-degree symmetrical screw thread

Standards:
-ANSI/ASME B1.13M-2005 Metric Screw Threads: M Profile
-ANSI B1.18M-1982 (R1987) Metric Screw Threads for Commercial Mechanical Fasteners - Boundary Profile Defined
-ISO 68-1:1998, ISO general purpose screw threads — Basic profile — Part 1: Metric screw threads
-ISO 261 general purpose metric screw threads — General plan
-ISO 724:1993, ISO general purpose metric screw threads — Basic dimensions
-ISO 965-1:1998, ISO general purpose metric screw threads — Tolerances — Part 1: Principles and basic data
-ANSI/ASME B1.21M-1997 (R2003) Metric Screw Threads: MJ Profile
-ISO 5408:1983, Cylindrical screw threads — Vocabulary

Symbols:
-D: basic major diameter (internal thread)
-D1: basic minor diameter (internal thread)
-D2: basic pitch diameter (internal thread)
-d: basic major diameter (external thread)
-d1: basic minor diameter (external thread)
-d2: basic pitch diameter (external thread)
-d3: rounded form minor diameter (external thread, M)
-d3: diameter to bottom of root radius (external thread, MJ)
-P: thread pitch
-r: external thread root radius
-T: tolerance
-TD1, TD2: tolerances for D1, D2
-Td, Td2: tolerances for d, d2
-ES: Upper Deviation, Internal Thread [Equals the Allowance (Fundamental Deviation) Plus the Tolerance]
-EI: Lower Deviation, Internal Thread Allowance (Fundamental Deviation)
-G, H: Letter Designations for Tolerance Positions for Lower Deviation, (Internal Thread)
-g, h: Letter Designations for Tolerance Positions for Upper Deviation, (External Thread)
-es: Upper Deviation, External Thread Allowance (Fundamental Deviation). In the ISO system es is always negative for an allowance fit or zero for no allowance.
-ei: Lower Deviation, External Thread [Equals the Allowance (Fundamental Deviation) Plus the Tolerance] In the ISO system ei is always negative for an allowance fit.
-H: height of fundamental triangle
-LE: length of engagement
-LH: left hand thread

"""
import numpy as np

# coarse pitch metric thread M profile series:
# [diameter, pitch], 
# machinery handbook 29th ed, pg 1880
mc_thread_list = [
    [1.6, 0.35],
    [2.0, 0.4],
    [2.5, 0.45],
    #TODO: finish...
]


# TODO: need to encode table 6, pg 1886

# TODO: need to encode table 7, pg 1887

# TODO: need to encode table 8, pg 1889

# TODO: need to encode table 9, pg 1890

# TODO: need to encode table 10, pg 1890

# TODO: need to encode table 11, pg 1891



class MetricThread:
    def __init__(
            self, 
            name: str,
            basic_major_diameter: float,
            pitch: float,
            tolerance_grade: int,  # [3,4,5,6,7,8,9]
            tolerance_position: str,  # [e, f, g, h, G, H]
            external: bool=True,
            intneral: bool=False,
            profile: str='M',  # [M, MJ]
        ):
            
        if internal is True:
            external = False
        
        # external or internal thread?:
        self.external = external
        self.internal = internal
            
        self.name = name
        
        # basic major diameter:
        self.d = basic_major_diameter
        self.D = basic_major_diameter
        
        # thread pitch:
        self.pitch = pitch
        
        # tolerance grade (indicated by number):
        self.tolerance_grade = tolerance_grade
        
        # allowance (fundamental deviation) (indicated by letter):
        self.tolerance_position = tolerance_position
        
        # M or MJ:
        self.profile = profile
        
        
        # Lower Deviation, Internal Thread Allowance (Fundamental Deviation)
        self.EI = 1.0
        
        # min major diameter:
        self.D_min = self.D + self.EI
        
        
        


def main() -> None:
    # Tests:
    
    M6_1 = MetricThread(
        name='M6x1.0',
        basic_major_diameter=6.0,
        pitch=1.0,
        tolerance_grade=4,
        tolerance_position='h',
        external=True,
        profile='M',
    )



if __name__ == "__main__":
    main()
    