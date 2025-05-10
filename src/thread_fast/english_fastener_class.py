"""English Fastener Class Definition
Timothy P Woodard
July 1, 2021
"""
import numpy as np

# UTS = Unified Thread Standard
# UN = Unified Thread Standard 
# UNC = Unified Thread Standard Coarse
# UNF = Unified Thread Standard Fine
# UNF = Unified Thread Standard Extra Fine
# UNJ = Unified Thread Standard Inch Aerospace Modified Thread (larger dm)


class EnglishFastener:
    def __init__(self):
        self.size = '1/4in UNC'
        self.thread_type = 'UNC'
        
        # [in], length overall:
        self.lo = 3.0
        
        # [in], length of shank (unthreaded portion of length):
        self.l_shank = 1.0
        
        # [tpi], threads per inch:
        self.n = 20.0
        
        # [in], distance between subsequent threads:
        self.pitch = 1.0 / self.n
        
        # [in], major (outer) diameter:
        self.d_outer = 0.25
        
        # [in], head washer bearing diameter:
        self.dh = 0.435
        self.coarse = True
        
        # [rad], thread angle:
        self.thread_angle = 60.0 * np.pi / 180.0
        
        # [in], nominal clearance hole:
        self.clearance_hole_nom = 0.28
        
        # [in], close clearance hole:
        self.clearance_hole_close = 0.26
        
        # [in], loose clearance hole:
        self.clearance_hole_loose = 0.30
        
        # [in], tapped hole size:
        self.tapped_hole = 0.23
        
        ###############################
        # Material Properties:
        ###############################
        
        # [psi], ultimate tensile strength
        self.sigma_u = 80.0e3
        
        # [psi], yield strength:
        self.sigma_y = 80.0e3
        
        # [psi], young's modulus:
        self.e = 29.0e6
        
        # [in/in/F], coefficient of thermal expansion:
        self.cte = 5.0e-6

    @property
    def dp(self):  
        """# [in], thread pitch diameter
        # from machinery handbook 29th ed. page 1528
        """
        return self.d_outer - 0.649519 * self.pitch
        
    @property
    def dm(self):  
        """# [in], thread minor diameter
        from machinery handbook 29th ed. page 1528
        """
        # return self.d_outer - 1.082532 * self.pitch
        return self.d_outer - 1.299038 * self.pitch

    @property
    def thread_tensile_stress_area(self):  
        """# [in^2], stress area in threaded portion"""
        return (np.pi / 4.0) * ((self.dm + self.dp) / 2.0)**2
        
    @property
    def min_thread_eng_len(self):  # [in]
        return self.pitch * 3.0
        
    @property
    def da(self):  
        """# [in], thread stress diameter"""
        return np.sqrt(4.0 * self.thread_tensile_stress_area / np.pi)
        
    def tension_torque_t1(self, pb):  
        """# [in-lb], torque required to apply desired tension
        # pb = axial load (tension desired)
        """
        # [rad], ramp angle of the threads (helix, lead)
        beta = self.pitch / (np.pi * self.dp)
        return pb * np.tan(beta) * self.dp / 2.0  # [in-lb]

    def thread_friction_torque_t2(self, mu, pb):  
        """# [in-lb], torque to overcome thread friction
        # mu = friction between threads
        # pb = axial load (tension applied) [lb]
        """
        return self.dp * mu * pb / (2.0 * np.cos(self.alpha))  # [in-lb]

    def washer_friction_torque_t3(self, mu, pb):  
        """# [in-lb], torque to overcome friction between bearing surfaces
        # mu = friction between bolt or nut head and bearing surface (washer)
        # pb = axial load (tension applied) [lb]
        """
        return mu * pb * (self.d_outer + self.dh) / 4.0  # [in-lb]

    def nut_turns_for_tension(self, preload, lj, hn, hb):
        # preload = target tension
        # lj = length of the clamped joint
        # hn = height of the nut
        # hb = height of the bolt head
        theta = 360.0 * preload * self.lb(lj, hn, hb) / (self.e * self.pitch)
        return theta  # [deg]
        
    def lb(self, lj, hn, hb):  
        """[in], effective bolt length for joint calculations
        # lj = length of the clamped joint
        # hn = length of the nut or threaded hole
        # hb = length of the bolt head
        """
        lt = lj - self.l_shank  # [in], length of threaded portion
        lb = (self.da / self.d_outer)**2 * (self.l_shank + hb / 2.0) + lt + (hn / 2.0)
        return lb
        
    def length_change(self, preload, lj):  
        """[in], change in bolt length due to tension
        Args:
            preload = tension applied to the bolt [lb]
            lj = length of the joint [in]
        """
        delta = preload * lj / (self.thread_tensile_stress_area * self.e)  # [in]
        return delta
        
    def torque_for_tension(self, preload, k=0.2):  
        """# [in-lb], torque required for desired tension (preload)"""
        torque = k * preload * self.d_outer
        return torque

    @property
    def alpha(self):
        return self.thread_angle / 2.0  # [rad]
        
    def estimated_k(self, mus, muw):
        """from Machinery's Handbook 29th ed., Page 1529
        mus = coefficient of friction between the threads
        muw = coefficient of friction between bolt or nut bearing surfaces
        """
        alpha = self.alpha  # [rad], thread wedge angle
        beta = self.pitch / (2.0 * np.pi * self.d_outer / 2.0)  # thread ramp angle
        tanacosb = np.tan(alpha) * np.cos(beta)
        alpha_prime = np.arctan(tanacosb)
        # dw = [mm], equivalent diameter of bearing friction torque
        dw = (2.0 / 3.0) * (self.dh**3 - self.d_outer**3) / (self.dh**2 - self.d_outer**2)
        k = 1.0 / (2.0 * self.d_outer) * (self.pitch / np.pi + mus * self.dp / np.cos(alpha_prime) + muw * dw)
        return k

    def yield_clamping_force(self, mus):
        
        # [rad], thread wedge angle:
        alpha = self.alpha
        
        # thread ramp angle:
        beta = self.pitch / (2.0 * np.pi * self.d_outer / 2.0)
        tanacosb = np.tan(alpha) * np.cos(beta)
        alpha_prime = np.arctan(tanacosb)
        num = self.sigma_y * self.thread_tensile_stress_area
        dA = np.sqrt(4.0 * self.thread_tensile_stress_area / np.pi)
        pt = (2.0 / dA) * (self.pitch / np.pi + mus * self.dp / np.cos(alpha_prime))
        den = np.sqrt(1.0 + 3.0*pt**2)
        return num / den  # [lb]
        
    def thread_section_stress(self, pb, torque):  
        """# [psi], stress in threaded cross section area"""
        sigma = pb / self.thread_tensile_stress_area  # [psi]
        j = np.pi * (self.da/2.0)**4 / 2.0
        tau = torque * self.da / 2.0 / j  # [in-lb * in / in^4]
        return np.sqrt(sigma**2 + 3.0 * tau**2)
        
"""  
    @property
    def area(self):
        return np.pi * (self.d_outer / 2.0)**2  # [in^2], cross sectional area

    @property
    def h(self):  
        # [in], height of the fundamental thread triangle (based on JIS)
        return 0.866025 * self.pitch

    @property
    def d1(self):  
        # [in], minor diameter of the external thread (based on JIS)
        return self.d_outer - 1.082532 * self.pitch

    @property
    def d2(self):  
        # [in], pitch diameter of the thread  (based on JIS)
        return self.d_outer - 0.649515 * self.pitch
        
    @property
    def d3(self):  
        # [in], (based on JIS)
        return self.d1 - self.h / 6.0

    def combine_tensile_stress(self, sigma_t, sigma_s):
        # [psi], combined tensile stress
        return np.sqrt(sigma_t**2 + 3.0 * sigma_s**2)
"""
