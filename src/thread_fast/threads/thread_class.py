"""ScrewThread class definition.

Units? Try to be unitless?

basic_major_diameter in inches or mm

pitch in inches/thread or mm/thread

"""
import numpy as np
import thread_fast.conversion_factors as cf


class ScrewThread:
    """ScrewThread class.
    
    Args:
        name (str): Descriptive name.
        basic_major_diameter (float): Basic (nominal) major diameter.
        pitch (float): thread pitch.
        beta_rad (float): Thread half angle in radians.
        beta_deg (float): Thread half angle in degrees.
    """
    def __init__(
            self,
            name: str,
            basic_major_diameter: float,
            pitch: float,
            beta_rad: float=30.0 * cf.deg_to_rad,
            beta_deg: float=None,
        ):
            
        self.name = name
        
        # basic major diameter:
        self.basic_major_diameter = basic_major_diameter
        
        # [rad], thread half angle:
        self.beta_rad = beta_rad
        
        if beta_deg is not None:
            self.beta_rad = beta_deg * cf.deg_to_rad
        
        # thread pitch:
        self.pitch = pitch

        # height of fundamental triangle:
        # from: iso 68
        self.fundamental_triangle_height = (np.sqrt(3.0) / 2.0) * self.pitch

    @property
    def H(self) -> float:
        """Fundamental triangle height."""
        return self.fundamental_triangle_height

    @classmethod
    def from_dict(cls, input_dict):
        """Create ScrewThread object from input dictionary.
        
        Mandatory items:
        - name
        - basic_major_diameter
        - pitch
        
        Optional:
        - beta_rad
        - beta_deg
        """
        assert input_dict['type'] == 'ScrewThread'
        
        if 'beta_rad' in input_dict:
            beta_rad = input_dict['beta_rad']
        else:
            beta_rad = None
        
        if 'beta_deg' in input_dict:
            beta_deg = input_dict['beta_deg']
        else:
            beta_deg = None
        
        return ScrewThread(
            name=input_dict['name'],
            basic_major_diameter=input_dict['basic_major_diameter'],
            pitch=input_dict['pitch'],
            beta_rad=beta_rad,
            beta_deg=beta_deg,
        )
    
    def to_dict(self) -> dict:
        return {
            "type": 'ScrewThread',
            # Inputs:
            "name": self.name,
            "pitch": self.pitch,
            "basic_major_diameter": self.d,
            "beta_rad": self.beta_rad,  # default uses beta_rad
            "fundamental_triangle_height": self.H,
        }

    def __str__(self):
        return "\n".join([
            "\nScrewThread:",
            f"name = {self.name}",
            f"basic_major_diameter = {self.basic_major_diameter}",
            f"pitch = {self.pitch}",
            f"beta_rad = {self.beta_rad}",
            f"beta_deg = {self.beta_rad * cf.rad_to_deg}",
            f"fundamental_triangle_height = {self.H}",
            "",
        ])


def main() -> None:
    # Tests:
    test_thread = ScrewThread(
        name='test_thread',
        basic_major_diameter=6.0,
        pitch=1.0,
        beta_rad=30.0 * cf.deg_to_rad,
        beta_deg=None,
    )
    print(test_thread)
    
    test_thread2 = ScrewThread(
        name='test_thread',
        basic_major_diameter=6.0,
        pitch=1.0,
        beta_rad=30.0 * cf.deg_to_rad,
    )
    print(test_thread2)
    
    test_thread3 = ScrewThread(
        name='test_thread',
        basic_major_diameter=6.0,
        pitch=1.0,
        beta_deg=30.0,
    )
    print(test_thread3)


if __name__ == "__main__":
    main()
    