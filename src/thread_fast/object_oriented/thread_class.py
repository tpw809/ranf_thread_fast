"""Thread class."""
import json
import numpy as np


class Thread:
    def __init__(
            self, 
            diameter: float,
            pitch: float,
            es: float,
            external: bool=True,
        ):
        """
        Args:
            diameter: basic major diameter
            pitch: thread pitch [mm/thread]
            es: external thread upper deviation, based on tolerance
            external: external or internal thread?
        """
        # [mm], major (outer) diameter:
        self.d_major_basic = diameter
        
        # [mm/thread], thread pitch:
        self.pitch = pitch
        
        # upper deviation, external thread (fundamental deviation)
        # based on specified tolerance position (e,f,g,h)
        self.es = es
        
        # [mm], maximum major (outer) diameter:
        self.d_major_max = self.d_major_basic - self.es
        
        # [mm], fundamental triangle height:
        self.H = np.sqrt(3.0) / 2.0 * pitch
        
        # [mm], minor diameter:
        self.d_minor_basic = self.d_major_basic - self.H * (5.0/8.0)
        
        # [mm], pitch diameter:
        self.d_pitch_basic = self.d_major_basic - 0.5 * self.H
        
        # [mm], minimum root radius for rounded root threads:
        self.r_min = 0.125 * pitch
        
    def __str__(self):
        return "\n".join([
            f"pitch = {self.pitch}",
            f"H = {self.H}",
            f"r_min = {self.r_min}",
        ])


def main() -> None:
    
    m4x0_7 = Thread(
        diameter=4.0,
        pitch=0.7,
        es=0.022,
    )
    
    print(m4x0_7)


if __name__ == "__main__":
    main()
    