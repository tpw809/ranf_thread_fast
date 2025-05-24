"""Conversion Factors for unit conversions."""
import numpy as np


in_to_mm = 25.4
mm_to_in = 1.0 / 25.4


deg_to_rad = np.pi / 180.0
rad_to_deg = 180.0 / np.pi


psi_to_MPa = 0.00689476
MPa_to_psi = 145.038



def tpi_to_pitch_mm(tpi: float) -> float:
    """Convert from threads per inch (TPI) to metric pitch (mm/thread).
    
    To convert thread pitch to threads per inch (TPI), divide 25.4 (millimeters per inch) by the thread pitch in millimeters.
    """
    assert tpi > 0.0
    pitch = 25.4 / tpi
    return pitch


def pitch_mm_to_tpi(pitch: float) -> float:
    """Convert from metric pitch (mm/thread) to threads per inch (TPI).
    
    To convert thread pitch to threads per inch (TPI), divide 25.4 (millimeters per inch) by the thread pitch in millimeters.
    """
    assert pitch > 0.0
    tpi = 25.4 / pitch
    return tpi


# TODO: temperature F and C:
