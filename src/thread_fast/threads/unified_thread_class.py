"""UnifiedThread class definition.

Symbols:
-d_bsc: basic major diameter (external thread)
-D_bsc: basic major diameter (internal thread)
-d_max: max external major diameter
-d_min: min external major diameter
-d2_max: max external pitch diameter
-d2_min: minimum external pitch diameter
-D2_max: maximum internal pitch diameter
-D2_min: minimum internal pitch diameter
-D1_max: max internal minor diameter
-D1_min: minimum internal minor diameter
-es: basic allowance
-h_as: external thread addendum
-h_b: external thread addendum
-LE: length of engagement
-P: thread pitch
-Td: major diameter tolerance
-Td2: pitch diameter tolerance
-TD2: external pitch diameter tolerance

"""
import numpy as np


class UnifiedThread:
    def __init__(
            self, 
            name: str,
            basic_major_diameter: float,
            pitch: float,
            external: bool=True,
            intneral: bool=False,
        ):
            
        if internal is True:
            external = False
        
        # external or internal thread?:
        self.external = external
        self.internal = internal
            
        self.name = name
        
        # basic major diameter:
        self.d_bsc = basic_major_diameter
        self.D_bsc = basic_major_diameter
        
        # thread pitch:
        self.pitch = pitch
        
        # pitch diameter tolerance:
        self.Td2 = 1.0
        
        # basic allowance:
        self.es = 0.3 * self.Td2
        
        self.Td = 1.0
        
        # max external major diameter:
        self.d_max = self.d_bsc - self.es
        
        # min external major diameter:
        self.d_min = self.d_max - self.Td
        
        
        # external thread addendum:
        self.h_b = 1.0
        
        # minimum internal pitch diameter:
        self.D2_min = self.D_bsc - self.h_b
        
        # maximum internal pitch diameter:
        self.D2_max = self.D2_min + self.TD2



def main() -> None:
    # Tests:
    
    
    # machinery handbook 29th ed, Table 3 example, pg 1869:
    
    un_1_2_28_ef2A = UnifiedThread(
        name='un_1_2_28_ef2A',
        basic_major_diameter=0.5,
        pitch=1.0/28.0,
        external=True,
    )
    
    
    
    # machinery handbook 29th ed, Table 3 example, pg 1871:
    
    un_1_2_28_ef2A = UnifiedThread(
        name='un_1_2_28_ef2A',
        basic_major_diameter=0.5,
        pitch=1.0/28.0,
        internal=True,
    )
    


if __name__ == "__main__":
    main()
    