"""Metric Fastener Class Definition

Timothy P Woodard

References:

Machinery Handbook 29th Ed.

NASA STD 5020A, 2018

NASA STD 5020B, 2021

Mil-Hdbk-60: threaded fasteners, tightening to proper tension
"""
import numpy as np


def combine_tensile_stress(
        sigma_t: float, 
        sigma_s: float,
    ) -> float:
    """combined tensile stress.
    
    Reference: 
    
    Warning: May be deprecated by NASA-TM-2012-217454
    
    Args:
        sigma_t (float): =
        sigma_s (float): =
    
    Returns:
        float: Combined stress.
    """
    return np.sqrt(sigma_t ** 2 + 3.0 * sigma_s ** 2)


class MetricFastener:
    def __init__(
            self,
            l_overall: float=10.0,
            l_shank: float=5.0,
        ):
        # name:
        self.size = 'M3x0.5mm'
        
        # [mm], length overall:
        self.l_overall = l_overall
        
        # [mm], length of shank (un-threaded portion of length):
        self.l_shank = l_shank
        
        # [mm], distance between subsequent threads:
        self.pitch = 0.5
        
        # [mm], major (outer) diameter:
        self.d_outer = 2.980
        
        # [mm], pitch diameter:
        # self.dp = 2.655
        
        # [mm], head washer bearing diameter:
        self.d_head = 5.0
        
        self.coarse = True
        
        # [MPa], ultimate tensile strength:
        self.sigma_u = 480.0
        
        # [MPa], yield strength:
        self.sigma_y = 410.0
        
        # [rad], thread angle:
        self.thread_angle = 60.0 * np.pi / 180.0
        
        # [mm], nominal clearance hole:
        self.clearance_hole_nom = 3.40
        
        # [mm], close clearance hole:
        self.clearance_hole_close = 3.20
        
        # [mm], loose clearance hole:
        self.clearance_hole_loose = 3.60
        
        # [mm], tapped hole size:
        self.tapped_hole = 2.8

        # e [MPa], young's modulus:
        self.e = 200.0e3

        # cte [mm/mm/C], coefficient of thermal expansion:
        self.cte = 5.0e-6

    @property
    def min_thread_eng_len(self) -> float:
        """[mm], minimum recommended thread engagement length"""
        return self.pitch * 3.0
        
    @property
    def area(self) -> float:
        """[mm^2], cross sectional area"""
        return np.pi * (self.d_outer / 2.0)**2

    @property
    def alpha(self) -> float:
        """thread angle, [rad]"""
        return self.thread_angle / 2.0
        
    @property
    def thread_tensile_stress_area(self) -> float:
        """stress area in threaded portion, [mm^2]"""
        return (np.pi / 4.0) * ((self.dm + self.dp) / 2.0)**2
        # return 0.7854 * (self.d_outer - 0.9382 * self.pitch)**2  # JIS method

    @property
    def thread_tensile_stress_area_jis(self) -> float:
        """stress area in threaded portion, [mm^2]
        JIS method:
        d_outer =
        pitch =
        """
        # return (np.pi / 4.0) * ((self.d2 + self.d3) / 2.0)**2
        return 0.7854 * (self.d_outer - 0.9382 * self.pitch)**2

    @property
    def h(self) -> float:
        """height of the fundamental thread triangle (based on JIS), [mm]
        pitch =
        """
        return 0.866025 * self.pitch

    @property
    def d1(self) -> float:
        """minor diameter of the external thread (based on JIS), [mm]
        d_outer =
        pitch =
        """
        return self.d_outer - 1.082532 * self.pitch

    @property
    def d2(self) -> float:
        """pitch diameter of the thread  (based on JIS), mm.
        d_outer =
        pitch =
        """
        return self.d_outer - 0.649515 * self.pitch
        
    @property
    def d3(self) -> float:
        """
        [mm], (based on JIS)
        d1 =
        h =
        """
        return self.d1 - self.h / 6.0

    @property
    def dm(self) -> float:
        """minor diameter, [mm]"""
        return self.d1
        
    @property
    def dp(self) -> float:
        """thread pitch diameter, [in]
        from machinery handbook 29th ed. page 1528
        """
        return self.d_outer - 0.649519 * self.pitch
        
    @property
    def da(self) -> float:
        """thread stress diameter, [mm]"""
        return np.sqrt(4.0 * self.thread_tensile_stress_area_jis / np.pi)

    def lb(self, lj: float, hn: float, hb: float) -> float:
        """effective bolt length for joint calculations, [mm]
        
        Args:
            lj: length of the clamped joint
            hn: length of the nut or threaded hole
            hb: length of the bolt head
        """

        # [mm], length of threaded portion:
        lt = lj - self.l_shank
        lb = (self.da / self.d_outer)**2 * (self.l_shank + hb / 2.0) + lt + (hn / 2.0)
        return lb

    def length_change(
            self, 
            preload: float, 
            lj: float,
        )  -> float:
        """change in bolt length due to tension, mm.
        
        F = k*x => x = F/k
        
        Args:
            preload = tension applied to the bolt
            lj = length of the joint
        """
        delta = preload * lj / (self.area * self.e)  # [mm]
        return delta
        
    def torque_for_tension(self, preload: float, k: float=0.2):
        """torque required for desired tension (preload), N-mm.
        
        Args:
            preload: tension load in the joint
            k: nut factor
        """

        # trq [N-mm]
        trq = k * preload * self.d_outer
        return trq
        
    def estimated_k(self, mus: float, muw: float) -> float:
        """Estimated nut factor.
        
        from Machinery's Handbook 29th, Page 1529
        
        Args:
            mus: coefficient of friction between the threads
            muw: coefficient of friction between bolt or nut bearing surfaces
        """
        
        # [rad], thread wedge angle:
        alpha = self.alpha
        
        # thread ramp angle:
        beta = self.pitch / (2.0 * np.pi * self.d_outer / 2.0)
        tanacosb = np.tan(alpha) * np.cos(beta)
        alpha_prime = np.arctan(tanacosb)

        # dw = [mm], equivalent diameter of bearing friction torque
        dw = (2.0 / 3.0) * (self.d_head**3 - self.d_outer**3) / (self.d_head**2 - self.d_outer**2)

        # k = nut factor
        k = 1.0 / (2.0 * self.d_outer) * (self.pitch / np.pi + mus * self.d2 / np.cos(alpha_prime) + muw * dw)
        return k

    def yield_clamping_force(self, mus: float) -> float:
        """
        Args:
            mus: 
        """
        # [rad], thread wedge angle
        alpha = self.alpha

        # thread ramp angle
        beta = self.pitch / (2.0 * np.pi * self.d_outer / 2.0)

        tanacosb = np.tan(alpha) * np.cos(beta)
        alpha_prime = np.arctan(tanacosb)
        num = self.sigma_y * self.thread_tensile_stress_area_jis

        # da =
        da = np.sqrt(4.0 * self.thread_tensile_stress_area_jis / np.pi)

        # pt =
        pt = (2.0 / da) * (self.pitch / np.pi + mus * self.d2 / np.cos(alpha_prime))
        den = np.sqrt(1.0 + 3.0*pt**2)
        return num / den  # [N]

    def tension_torque_t1(self, pb: float) -> float:
        """
        [N-mm], torque required to apply desired tension
        
        Args:
            pb: axial load (tension desired)
        """

        # beta [rad], ramp angle of the threads (helix, lead):
        beta = self.pitch / (np.pi * self.d2)
        return pb * np.tan(beta) * self.d2 / 2.0

    def thread_friction_torque_t2(
            self, 
            mu: float, 
            pb: float,
        ):
        """torque to overcome thread friction, N-mm.
        
        Args:
            mu: friction between threads
            pb: axial load (tension applied)
            d2:
            alpha:
        """
        return self.d2 * mu * pb / (2.0 * np.cos(self.alpha))

    def washer_friction_torque_t3(self, mu: float, pb: float):
        """torque to overcome friction between bearing surfaces, (N-mm).
        
        Args:
            mu: friction between bolt or nut head and bearing surface (washer)
            pb: axial load (tension applied)
            d_outer:
            d_head:
        """
        # [N-mm]
        return mu * pb * (self.d_outer + self.d_head) / 4.0

    def nut_turns_for_tension(
            self, 
            preload: float, 
            lj: float, 
            hn: float, 
            hb: float,
        ) -> float:
        """returns the angle necessary to reach desired preload
        
        Args:
            preload: target tension (preload)
            lj: 
            hn: 
            hb: 
            e: 
            pitch: 
        """

        # theta [deg]
        theta = 360.0 * preload * self.lb(lj, hn, hb) / (self.e * self.pitch)
        return theta
        
    def thread_section_stress(self, pb: float, trq: float):
        """stress in threaded cross section area, [MPa]
        
        Args:
            pb:
            trq:
        """

        # sigma [MPa]
        sigma = pb / self.thread_tensile_stress_area_jis
        j = np.pi * (self.da/2.0)**4 / 2.0

        # tau [N-mm * mm / mm^4]
        tau = trq * self.da / 2.0 / j
        return np.sqrt(sigma**2 + 3.0 * tau**2)

    def __str__(self):
        """called during print(object)"""
        return "\n".join([
            f'name = {self.size}',
            f'overall length = {self.l_overall} [mm]',
        ])


# TODO: change these child classes to generators using
# basic MetricFastener constructor...


class M2MetricFastener(MetricFastener):
    def __init__(
            self, 
            l_overall=10.0,  # [mm], length overall
            l_shank=4.0,  # [mm], length of shank (unthreaded portion of length)
        ):
        super().__init__(
            l_overall=l_overall,
            l_shank=l_shank,
        )
        self.size = 'M2x0.4mm'

        # [mm], distance between subsequent threads:
        self.pitch = 0.4
        
        # [mm], major (outer) diameter:
        self.d_outer = 2.0
        
        # [mm], head washer bearing diameter:
        self.d_head = 3.8
        
        self.coarse = True
        
        # [MPa], ultimate tensile strength:
        self.sigma_u = 440.0 / 0.8 

        # [MPa], yield strength:      
        self.sigma_y = 440.0
        
        # [rad], thread angle:
        self.thread_angle = 60.0 * np.pi / 180.0
        
        # [mm], nominal clearance hole:
        self.clearance_hole_nom = 2.40
        
        # [mm], close clearance hole:
        self.clearance_hole_close = 2.20
        
        # [mm], loose clearance hole:
        self.clearance_hole_loose = 2.60
        
        # [mm], tapped hole size:
        self.tapped_hole = 1.7

        # e [MPa], young's modulus:
        self.e = 200.0e3

        # cte [mm/mm/C], coefficient of thermal expansion:
        self.cte = 5.0e-6


class M3MetricFastener(MetricFastener):
    def __init__(
            self, 
            l_overall=10.0,  # [mm], length overall
            l_shank=4.0,  # [mm], length of shank (unthreaded portion of length)
        ):
        super().__init__(
            l_overall=l_overall,
            l_shank=l_shank,
        )
        self.size = 'M3x0.5mm'

        # [mm], distance between subsequent threads:
        self.pitch = 0.5
        
        # [mm], major (outer) diameter:
        self.d_outer = 3.0
        
        # [mm], head washer bearing diameter:
        self.d_head = 5.5
        
        self.coarse = True
        
        # [MPa], ultimate tensile strength:
        self.sigma_u = 440.0 / 0.8
        
        # [MPa], yield strength:
        self.sigma_y = 440.0
        
        # [rad], thread angle:
        self.thread_angle = 60.0 * np.pi / 180.0  
        
        # [mm], nominal clearance hole:
        self.clearance_hole_nom = 3.40
        
        # [mm], close clearance hole:
        self.clearance_hole_close = 3.20
        
        # [mm], loose clearance hole:
        self.clearance_hole_loose = 3.60
        
        # [mm], tapped hole size:
        self.tapped_hole = 2.7

        # e [MPa], young's modulus:
        self.e = 200.0e3

        # cte [mm/mm/C], coefficient of thermal expansion:
        self.cte = 5.0e-6


class M4MetricFastener(MetricFastener):
    def __init__(
            self, 
            l_overall=20.0,  # [mm], length overall
            l_shank=5.0,  # [mm], length of shank (unthreaded portion of length)
        ):
        super().__init__(
            l_overall=l_overall,
            l_shank=l_shank,
        )
        self.size = 'M4x0.7mm'

        # [mm], distance between subsequent threads:
        self.pitch = 0.7
        
        # [mm], major (outer) diameter:
        self.d_outer = 4.0
        
        # [mm], head washer bearing diameter:
        self.d_head = 7.0
        
        self.coarse = True
        
        # [MPa], ultimate tensile strength:
        self.sigma_u = 440.0 / 0.8
        
        # [MPa], yield strength:
        self.sigma_y = 440.0
        
        # [rad], thread angle:
        self.thread_angle = 60.0 * np.pi / 180.0
        
        # [mm], nominal clearance hole:
        self.clearance_hole_nom = 4.40
        
        # [mm], close clearance hole:
        self.clearance_hole_close = 4.20
        
        # [mm], loose clearance hole:
        self.clearance_hole_loose = 4.60
        
        # [mm], tapped hole size:
        self.tapped_hole = 3.7

        # e [MPa], young's modulus:
        self.e = 200.0e3

        # cte [mm/mm/C], coefficient of thermal expansion:
        self.cte = 5.0e-6


class M5MetricFastener(MetricFastener):
    def __init__(
            self, 
            l_overall=30.0,  # [mm], length overall 
            l_shank=10.0,  # [mm], length of shank (unthreaded portion of length)
        ):
        super().__init__(
            l_overall=l_overall,
            l_shank=l_shank,
        )
        self.size = 'M5x0.8mm'
        
        # [mm], distance between subsequent threads
        self.pitch = 0.8
        
        # [mm], major (outer) diameter:
        self.d_outer = 5.0
        
        # [mm], head washer bearing diameter:
        self.d_head = 8.5
        
        self.coarse = True
        
        # [MPa], ultimate tensile strength:
        self.sigma_u = 440.0 / 0.8
        
        # [MPa], yield strength:
        self.sigma_y = 440.0
        
        # [rad], thread angle:
        self.thread_angle = 60.0 * np.pi / 180.0
        
        # [mm], nominal clearance hole:
        self.clearance_hole_nom = 5.40
        
        # [mm], close clearance hole:
        self.clearance_hole_close = 5.20
        
        # [mm], loose clearance hole:
        self.clearance_hole_loose = 5.60
        
        # [mm], tapped hole size:
        self.tapped_hole = 4.7

        # e [MPa], young's modulus:
        self.e = 200.0e3

        # cte [mm/mm/C], coefficient of thermal expansion:
        self.cte = 5.0e-6


class M6MetricFastener(MetricFastener):
    def __init__(
            self, 
            l_overall=30.0,  # [mm], length overall
            l_shank=10.0,  # [mm], length of shank (unthreaded portion of length)
        ):
        super().__init__(
            l_overall=l_overall,
            l_shank=l_shank,
        )
        self.size = 'M6x1.0mm'
        
        # [mm], distance between subsequent threads:
        self.pitch = 1.0
        
        # [mm], major (outer) diameter:
        self.d_outer = 6.0
        
        # [mm], head washer bearing diameter:
        self.d_head = 10.0
        
        self.coarse = True
        
        # [MPa], ultimate tensile strength:
        self.sigma_u = 440.0 / 0.8
        
        # [MPa], yield strength:
        self.sigma_y = 440.0
        
        # [rad], thread angle:
        self.thread_angle = 60.0 * np.pi / 180.0
        
        # [mm], nominal clearance hole:
        self.clearance_hole_nom = 6.40
        
        # [mm], close clearance hole:
        self.clearance_hole_close = 6.20
        
        # [mm], loose clearance hole:
        self.clearance_hole_loose = 6.60
        
        # [mm], tapped hole size:
        self.tapped_hole = 5.7

        # e [MPa], young's modulus
        self.e = 200.0e3

        # cte [mm/mm/C], coefficient of thermal expansion
        self.cte = 5.0e-6


class M10MetricFastener(MetricFastener):
    def __init__(
            self, 
            l_overall=50.0,  # [mm], length overall
            l_shank=20.0,  # [mm], length of shank (unthreaded portion of length)
        ):
        super().__init__(
            l_overall=l_overall,
            l_shank=l_shank,
        )
        self.size = 'M10x1.5mm'
        
        # [mm], distance between subsequent threads:
        self.pitch = 1.5
        
        # [mm], major (outer) diameter:
        self.d_outer = 10.0
        
        # [mm], head washer bearing diameter:
        self.d_head = 16.0
        
        self.coarse = True
        
        # [MPa], ultimate tensile strength:
        self.sigma_u = 640.0 / 0.8
        
        # [MPa], yield strength:
        self.sigma_y = 640.0
        
        # [rad], thread angle:
        self.thread_angle = 60.0 * np.pi / 180.0
        
        # [mm], nominal clearance hole:
        self.clearance_hole_nom = 10.60
        
        # [mm], close clearance hole:
        self.clearance_hole_close = 10.40
        
        # [mm], loose clearance hole:
        self.clearance_hole_loose = 10.80
        
        # [mm], tapped hole size:
        self.tapped_hole = 9.7

        # e [MPa], young's modulus:
        self.e = 200.0e3

        # cte [mm/mm/C], coefficient of thermal expansion:
        self.cte = 5.0e-6


# M12
# M14

def main() -> None:
    met_fast = MetricFastener(
        l_overall=40.0, 
        l_shank=20.0,
    )
    
    m2 = M2MetricFastener(l_overall=15.0, l_shank=5.0)
    m3 = M3MetricFastener(l_overall=15.0, l_shank=5.0)
    m4 = M4MetricFastener(l_overall=20.0, l_shank=5.0)
    m5 = M5MetricFastener(l_overall=30.0, l_shank=10.0)
    m6 = M6MetricFastener(l_overall=30.0, l_shank=10.0)
    m10 = M10MetricFastener(l_overall=50.0, l_shank=20.0)


if __name__ == "__main__":
    main()
    