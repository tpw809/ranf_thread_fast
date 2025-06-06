"""Equations from NSTS 08307 Rev A

Criteria for Preloaded Bolts
"""
import numpy as np
from typing import Tuple

########################################################
# 3.0 Required Criteria for Preloaded Bolts: pg 3-1
########################################################

# Basic Requirements:
# adequate strength (at max preload & max external load)
# no joint separation (at min preload & max external load)
# fracture & fatigue life

# need to estimate max and min preloads...
# no factor of safety put on preload (use min & max estimated)
# safety factors applied to external loads

########################################################
# 3.2 Definitions: pg 3-1
########################################################


########################################################
# 3.2.2 Definition of Symbols: pg 3-2
########################################################

# a. External/Internal Loads:

# P = External axial load applied to joint at bolt location due to application of limit load to the structure
# Pb = Bolt axial load resulting from yield, ultimate or joint separation load
# V = Bolt shear load resulting from limit load
# M = Bolt bending moment resulting from limit load

# b. Factors of Safety:
# SF = Bolt strength factor of safety
# SFsep = Joint separation factor of safety

# c. Allowables/Strengths:
# PAt = Axial load allowable of bolt due to tension
# PAs = Axial load allowable of bolt or nut due to thread shear
# VA = Shear load allowable of bolt
# MA = Bending load allowable of bolt


########################################################
# 3.3 Calculation of Max and Min Preloads: pg 3-5
########################################################

# 1. Typical Coefficient Method:

# K_typ = typical nut factor
# K_min = minimum nut factor
# K_max = maximum nut factor


def nut_factor(
        R_t: float, 
        R_e: float, 
        mu_t_min: float,
        mu_t_typ: float, 
        mu_t_max: float,
        mu_b_min: float,
        mu_b_typ: float, 
        mu_b_max: float,
        alpha: float, 
        beta: float, 
        D: float,
    ) -> Tuple[float, float, float]:
    """Calculate nut factor, K.
    
    NSTS 08307 Rev A, pg 3-5 to 3-6
    
    Args:
        R_t: Effective radius of thread forces (1/2 x E approximately)
        R_e: Effective radius of torqued element-to-joint bearing forces = 1/2 x (Ro + Ri)
        mu_t_typ: typical coefficient of friction at the external-to-internal thread interface
        mu_b_typ: typical coefficient of friction at the nut-to-joint bearing interface
        alpha: Thread lead angle (Tan^-1 [1/(n_0*pi*E)] for unified thread form)
        beta: Thread half angle (30° for unified thread form)
        D: Basic major diameter of external threads (bolt)
    Returns:
        Tuple[float, float, float]: estimated nut factor
    """
    K_typ = (R_t * (np.tan(alpha) + mu_t_typ / np.cos(beta)) + R_e * mu_b_typ) / D
    
    K_min = (R_t * (np.tan(alpha) + mu_t_min / np.cos(beta)) + R_e * mu_b_min) / D
    
    K_max = (R_t * (np.tan(alpha) + mu_t_max / np.cos(beta)) + R_e * mu_b_max) / D
    
    return K_min, K_typ, K_max



def max_preload(
        gamma: float, 
        T_max: float,
        K_typ: float,
        D: float,
        P_thr_pos: float=0.0,
        K_min: float=None,
    ) -> float:
    """Calculate max preload, PLD_max.
    
    NSTS 08307 Rev A, pg 3-5 & 3-6
    
    Args:
        gamma: preload uncertainty factor
        T_max: maximum applied (specified) torque to tighten fastener
        K_typ: typical nut factor
        D: nominal fastener diameter
        P_thr_pos: thermally induced load that increases the preload
        K_min: minimum expected nut factor
    Returns:
        float: maximum predicted preload
    """
    assert gamma >= 0.0
    assert D > 0.0
    assert K_typ > 0.0
    assert P_thr_pos >= 0.0, "error, P_thr_pos must increase the preload"
    # TODO: finish... PLD input & TOL
    
    # 1. Typical Coefficient Method:
    PLD_max = (1.0 + gamma) * T_max / (K_typ * D) + P_thr_pos
    
    # 2.0 Experimental Coefficient Method:
    if K_min is not None:
        print("using experimental coefficient method...")
        PLD_max = T_max / (K_min * D) + P_thr_pos
    return PLD_max


def min_preload(
        gamma: float, 
        T_min: float,
        K_typ: float,
        T_p: float,
        D: float,
        P_thr_neg: float=0.0,
        relaxation_ratio: float=0.05,
        P_loss: float=None,
        K_max: float=None,
    ) -> float:
    """Calculate min preload, PLD_min.
    
    NSTS 08307 Rev A, pg 3-5 & 3-6
    
    Args:
        gamma: preload uncertainty factor
        T_min: minimum applied (specified) torque to tighten fastener
        K_typ: typical nut factor
        T_p: prevailing torque
        D: nominal fastener diameter
        P_thr_neg: thermally induced load that decreases the preload
        relaxation_ratio: assumed preload percentage loss due to relaxation
        K_max: maximum expected nut factor
    Returns:
        float: minimum predicted preload
    """
    assert gamma >= 0.0
    assert D > 0.0
    assert K_typ > 0.0
    assert P_thr_neg <= 0.0, "error, P_thr_neg must decrease the preload"
    assert relaxation_ratio >= 0.0
    # TODO: finish...  PLD input & TOL
    
    # 1. Typical Coefficient Method:
    if P_loss is not None:
        PLD_min = (1.0 - gamma) * (T_min - T_p) / (K_typ * D) + P_thr_neg - P_loss
    else:
        PLD_min = ((1.0 - gamma) * (T_min - T_p) / (K_typ * D) + P_thr_neg) / (1.0 + relaxation_ratio)
    
    # 2.0 Experimental Coefficient Method:
    if K_max is not None:
        print("using experimental coefficient method...")
        if P_loss is not None:
            PLD_min = (T_min - T_p) / (K_max * D) + P_thr_neg - P_loss
        else:
            PLD_min = ((T_min - T_p) / (K_max * D) + P_thr_neg) / (1.0 + relaxation_ratio)
    return PLD_min


########################################################
# 3.4 Typical Preload Uncertainties: pg 3-6
########################################################

# None.

########################################################
# 3.5 Typical Coefficients of Friction / Nut Factor: pg 3-7
########################################################

# None.

########################################################
# 3.6 Expected Preload Loss: pg 3-8
########################################################

# P_loss = 0.05 * PLD_max
# input: relaxation_ratio
# included in max_preload & min_preload functions

########################################################
# 3.7 Preloaded Bolt Strength Criteria: pg 3-8
########################################################


def bolt_axial_load_for_strength(
        PLD_max: float, 
        n: float, 
        phi: float, 
        SF: float, 
        P: float,
    ) -> float:
    """Bolt axial load resulting from yield, ultimate or joint separation load, P_b.
    
    Used for strength margin calculations (highest expected load in the bolt).
    
    NSTS 08307 Rev A, pg 3-9
    
    Args:
        PLD_max: maximum preload
        phi: stiffness parameter
        n: loading plane factor
        SF: safety factor
        P: External axial load applied to joint at bolt location due to application of limit load to the structure
    Returns:
        float: bolt axial load used for strength margins
    """
    assert SF >= 1.0, "error: SF must be >= 1.0"
    assert 0.0 <= n <= 1.0
    P_b = PLD_max + n * phi * (SF * P)
    return P_b


# a. Axial Load: pg 3-9
# 1. Minimum cross section of Bolt: pg 3-9


def bolt_tensile_margin(
        PA_t: float, 
        SF: float, 
        P: float, 
        P_b: float,
    ):
    """Calculate margin of safety for bolt tensile failure.
    
    NSTS 08307 Rev A, pg 3-9
    
    Args:
        PA_t: bolt tensile load allowable
        SF: safety factor
        P: External axial load applied to joint at bolt location due to application of limit load to the structure
        P_b: Bolt axial load resulting from yield, ultimate or joint separation load
    Returns:
        float: margin of safety for bolt tensile failure
    """
    assert SF >= 1.0, "error: SF must be >= 1.0"
    MS_crit1 = PA_t / (SF * P) - 1.0
    MS_crit2 = PA_t / P_b - 1.0
    return MS_crit1, MS_crit2


# 2. Shear Pull-Out of Threads: pg 3-9


def thread_shear_pull_out_margin(
        PA_s: float, 
        SF: float, 
        P: float, 
        P_b: float,
    ) -> float:
    """Calculate margin of safety for thread shear pullout failure.
    
    NSTS 08307 Rev A, pg 3-10
    
    Only checked at ultimate load.
    
    Args:
        PA_s: thread shear load allowable
        SF: safety factor
        P: External axial load applied to joint at bolt location due to application of limit load to the structure
        P_b: Bolt axial load resulting from yield, ultimate or joint separation load
    Returns:
        float: margin of safety for thread shear pullout failure
    """
    assert SF >= 1.0, "error: SF must be >= 1.0"
    MS_crit1 = PA_s / (SF * P) - 1.0
    MS_crit2 = PA_s / P_b - 1.0
    return MS_crit1, MS_crit2


# b. Shear Load:


def shear_margin(VA: float, SF: float, V: float) -> float:
    """Calculate margin of safety for shear.
    
    NSTS 08307 Rev A, pg 3-10
    
    Args:
        VA: shear load allowable of bolt
        SF: safety factor
        V: Bolt shear load resulting from limit load
    Returns:
        float: margin of safety for shear
    """
    assert SF >= 1.0, "error: SF must be >= 1.0"
    MS = (VA / (SF * V)) - 1.0
    return MS


# c. Bending Load:


def bending_margin(MA: float, SF: float, M: float) -> float:
    """Calculate margin of safety for bending.
    
    NSTS 08307 Rev A, pg 3-10
    
    Args:
        MA: bending load allowable of bolt
        SF: safety factor
        M: Bolt bending load resulting from limit load
    Returns:
        float: margin of safety for bending
    """
    assert SF >= 1.0, "error: SF must be >= 1.0"
    MS = (MA / (SF * M)) - 1.0
    return MS


# d. Combined Axial, Shear and/or Bending Load:


def axial_load_ratio(
        SF: float, 
        P: float, 
        PA_t: float, 
        P_b: float, 
        PLD_max: float,
    ) -> float:
    """Calculate ratio of axial load to axial load allowable.
    
    NSTS 08307 Rev A, pg 3-10
    
    Args:
        SF:
        P:
        PA_t:
        P_b:
        PLD_max:
    Returns:
        float: Ratio of axial load to axial load allowable
    """
    assert SF >= 1.0, "error: SF must be >= 1.0"
    R_a1 = (SF * P) / PA_t
    R_a2 = P_b / PA_t
    R_a3 = PLD_max / PA_t
    return np.max([R_a1, R_a2, R_a3])


def bending_load_ratio(
        SF: float, 
        M: float, 
        MA: float, 
        K_p: float=1.0,
    ) -> float:
    """Calculate ratio of bending load to bending allowable, R_b.
    
    NSTS 08307 Rev A, pg 3-10 & 3-11
    
    Used in combined loading criteria.
    
    Args:
        SF: factor of safety
        M: Bolt bending moment resulting from limit load
        MA: Bending load allowable of bolt
        K_p: plastic bending factor
    Returns: 
        float: Ratio of bending load to bending allowable
    """
    assert SF >= 1.0, "error: SF must be >= 1.0"
    R_b = (SF * M) / (MA * K_p)
    return R_b


def shear_load_ratio(SF: float, V: float, VA: float) -> float:
    """Calculate ratio of shear load to shear load allowable.
    
    Args:
        SF: safety factor
        V:
        VA:
    Returns:
        float: Ratio of shear load to shear load allowable
    """
    assert SF >= 1.0, "error: SF must be >= 1.0"
    R_s = (SF * V) / VA
    return R_s


def combined_load_margin(
        R_a: float, 
        R_b: float, 
        R_s: float,
        K: float,
    ) -> float:
    """Calculate combined load failure criterion.
    
    Result must be > 1.0
    
    Deprecated, see: 
    
    Args:
        R_a: Ratio of axial load to axial load allowable
        R_b: Ratio of bending load to bending load allowable
        R_s: Ratio of shear load to shear load allowable
        K: plastic bending factor
    Returns:
        float: combined load failure criterion
    """
    print("warning: this criteria for combined loading is deprecated")
    return (R_a + R_b/K)**2 + R_s**3 


########################################################
# 3.8 Plastic Bending: pg 3-10
########################################################

# a. bending load:


def bolt_bending_margin(
        MA: float, 
        K_p: float, 
        SF: float, 
        M: float,
    ) -> float:
    """Calculate margin of safety for bolt bending failure.
    
    NSTS 08307 Rev A, pg 3-11
    
    For bending load only and ductile material.
    
    Args:
        MA: Bending load allowable of bolt
        K_p: plastic bending factor
        SF: factor of safety
        M: Bolt bending moment resulting from limit load
    Returns:
        float: margin of safety for bolt bending failure
    """
    assert SF >= 1.0, "error: SF must be >= 1.0"
    MS = (MA * K_p) / (SF * M) - 1.0
    return MS


# b. combined axial, shear, and/or bending load:


def combined_load_margin2(
        R_a: float, 
        R_b: float, 
        R_s: float,
    ) -> float:
    """Calculate combined load failure criterion.
    
    Result must be > 1.0
    
    R_a**2 + R_b + R_s**3 <= 1.0
    
    Deprecated, see: 
    
    Args:
        R_a: Ratio of axial load to axial load allowable
        R_b: Ratio of bending load to bending load allowable
        R_s: Ratio of shear load to shear load allowable
        K: plastic bending factor
    Returns:
        float: combined load failure criterion
    """
    print("warning: this criteria for combined loading is deprecated")
    return R_a**2 + R_b + R_s**3 


########################################################
# 3.9 Preloaded Bolt Separation Criteria: pg 3-11
########################################################


def bolt_axial_load_for_separation(
        PLD_min: float,
        n: float,
        phi: float,
        P_sep: float,
    ) -> float:
    """Calculate bolt axial load resulting from yield, ultimate or joint separation load, P_b.
    
    Used in Joint separation margin.
    
    NSTS 08307 Rev A, pg 3-12
    
    Args:
        phi: stiffness parameter
        n: loading plane factor
        P_sep: 
        PLD_min: minimum preload
    Returns:
        float: bolt axial load (used for joint separation margin)
    """
    assert 0.0 <= n <= 1.0
    P_b = PLD_min + n * phi * P_sep
    return P_b


def joint_separation_load(P: float, SF_sep: float) -> float:
    """Calculate joint separation load, P_sep.
    
    NSTS 08307 Rev A, pg 3-12
    
    Args:
        P: External axial load applied to joint at bolt location due to application of limit load to the structure
        SF_sep: factor of safety for joint separation
    Returns:
        float: joint separation load
    """
    assert SF_sep >= 1.0, "error: SF_sep must be >= 1.0"
    P_sep = P * SF_sep
    return P_sep


def joint_separation_margin_of_safety(
        PLD_min: float, 
        n: float, 
        phi: float,
    ) -> float:
    """Calculate margin of safety for joint separation, MS_sep.
    
    NSTS 08307 Rev A, pg 3-12
    
    Only for P_b < tensile yield allowable of the bolt.
    
    Args:
        PLD_min: minimum preload
        n: loading plane factor 
        phi: stiffness factor
    Returns:
        float: margin of safety for joint separation
    """
    assert 0.0 <= n <= 1.0
    MS_sep = PLD_min / (1.0 - n * phi) - 1.0
    return MS_sep



########################################################
# 3.10 Preloaded Bolt Fatigue & Fracture Criteria: pg 3-12
########################################################

# None.

########################################################
# 3.11 Re-Torquing of Preloaded Bolts: pg 3-12
########################################################

# None.

########################################################
# Appendix A: Bolt Axial Load Allowables: pg A-3
########################################################

# Two axial load allowables are referenced in this criteria.
# The tensile axial load allowable (PAt) is based on the minimum cross-sectional area of the bolt and is a measure of the ability of the main body of the bolt to withstand load. 
# The thread shear axial load allowable (PAs) is based on the smaller of the two thread shear load allowables.

########################################################
# 1.0 Axial Load Allowable Due to Tension: pg A-4
########################################################

# If a minimum ultimate tensile load is given for a bolt, the axial load allowables are calculated as follows:


def tensile_axial_load_allowable_yield(
        F_ty: float, 
        F_tu: float,
    ) -> float:
    """Calculate tensile axial load allowable, PA_t_yield
    
    NSTS 08307 Rev A, pg A-4
    
    Args:
        F_ty: Minimum tensile yield strength of bolt
        F_tu: Minimum tensile ultimate strength of bolt
    Returns:
        float: allowable yield tensile load
    """
    PA_t_yield = (F_ty / F_tu) * minimum_ultimate_tensile_load
    return PA_t_yield


def tensile_axial_load_allowable_ultimate(
        minimum_ultimate_tensile_load: float,
    ) -> float:
    """Calculate tensile axial ultimate load allowable, PA_t.
    
    NSTS 08307 Rev A, pg A-4
    
    Args:
        minimum_ultimate_tensile_load:
    Returns:
        float: tensile axial ultimate load allowable
    """
    PA_t_ultimate = minimum_ultimate_tensile_load
    return PA_t_ultimate


# If a minimum ultimate tensile load is not given for a bolt, the axial load allowables must be determined from testing or calculated using the following equations:


def tensile_axial_load_allowable_yield(
        A_t: float, 
        F_ty: float,
    ) -> float:
    """Calculate tensile allowable load against yield failure.
    
    NSTS 08307 Rev A, pg A-4
    
    Args:
        A_t: tensile stress area of the bolt
        F_ty: Minimum tensile yield strength of bolt
    Returns:
        float: allowable yield tensile load
    """
    assert A_t > 0.0
    PA_t_yield = A_t * F_ty
    return PA_t_yield


def tensile_axial_load_allowable_ultimate(
        A_t: float, 
        F_tu: float,
    ) -> float:
    """Calculate tensile allowable load against ultimate failure.
    
    NSTS 08307 Rev A, pg A-4
    
    Args:
        A_t: tensile stress area of the bolt
        F_tu: Minimum tensile ultimate strength of bolt
    Returns:
        float: tensile allowable load against ultimate failure
    """
    assert A_t > 0.0
    PA_t_ultimate = A_t * F_tu
    return PA_t_ultimate


def bolt_tensile_stress_area(
        D_e_bsc: float, 
        n_0: float,
        pitch: float=None,
    ) -> float:
    """Calculate tensile stress area of the bolt, A_t.
    
    NSTS 08307 Rev A, pg A-4
    
    To convert thread pitch to threads per inch (TPI), divide 25.4 (millimeters per inch) by the thread pitch in millimeters. 
    
    Args:
        D_e_bsc: basic (nominal) major diameter of external threads
        n_0: threads per inch (tpi)
        pitch: thread pitch, mm
    Returns:
        float: tensile stress area of the bolt
    """
    if n_0 is None:
        assert pitch is not None
        n_0 = 25.4 / pitch 
    A_t = 0.7854 * (D_e_bsc - 0.9743 / n_0)**2
    return A_t


########################################################
# 2.0 Axial Load Allowable Due to Thread Shear: pg A-4
########################################################

# The axial load allowable due to thread shear is the smaller of the external thread shear load allowable (Pse) and the internal thread shear load allowable (Psi). These two allowables are calculated as follows:


def external_thread_shear_load_allowable(
        A_se: float,
        F_su_bolt: float,
    ) -> float:
    """Calculate external thread shear load allowable, P_se.
    
    NSTS 08307 Rev A, pg A-4
    
    Args:
        A_se: external thread shear area
        F_su_bolt: Minimum shear ultimate strength of bolt
    Returns:
        float: external thread shear load allowable
    """
    assert A_se > 0.0
    P_se = A_se * F_su_bolt
    return P_se


def internal_thread_shear_load_allowable(
        A_si: float, 
        F_su_nut: float,
    ) -> float:
    """Calculate internal thread shear load allowable, P_si.
    
    NSTS 08307 Rev A, pg A-4
    
    Args:
        A_si: internal thread shear area
        F_su_nut: Minimum shear ultimate strength of nut
    Returns:
        float: internal thread shear load allowable
    """
    assert A_si > 0.0
    P_si = A_si * F_su_nut
    return P_si


# The two thread shear areas are calculated using the following equations:


def external_thread_shear_area(
        L_e: float,
        K_i_max: float,
        n_0: float,
        TK_i: float,
        TE_e: float,
        G_e: float,
        pitch: float=None,
    ) -> float:
    """Calculate external thread shear area, A_se.
    
    NSTS 08307 Rev A, pg A-5
    
    The equations for the tensile stress area and the thread shear areas were taken from FED-STD-H28, Screw Thread Standards for Federal Services, issued by the United States Department of Commerce, National Bureau of Standards.
    
    To convert thread pitch to threads per inch (TPI), divide 25.4 (millimeters per inch) by the thread pitch in millimeters.
    
    Args:
        L_e: Length of thread engagement
        K_i_max: maximum minor diameter of internal threads
        n_0: threads per inch (tpi)
        TK_i: Tolerance on minor diameter of internal threads
        TE_e: Tolerance on pitch diameter of external threads
        G_e: Allowance on external threads
        pitch: thread pitch, mm
    Returns:
        float: external thread shear area
    """
    if n_0 is None:
        assert pitch is not None
        n_0 = 25.4 / pitch 
    assert L_e > 0.0
    assert K_i_max > 0.0
    A_se = np.pi * L_e * K_i_max * (0.750 - 0.57735 * n_0 * (TK_i + TE_e + G_e))
    return A_se


def internal_thread_shear_area(
        L_e: float,
        D_e_min: float,
        n_0: float,
        TD_e: float,
        TE_i: float,
        G_e: float,
        pitch: float=None,
    ) -> float:
    """Calculate internal thread shear area, A_si.
    
    NSTS 08307 Rev A, pg A-5
    
    The equations for the tensile stress area and the thread shear areas were taken from FED-STD-H28, Screw Thread Standards for Federal Services, issued by the United States Department of Commerce, National Bureau of Standards.
    
    To convert thread pitch to threads per inch (TPI), divide 25.4 (millimeters per inch) by the thread pitch in millimeters.
    
    Args:
        L_e: Length of thread engagement
        D_e_min: minimum major diameter of external threads
        n_0: threads per inch (tpi)
        TD_e: Tolerance on major diameter of external threads
        TE_i: Tolerance on pitch diameter of internal threads
        G_e: Allowance on external threads
        pitch: thread pitch, mm
    Returns:
        float: internal thread shear area
    """
    if n_0 is None:
        assert pitch is not None
        n_0 = 25.4 / pitch 
    assert L_e > 0.0
    assert D_e_min > 0.0
    A_si = np.pi * L_e * D_e_min * (0.875 - 0.57735 * n_0 * (TD_e + TE_i + G_e))
    return A_si


def main() -> None:
    from thread_fast.threads.iso_68_1998 import eq_H
    from thread_fast.threads.iso_724_1993 import eq_d_1
    
    # conversion factors:
    deg_to_rad = np.pi / 180.0
    psi_to_MPa = 0.00689476
    
    # [mm/thread], screw pitch: for M5 coarse thread
    pitch = 0.8
    print(f"pitch = {pitch} [mm/thread]")
    
    # To convert thread pitch to threads per inch (TPI), divide 25.4 (millimeters per inch) by the thread pitch in millimeters.
    
    # threads/inch:
    n_0 = 25.4 / pitch
    print(f"n_0 = {n_0} [thread/in]")
    
    # bolt strength factor of safety:
    SF = 1.2
    
    # joint separation factor of safety:
    SF_sep = 1.15
    
    # External axial load applied to joint at bolt location due to application of limit load to the structure:
    P = 100.0
    
    # Bolt shear load resulting from limit load:
    V = 20.0
    
    # Bolt bending moment resulting from limit load:
    M = 5.0
    
    
    # Geometry:
    
    # height of fundamental triangle:
    H = eq_H(pitch)
    print(f"H = {H} [mm]")
    
    # Basic major diameter of external threads (bolt):
    D = 5.0
    
    # [mm], fastener major (outer) diameter:
    D_major = 4.976
    
    # [mm], fastener minor diameter (basic):
    D_minor = 4.134
    print(f"D_minor = {D_minor}")
    D_minor = eq_d_1(d=D, H=None, P=pitch)
    print(f"D_minor = {D_minor}")
    D_minor = eq_d_1(d=D, H=H)
    print(f"D_minor = {D_minor}")
    D_minor = D - (5.0/4.0)*H
    print(f"D_minor = {D_minor}")
    
    # Major diameter of external threads (basic (nominal) dimension):
    D_e_bsc = D_major
    
    # preload uncertainty due to installation method:
    gamma = 0.25
    
    # assumed preload relaxation:
    relaxation_ratio = 0.05
    
    
    # length of thread engagement:
    L_e = 5.0
    
    # [mm], mean thread (pitch?) diameter:
    # Basic pitch diameter of external threads (bolt)
    E = (D_major + D_minor) / 2.0
    print(f"E = {E} [mm]")
    
    # pitch diameter in inches:
    E_in = E / 25.4
    
    # [mm], mean radius of the screw thread:
    r_m = E / 2.0
    print(f"r_m = {r_m} [mm]")
    
    
    # [rad], thread lead angle:
    psi = np.arctan(pitch / (2.0 * np.pi * r_m))
    print(f"psi = {psi} [rad]")
    print(f"psi = {psi / deg_to_rad} [deg]")
    alpha = np.arctan(1.0 / (n_0 * np.pi * E_in))
    print(f"alpha = {alpha} [rad]")
    print(f"alpha = {alpha / deg_to_rad} [deg]")
    
    # [rad], thread half angle:
    beta = 30.0 * deg_to_rad
    print(f"beta = {beta} [rad]")
    
    # Effective radius of torqued element-to-joint bearing forces = 1/2 x (Ro + Ri)
    R_e = 0.5 * (D / 2.0 + 8.5 / 2.0)
    print(f"R_e = {R_e} [mm]")
    
    # Allowance on external threads:
    G_e = 0.01
    
    # Tolerance on pitch diameter of internal threads:
    TE_i = 0.001
    
    # Tolerance on pitch diameter of external threads:
    TE_e = 0.001
    
    # Tolerance on minor diameter of internal threads:
    TK_i = 0.001
    
    # Tolerance on major diameter of external threads:
    TD_e = 0.001
    
    
    # Material Properties:
    
    # Minimum tensile yield strength of bolt:
    F_ty = 30.0e3
    
    # Minimum tensile ultimate strength of bolt:
    F_tu = 40.0e3
    
    # Minimum shear ultimate strength of bolt:
    F_su_bolt=20.e3
    
    # Minimum shear ultimate strength of nut:
    F_su_nut=20.0e3
    
    # Shear load allowable of bolt:
    VA = 1.0
    
    # Bending load allowable of bolt:
    MA = 1.0
    
    # load introduction factor:
    n = 0.5
    
    # stiffness factor:
    phi = 0.75
    phi = k_b / (k_b + k_j)
    
    
    # Preload Plan:
    
    # applied torque:
    T_max = 12.0
    T_min = 8.0
    
    
    # Nut Factor:
    
    K = nut_factor(
        R_t=r_m, 
        R_e=R_e, 
        mu_t_min=0.1,
        mu_t_typ=0.15, 
        mu_t_max=0.2,
        mu_b_min=0.1,
        mu_b_typ=0.15, 
        mu_b_max=0.2,
        alpha=alpha, 
        beta=beta, 
        D=D,
    )
    print(f"nut factor, K = {K}")
    
    # Tensile Area:
    
    A_t = bolt_tensile_stress_area(
        D_e_bsc=D_e_bsc, 
        n_0=n_0,
        pitch=None,
    )
    print(f"A_t = {A_t} [mm^2]")
    
    A_t = bolt_tensile_stress_area(
        D_e_bsc=D_e_bsc, 
        n_0=None,
        pitch=pitch,
    )
    print(f"A_t = {A_t} [mm^2]")
    
    # Thread Shear Area:
    
    A_se = external_thread_shear_area(
        L_e=L_e,
        K_i_max=4.5,
        n_0=n_0,
        TK_i=TK_i,
        TE_e=TE_e,
        G_e=G_e,
        pitch=None,
    )
    print(f"A_se = {A_se} [mm^2]")
    
    A_se = external_thread_shear_area(
        L_e=L_e,
        K_i_max=4.5,
        n_0=None,
        TK_i=TK_i,
        TE_e=TE_e,
        G_e=G_e,
        pitch=pitch,
    )
    print(f"A_se = {A_se} [mm^2]")
    
    A_si = internal_thread_shear_area(
        L_e=L_e,
        D_e_min=4.7,
        n_0=n_0,
        TD_e=TD_e,
        TE_i=TE_i,
        G_e=G_e,
        pitch=None,
    )
    print(f"A_si = {A_si} [mm^2]")
    
    A_si = internal_thread_shear_area(
        L_e=L_e,
        D_e_min=4.7,
        n_0=None,
        TD_e=TD_e,
        TE_i=TE_i,
        G_e=G_e,
        pitch=pitch,
    )
    print(f"A_si = {A_si} [mm^2]")
    
    
    # Estimated Preload:
    PLD_max = max_preload(
        gamma=gamma, 
        T_max=T_max,
        K_typ=K[1],
        D=D,
        P_thr_pos=0.0,
        K_min=None,
    )
    print(f"PLD_max = {PLD_max} [??]")
    
    PLD_min = min_preload(
        gamma=gamma, 
        T_min=T_min,
        K_typ=K[1],
        T_p=0.5,
        D=D,
        P_thr_neg=0.0,
        relaxation_ratio=0.05,
        P_loss=None,
        K_max=None,
    )
    print(f"PLD_min = {PLD_min} [??]")
    
    
    # Bolt Axial Load: 
    
    P_b_str = bolt_axial_load_for_strength(
        PLD_max=PLD_max, 
        n=n, 
        phi=phi, 
        SF=SF, 
        P=P,
    )
    print(f"P_b_str = {P_b_str} [??]")
    
    P_sep = joint_separation_load(
        P=P, 
        SF_sep=SF_sep,
    )
    
    P_b_sep = bolt_axial_load_for_separation(
        PLD_min=PLD_min,
        n=n,
        phi=phi,
        P_sep=P_sep,
    )
    print(f"P_b_sep = {P_b_sep} [??]")
    
    
    # Allowables:
    
    PA_t = tensile_axial_load_allowable_ultimate(
        A_t=A_t, 
        F_tu=F_tu,
    )
    print(f"PA_t = {PA_t} [??]")
    
    P_se = external_thread_shear_load_allowable(
        A_se=A_se,
        F_su_bolt=F_su_bolt,
    )
    print(f"P_se = {P_se} [N]")
    
    P_si = internal_thread_shear_load_allowable(
        A_si=A_si, 
        F_su_nut=F_su_nut,
    )
    print(f"P_si = {P_si} [N]")
    
    
    # Margins of Safety:
    
    MS_tensile = bolt_tensile_margin(
        PA_t=PA_t, 
        SF=SF, 
        P=P, 
        P_b=P_b_str,
    )
    print(f"MS_tensile = {MS_tensile} [-]")
    
    MS_pull_out_i = thread_shear_pull_out_margin(
        PA_s=P_si, 
        SF=SF, 
        P=P, 
        P_b=P_b_str,
    )
    print(f"MS_pull_out_i = {MS_pull_out_i} [-]")
    
    MS_pull_out_e = thread_shear_pull_out_margin(
        PA_s=P_se, 
        SF=SF, 
        P=P, 
        P_b=P_b_str,
    )
    print(f"MS_pull_out_e = {MS_pull_out_e} [-]")
    
    MS_shear = shear_margin(
        VA=VA, 
        SF=SF, 
        V=V,
    )
    print(f"MS_shear = {MS_shear} [-]")
    
    MS_bend = bending_margin(
        MA=MA, 
        SF=SF, 
        M=M,
    )
    



if __name__ == "__main__":
    main()
    