"""MetricThread class definition.

machinery handbook 29th ed, pg 1878

60-degree symmetrical screw thread

Standards:

- ANSI/ASME B1.13M-2005 Metric Screw Threads: M Profile
- ANSI B1.18M-1982 (R1987) Metric Screw Threads for Commercial Mechanical Fasteners - Boundary Profile Defined
- ISO 68-1:1998, ISO general purpose screw threads — Basic profile — Part 1: Metric screw threads
- ISO 261 general purpose metric screw threads — General plan
- ISO 724:1993, ISO general purpose metric screw threads — Basic dimensions
- ISO 965-1:1998, ISO general purpose metric screw threads — Tolerances — Part 1: Principles and basic data
- ANSI/ASME B1.21M-1997 (R2003) Metric Screw Threads: MJ Profile
- ISO 5408:1983, Cylindrical screw threads — Vocabulary

Symbols:

- D: basic major diameter (internal thread)
- D1: basic minor diameter (internal thread)
- D2: basic pitch diameter (internal thread)
- d: basic major diameter (external thread)
- d1: basic minor diameter (external thread)
- d2: basic pitch diameter (external thread)
- d3: rounded form minor diameter (external thread, M)
- d3: diameter to bottom of root radius (external thread, MJ)
- P: thread pitch
- r: external thread root radius
- T: tolerance
- TD1, TD2: tolerances for D1, D2
- Td, Td2: tolerances for d, d2
- ES: Upper Deviation, Internal Thread [Equals the Allowance (Fundamental Deviation) Plus the Tolerance]
- EI: Lower Deviation, Internal Thread Allowance (Fundamental Deviation)
- G, H: Letter Designations for Tolerance Positions for Lower Deviation, (Internal Thread)
- g, h: Letter Designations for Tolerance Positions for Upper Deviation, (External Thread)
- es: Upper Deviation, External Thread Allowance (Fundamental Deviation). In the ISO system es is always negative for an allowance fit or zero for no allowance.
- ei: Lower Deviation, External Thread [Equals the Allowance (Fundamental Deviation) Plus the Tolerance] In the ISO system ei is always negative for an allowance fit.
- H: height of fundamental triangle
- LE: length of engagement
- LH: left hand thread

"""
import numpy as np
import thread_fast.threads.asme_b1_13M_2005 as asme_m_thread
import thread_fast.threads.iso_724_1993 as iso_724_1993
import thread_fast.threads.iso_5855_1_1999 as iso_5855_1_1999
import thread_fast.conversion_factors as cf

# coarse pitch metric thread M profile series:
# [diameter, pitch], 
# machinery handbook 29th ed, pg 1880
metric_coarse_thread_list = [
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
    """MetricThread class.
    
    Args:
        name (str): Descriptive name.
        basic_major_diameter (float): Basic (nominal) major diameter.
        pitch (float): thread pitch.
    """
    def __init__(
            self, 
            name: str,
            basic_major_diameter: float,
            pitch: float,
            tolerance_grade: int,  # [3,4,5,6,7,8,9]
            allowance_class: str,  # [e, f, g, h, G, H]
            external: bool=True,
            internal: bool=False,
            profile: str='M',  # [M, MJ]
            beta: float=30.0 * cf.deg_to_rad,
        ):
            
        if internal is True:
            external = False
        
        # [rad], thread half angle:
        self.beta = beta
        
        # external or internal thread?:
        self.external = external
        self.internal = internal
            
        self.name = name
        
        # thread pitch:
        self.pitch = pitch
        
        # height of fundamental triangle:
        # from: iso 68
        self.H = (np.sqrt(3.0) / 2.0) * self.pitch
        
        # tolerance grade (indicated by number):
        self.tolerance_grade = tolerance_grade
        
        # allowance (fundamental deviation) (indicated by letter):
        self.allowance_class = allowance_class
        
        # M or MJ:
        self.profile = profile
        
        # length of engagement:
        LE_min, LE_max = asme_m_thread.eq_LE(
            P=self.pitch,
            d=basic_major_diameter,
        )
        self.LE_min = LE_min
        self.LE_max = LE_max
        
        
        if self.external is True:
            # basic major diameter:
            self.d = basic_major_diameter
            
            self.es = asme_m_thread.eq_es(
                P=self.pitch, 
                allowance_class=allowance_class,
            )
        
            # basic pitch diameter:
            self.d2 = iso_724_1993.eq_d_2(
                d=self.d,
                H=self.H,
                P=self.pitch,
            )
            
            # basic minor diameter:
            self.d1 = iso_724_1993.eq_d_1(
                d=self.d,
                H=self.H,
                P=self.pitch,
            )
            
            # basic minor diameter (design profile):
            self.d3 = iso_724_1993.eq_d_3(
                d=self.d,
                H=self.H,
                P=self.pitch,
            )
            
            # major diameter tolerance:
            self.Td = asme_m_thread.eq_Td(
                P=self.pitch,
                tolerance_grade=self.tolerance_grade,
            )
            
            # pitch diameter tolerance:
            self.Td2 = asme_m_thread.eq_Td2(
                P=self.pitch,
                d=self.d,
                tolerance_grade=self.tolerance_grade,
            )
            
            # max major diameter:
            self.d_max = iso_5855_1_1999.eq_d_max(
                d=self.d,
                es=self.es,
            )
            
            # min major diameter:
            self.d_min = iso_5855_1_1999.eq_d_min(
                d_max=self.d_max,
                T_d=self.Td,
            )
            
            # max pitch diameter:
            self.d2_max = iso_5855_1_1999.eq_d2_max(
                d_max=self.d_max,
                P=self.pitch,
            )
            
            # min pitch diameter:
            self.d2_min = iso_5855_1_1999.eq_d2_min(
                d2_max=self.d2_max,
                T_d2=self.Td2,
            )
            
            # max root diameter:
            self.d3_max = iso_5855_1_1999.eq_d3_max(
                d2_max=self.d2_max,
                P=self.pitch,
                d3=self.d3,
            )
            
            # min root diameter:
            self.d3_min = iso_5855_1_1999.eq_d3_min(
                d2_min=self.d2_min,
                P=self.pitch,
            )
        
        
        else:
            # basic major diameter:
            self.D = basic_major_diameter
        
            # Lower Deviation, Internal Thread Allowance (Fundamental Deviation)
            self.EI = asme_m_thread.eq_EI(
                P=self.pitch, 
                allowance_class=allowance_class,
            )
        
            # min major diameter:
            self.D_min = self.D + self.EI
        
            # basic pitch diameter:
            self.D2 = iso_724_1993.eq_D_2(
                D=self.D,
                H=self.H,
                P=self.pitch,
            )
            
            # basic minor diameter:
            self.D1 = iso_724_1993.eq_D_1(
                D=self.D, 
                H=self.H, 
                P=self.pitch,
            )
            
            # minor diameter tolerance:
            self.TD1 = asme_m_thread.eq_TD1(
                P=self.pitch,
                tolerance_grade=self.tolerance_grade,
            )
            
            # pitch diameter tolerance:
            self.TD2 = asme_m_thread.eq_TD2(
                P=self.pitch,
                d=self.D,
                tolerance_grade=self.tolerance_grade,
            )
            
            # max diameter to root:
            self.D3_max = iso_5855_1_1999.eq_D3_max(
                D=self.D,
                P=self.pitch,
                EI=self.EI,
                T_D2=self.TD2,
            )
            
            # min minor diameter:
            self.D1_min = iso_5855_1_1999.eq_D1_min(
                D=self.D,
                P=self.pitch,
                EI=self.EI,
            )
            
            # max minor diameter:
            self.D1_max = iso_5855_1_1999.eq_D1_max(
                D=self.D,
                P=self.pitch,
                EI=self.EI,
                T_D1=self.TD1,
            )
            
            self.D2_min = iso_5855_1_1999.eq_D2_min(
                D=self.D,
                P=self.pitch,
                EI=self.EI,
            )
            
            self.D2_max = iso_5855_1_1999.eq_D2_max(
                D=self.D,
                P=self.pitch,
                EI=self.EI,
                T_D2=self.TD2,
            )
            
            self.D3_max = iso_5855_1_1999.eq_D3_max(
                D=self.D,
                P=self.pitch,
                EI=self.EI,
                T_D2=self.TD2,
            )
        
    @property
    def r_m(self) -> float:
        """mean radius of screw thread
        
        equals half of pitch diameter
        
        """
        return self.d2 / 2.0

    @property
    def psi(self) -> float:
        """thread lead angle, rad.
        
        alternative for english threads:
        alpha = np.arctan(1.0 / (n_0 * np.pi * E_in))
        
        """
        psi = np.arctan(self.pitch / (2.0 * np.pi * self.r_m))
        return psi

    def __str__(self):
        return "\n".join([
            "\nThread:",
            f"name = {self.name}",
            f"basic_major_diameter = {self.d}",
            f"pitch = {self.pitch}",
            "",
        ])




class ExternalMetricThread:
    def __init__(
            self, 
            name: str,
            basic_major_diameter: float,
            pitch: float,
            tolerance_grade: int,  # [3,4,5,6,7,8,9]
            allowance_class: str,  # [e, f, g, h]
            profile: str='M',  # [M, MJ]
            beta: float=30.0 * cf.deg_to_rad,
        ):
        
        # external or internal thread?:
        self.external = True
        self.internal = False
        
        # [rad], thread half angle:
        self.beta = beta
            
        self.name = name
        
        # thread pitch:
        self.pitch = pitch
        
        # height of fundamental triangle:
        # from: iso 68
        self.H = (np.sqrt(3.0) / 2.0) * self.pitch
        
        # tolerance grade (indicated by number):
        self.tolerance_grade = tolerance_grade
        
        # allowance (fundamental deviation) (indicated by letter):
        self.allowance_class = allowance_class
        
        # M or MJ:
        self.profile = profile
        
        # length of engagement:
        LE_min, LE_max = asme_m_thread.eq_LE(
            P=self.pitch,
            d=basic_major_diameter,
        )
        self.LE_min = LE_min
        self.LE_max = LE_max
        
        # basic major diameter:
        self.d = basic_major_diameter
        
        # 
        self.es = asme_m_thread.eq_es(
            P=self.pitch, 
            allowance_class=allowance_class,
        )
        
        # basic pitch diameter:
        self.d2 = iso_724_1993.eq_d_2(
            d=self.d,
            H=self.H,
            P=self.pitch,
        )
        
        # basic minor diameter:
        self.d1 = iso_724_1993.eq_d_1(
            d=self.d,
            H=self.H,
            P=self.pitch,
        )
        
        # basic minor diameter (design profile):
        self.d3 = iso_724_1993.eq_d_3(
            d=self.d,
            H=self.H,
            P=self.pitch,
        )
        
        # major diameter tolerance:
        self.Td = asme_m_thread.eq_Td(
            P=self.pitch,
            tolerance_grade=self.tolerance_grade,
        )
        
        # pitch diameter tolerance:
        self.Td2 = asme_m_thread.eq_Td2(
            P=self.pitch,
            d=self.d,
            tolerance_grade=self.tolerance_grade,
        )
        
        # max major diameter:
        self.d_max = iso_5855_1_1999.eq_d_max(
            d=self.d,
            es=self.es,
        )
        
        # min major diameter:
        self.d_min = iso_5855_1_1999.eq_d_min(
            d_max=self.d_max,
            T_d=self.Td,
        )
        
        # max pitch diameter:
        self.d2_max = iso_5855_1_1999.eq_d2_max(
            d_max=self.d_max,
            P=self.pitch,
        )
        
        # min pitch diameter:
        self.d2_min = iso_5855_1_1999.eq_d2_min(
            d2_max=self.d2_max,
            T_d2=self.Td2,
        )
        
        # max root diameter:
        self.d3_max = iso_5855_1_1999.eq_d3_max(
            d2_max=self.d2_max,
            P=self.pitch,
            d3=self.d3,
        )
        
        # min root diameter:
        self.d3_min = iso_5855_1_1999.eq_d3_min(
            d2_min=self.d2_min,
            P=self.pitch,
        )
        
        # [mm^2], tensile area (min cross section area of bolt):
        # NASA-TM-106943, equation 4, pg 5
        # used for fastener strength
        self.A_t = (np.pi/4.0) * (self.d - 0.9743*self.pitch)**2

        # [mm^2], mean area of threads:
        # used for fastener stiffness estimate
        self.A_mean = np.pi * self.r_m**2
        
    @property
    def r_m(self) -> float:
        """mean radius of screw thread, mm.
        
        equals half of pitch diameter
        
        """
        return self.d2 / 2.0

    @property
    def psi(self) -> float:
        """thread lead angle, rad.
        
        alternative for english threads:
        
        alpha = np.arctan(1.0 / (n_0 * np.pi * E_in))
        
        """
        psi = np.arctan(self.pitch / (2.0 * np.pi * self.r_m))
        return psi

    def to_dict(self) -> dict:
        return {
            "type": 'ExternalThread',
            "pitch": self.pitch,
            "basic_major_diameter": self.d,
            "mean_thread_radius": self.r_m,
            "thread_half_angle_rad": self.beta,
            "thread_lead_angle_rad": self.psi,
            "fundamental_triangle_height": self.H,
        }

    def __str__(self):
        return "\n".join([
            "\nExternalThread:",
            f"name = {self.name}",
            f"basic_major_diameter = {self.d}",
            f"pitch = {self.pitch}",
            "",
        ])


class InternalMetricThread:
    def __init__(
            self, 
            name: str,
            basic_major_diameter: float,
            pitch: float,
            tolerance_grade: int,  # [3,4,5,6,7,8,9]
            allowance_class: str,  # [G, H]
            profile: str='M',  # [M, MJ]
            beta: float=30.0 * cf.deg_to_rad,
        ):
        
        # external or internal thread?:
        self.external = False
        self.internal = True
        
        # [rad], thread half angle:
        self.beta = beta
            
        self.name = name
        
        # thread pitch:
        self.pitch = pitch
        
        # height of fundamental triangle:
        # from: iso 68
        self.H = (np.sqrt(3.0) / 2.0) * self.pitch
        
        # tolerance grade (indicated by number):
        self.tolerance_grade = tolerance_grade
        
        # allowance (fundamental deviation) (indicated by letter):
        self.allowance_class = allowance_class
        
        # M or MJ:
        self.profile = profile
        
        # length of engagement:
        LE_min, LE_max = asme_m_thread.eq_LE(
            P=self.pitch,
            d=basic_major_diameter,
        )
        self.LE_min = LE_min
        self.LE_max = LE_max
        
        # basic major diameter:
        self.D = basic_major_diameter
        
        # Lower Deviation, Internal Thread Allowance (Fundamental Deviation)
        self.EI = asme_m_thread.eq_EI(
            P=self.pitch, 
            allowance_class=allowance_class,
        )
        
        # min major diameter:
        self.D_min = self.D + self.EI
        
        # basic pitch diameter:
        self.D2 = iso_724_1993.eq_D_2(
            D=self.D,
            H=self.H,
            P=self.pitch,
        )
        
        # basic minor diameter:
        self.D1 = iso_724_1993.eq_D_1(
            D=self.D, 
            H=self.H, 
            P=self.pitch,
        )
        
        # minor diameter tolerance:
        self.TD1 = asme_m_thread.eq_TD1(
            P=self.pitch,
            tolerance_grade=self.tolerance_grade,
        )
        
        # pitch diameter tolerance:
        self.TD2 = asme_m_thread.eq_TD2(
            P=self.pitch,
            d=self.D,
            tolerance_grade=self.tolerance_grade,
        )
        
        # max diameter to root:
        self.D3_max = iso_5855_1_1999.eq_D3_max(
            D=self.D,
            P=self.pitch,
            EI=self.EI,
            T_D2=self.TD2,
        )
        
        # min minor diameter:
        self.D1_min = iso_5855_1_1999.eq_D1_min(
            D=self.D,
            P=self.pitch,
            EI=self.EI,
        )
        
        # max minor diameter:
        self.D1_max = iso_5855_1_1999.eq_D1_max(
            D=self.D,
            P=self.pitch,
            EI=self.EI,
            T_D1=self.TD1,
        )
        
        self.D2_min = iso_5855_1_1999.eq_D2_min(
            D=self.D,
            P=self.pitch,
            EI=self.EI,
        )
        
        self.D2_max = iso_5855_1_1999.eq_D2_max(
            D=self.D,
            P=self.pitch,
            EI=self.EI,
            T_D2=self.TD2,
        )
        
        self.D3_max = iso_5855_1_1999.eq_D3_max(
            D=self.D,
            P=self.pitch,
            EI=self.EI,
            T_D2=self.TD2,
        )
        
        # TODO: thread shear area
        
    @property
    def r_m(self) -> float:
        """mean radius of screw thread, mm.
        
        equals half of pitch diameter
        
        """
        return self.D2 / 2.0

    @property
    def psi(self) -> float:
        """thread lead angle, rad.
        
        alternative for english threads:
        
        alpha = np.arctan(1.0 / (n_0 * np.pi * E_in))
        
        """
        psi = np.arctan(self.pitch / (2.0 * np.pi * self.r_m))
        return psi

    def to_dict(self) -> dict:
        return {
            "type": 'InternalThread',
            "pitch": self.pitch,
            "basic_major_diameter": self.D,
            "mean_thread_radius": self.r_m,
            "thread_half_angle_rad": self.beta,
            "thread_lead_angle_rad": self.psi,
            "fundamental_triangle_height": self.H,
        }

    def __str__(self):
        return "\n".join([
            "\nInternalThread:",
            f"name = {self.name}",
            f"basic_major_diameter = {self.D}",
            f"pitch = {self.pitch}",
            "",
        ])



def main() -> None:
    # Tests:
    
    M6_1_ext = MetricThread(
        name='M6x1.0',
        basic_major_diameter=6.0,
        pitch=1.0,
        tolerance_grade=4,
        allowance_class='h',
        external=True,
        profile='M',
        beta=30.0 * deg_to_rad,
    )
    
    M6_1_ext2 = ExternalMetricThread(
        name='M6x1.0',
        basic_major_diameter=6.0,
        pitch=1.0,
        tolerance_grade=4,
        allowance_class='h',
        profile='M',
        beta=30.0 * deg_to_rad,
    )
    
    M6_1_int = MetricThread(
        name='M6x1.0',
        basic_major_diameter=6.0,
        pitch=1.0,
        tolerance_grade=4,
        allowance_class='H',
        internal=True,
        profile='M',
        beta=30.0 * deg_to_rad,
    )
    
    M6_1_int2 = InternalMetricThread(
        name='M6x1.0',
        basic_major_diameter=6.0,
        pitch=1.0,
        tolerance_grade=4,
        allowance_class='H',
        profile='M',
        beta=30.0 * deg_to_rad,
    )



if __name__ == "__main__":
    main()
    