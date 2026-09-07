"""Metric Bolt Class

References:
-Machinery Handbook 29th Edition
"""
import numpy as np

 
class MetricBolt:
    def __init__(
            self, 
            name='MetricBolt',
        ):
        self.name = name
        
        # yield strength of material:
        self.S_y = 1.0
        
        # preload:
        self.F_i = 1.0
        
        # modulus of elasticity:
        self.E = 200.0e6
        
        # length of threaded portion under load:
        self.l_t = 1.0
        
        # length of unthreaded portion of grip:
        self.l_d = 1.0
        
        # nominal bolt diameter:
        self.d = 1.0
        
        # 
        
    def recommended_preload(self):
        """Machinery Handbook 29th Edition: page 1521
        Fi = bolt preload
        A_t = tensile stress area
        S_p = proof strength
        """
        # for re-usable connections:
        F_i = 0.75 * A_t * S_p
        
        # for permanent connections:
        # F_i = 0.9 * A_t * S_p
        return F_i
        
    def A_t(self):
        """tensile stress area"""
        return 1.0
        
    def A_d(self):
        """major-diameter area of the bolt"""
        return 1.0
        
    def approximate_proof_strength(self):
        """Machinery Handbook 29th Edition: page 1521
        # S_y = yield strength of material
        """
        S_p = 0.85 * self.S_y
        return S_p
        
    def preload_elongation(self):
        """Machinery Handbook 29th Edition: page 1521
        # F_i = bolt preload
        # A_d = major-diameter area of the bolt
        # A_t = tensile stress area of the bolt
        # E = bolt modulus of elasticity
        # l_t = length of threaded portion within the grip
        # l_d = length of unthreaded portion of the grip
        # grip = total thickness of clamped material
        """
        num = F_i * A_d * l_t + A_t * l_d
        den = A_d * A_t * E
        delta = num / den
        return delta
        
    def preload_elongation_simple(self):
        """Machinery Handbook 29th Edition: page 1521
        # F_i = bolt preload
        # A = area of the bolt
        # E = bolt modulus of elasticity
        # l = grip length of the bolt
        # grip = total thickness of clamped material
        """
        delta = F_i * l / (A * E)
        return delta
        
    def wrench_torque_estimate(self):
        """Machinery Handbook 29th Edition: page 1521
        # F_i = bolt preload
        # K = constant depending on bolt material & size
        # d = nominal bolt diameter
        # T = wrench torque to apply preload
        """
        T = K * self.F_i * self.d
        return T
        
    def nut_factor(self):
        """a constant that depends on the
        # bolt material
        """
        K = 0.2
        return K
        
    def combined_tensile_stress(self):
        """Machinery Handbook 29th Edition: page 1524
        # combined tensile and torsion load
        # F_t = applied axial tensile stress
        # F_s = shear stress caused by torsion load
        # F_tc = combined tensile stress
        """
        F_tc = np.sqrt(F_t**2 + 3.0 * F_s**2)
        return F_tc
            
        
    def __str__(self):
        return "not yet implemented..."    


def main() -> None:
    mb1 = MetricBolt(name='mb1')
    print(mb1)
    mb1.combined_tensile_stress()
    mb1.nut_factor()
    mb1.wrench_torque_estimate()
    mb1.preload_elongation_simple()
    mb1.preload_elongation()
    mb1.A_t()
    mb1.recommended_preload()
    mb1.approximate_proof_strength()
    
    
if __name__ == "__main__":
    main()
    