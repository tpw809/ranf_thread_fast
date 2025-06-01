"""Equations from NASA-STD-5020B

REQUIREMENTS FOR THREADED FASTENING
SYSTEMS IN SPACEFLIGHT HARDWARE

2021
"""
import numpy as np
from typing import List


############################################
# 4.3.1 Maximum and Minimum Preload
############################################


def eq1(
        P_pi_max: float, 
        P_deltat_max: float,
    ) -> float:
    """Calculate maximum predicted preload, P_p_max.
    
    nasa-std-5020b, equation 1, pg 21
    
    Args:
        P_pi_max: maximum initial preload
        P_deltat_max: maximum increase in preload due to temperature
    Returns:
        float: max predicted preload
    """
    assert P_deltat_max >= 0.0
    P_p_max = P_pi_max + P_deltat_max
    return P_p_max


def eq2(
        P_pi_min: float, 
        P_pr: float, 
        P_deltat_min: float,
        P_pc: float=0.0, 
    ) -> float:
    """Calculate minimum predicted preload, P_p_min.
    
    nasa-std-5020b, equation 2, pg 21
    
    Args:
        P_pi_min: minimum initial preload
        P_pr: short term relaxation of preload
        P_deltat_min: maximum decrease in preload due to temperature
        P_pc: loss of preload from material creep
    Returns:
        float: min predicted preload
    """
    assert P_deltat_min >= 0.0
    assert P_pr >= 0.0
    assert P_pc >= 0.0
    P_p_min = P_pi_min - P_pr - P_pc - P_deltat_min
    return P_p_min


def eq3(
        c_max: float, 
        gamma: float, 
        P_pi_nom: float,
    ) -> float:
    """Calculate max initial preload, P_pi_max.
    
    nasa-std-5020b, equation 3, pg 22
    
    Args:
        c_max: factor that accounts for max value of controlled installation parameter, as allowed by specified tolerance
        gamma: preload variation
        P_pi_nom: nominal installation preload
    Returns:
        float: max initial preload
    """
    P_pi_max = c_max * (1.0 + gamma) * P_pi_nom
    return P_pi_max
    

def eq4(
        c_min: float, 
        gamma: float, 
        P_pi_nom: float,
    ) -> float:
    """Calculate min initial preload, P_pi_min.
    
    nasa-std-5020b, equation 4, pg 22
    
    Args:
        c_min: factor that accounts for min value of controlled installation parameter, as allowed by specified tolerance
        gamma: preload variation
        P_pi_nom: nominal installation preload
    Returns:
        float: min initial preload
    """
    P_pi_min = c_min * (1.0 - gamma) * P_pi_nom
    return P_pi_min


def eq5(c_min: float, 
        gamma: float, 
        P_pi_nom: float,
        n_f: int,
    ) -> float:
    """Calculate min initial preload, P_pi_min.
    
    nasa-std-5020b, equation 5, pg 23
    
    For use in joint slip and non-separation critical joint separation analysis.
    
    Args:
        c_min: factor that accounts for min value of controlled installation parameter, as allowed by specified tolerance
        gamma: preload variation
        P_pi_nom: nominal installation preload
        n_f: number of fastener in the joint.
    Returns:
        float: min initial preload
    """
    P_pi_min = c_min * (1.0 - gamma / np.sqrt(n_f)) * P_pi_nom
    return P_pi_min



############################################
# 4.4.1 Ultimate Design Loads
############################################


def eq6(
        P_tu_allow: float, 
        FS_u: float, 
        P_tL: float,
        FF: float=1.15,
    ) -> float:
    """Calculate margin of safety for ultimate load, MS_u.
    
    nasa-std-5020b, equation 6, pg 27
    
    For when separation occurs before rupture.
    
    Args:
        P_tu_allow: allowable ultimate load
        FS_u: ultimate factor of safety
        P_tL: limit tensile load
        FF: fitting factor
    Returns:
        float: margin of safety for ultimate tensile load
    """
    assert FF >= 1.0
    assert FS_u >= 1.0
    MS_u = P_tu_allow / (FF * FS_u * P_tL) - 1.0
    return MS_u
    

def eq7(
        P_prime_tu: float, 
        FS_u: float, 
        P_tL: float,
        FF: float=1.15,
    ) -> float:
    """Calculate margin of safety for ultimate load, MS_u.
    
    nasa-std-5020b, equation 7, pg 27
    
    For when rupture occurs before separation.
    
    Args:
        P_prime_tu: applied tensile load that causes the fastener load to exceed the allowable ultimate tensile load
        FS_u: ultimate factor of safety
        P_tL: limit tensile load
        FF: fitting factor
    Returns:
        float: margin of safety for ultimate tensile load
    """
    assert FF >= 1.0
    assert FS_u >= 1.0
    MS_u = P_prime_tu / (FF * FS_u * P_tL) - 1.0
    return MS_u


def eq6or7() -> float:
    """
    select between eq6 and eq 7
    
    For when separation occurs before rupture = eq6.
    
    For when rupture occurs before separation = eq7.
    """
    #TODO: evaluate separation and rupture, then choose ultimate margin of safety
    return MS_u


def eq8(
        P_p: float, 
        n: float, 
        phi: float, 
        P_t: float,
    ) -> float:
    """Calculate the tensile load in a preloaded bolt, P_tb.
    
    nasa-std-5020b, equation 8, pg 28
    
    Args:
        P_p: preload
        n: load introduction factor
        phi: stiffness factor
        P_t: applied tensile load
    Returns:
        float: tensile load in the bolt
    """
    assert 0.0 <= n <= 1.0
    P_tb = P_p + n * phi * P_t
    return P_tb


def eq9(k_b: float, k_c: float) -> float:
    """Calculate the stiffness factor, phi.
    
    nasa-std-5020b, equation 9, pg 28
    
    Args:
        k_b: stiffness of the bolt
        k_c: stiffness of the clamped parts
    Returns:
        float: stiffness factor
    """
    assert k_b > 0.0, "k_b must be > 0.0"
    assert k_c > 0.0, "k_c must be > 0.0"
    phi = k_b / (k_b + k_c)
    return phi


def eq10(
        n: float, 
        phi: float, 
        P_tu_allow: float, 
        P_p_max: float,
    ) -> float:
    """Calculate applied tensile load that causes the bolt load to exceed the allowable ultimate tensile load for the fastening system, P_prime_tu.
    
    nasa-std-5020b, equation 10, pg 28
    
    Args:
        n: load introduction factor
        phi: stiffness factor
        P_tu_allow: allowable ultimate load
        P_p_max: maximum preload
    Returns:
        float: applied tensile load that causes the bolt load to exceed the allowable ultimate tensile load
    """
    assert 0.0 <= n <= 1.0
    P_prime_tu = 1.0 / (n * phi) * (P_tu_allow - P_p_max)
    return P_prime_tu


def eq11(P_p_max: float, n: float, phi: float) -> float:
    """Calculate the linearly projected load that causes separation when at maximum preload, P_prime_sep.
    
    nasa-std-5020b, equation 11, pg 28
    
    Args:
        P_p_max: maximum preload
        n: load introduction factor
        phi: stiffness factor
    Returns:
        float: linearly projected load that causes separation when at maximum preload
    """
    assert 0.0 <= n <= 1.0
    P_prime_sep = P_p_max / (1.0 - n * phi)
    return P_prime_sep


def eq12(D: float, F_su: float) -> float:
    """Calculate allowable ultimate shear load for a fastener, P_su_allow.
    
    nasa-std-5020b, equation 12, pg 28
    
    For threads not in the shear plane.
    
    Args:
        D: nominal diameter
        F_su: allowable ultimate shear strength for the fastener material
    Returns:
        float: allowable ultimate shear load for a fastener
    """
    P_su_allow = np.pi * D**2 * F_su / 4.0
    return P_su_allow


def eq13(F_su: float, A_m: float) -> float:
    """Calculate allowable ultimate shear load for a fastener, P_su_allow.
    
    nasa-std-5020b, equation 13, pg 28
    
    For threads in the shear plane.
    
    Args:
        F_su: allowable ultimate shear strength for the fastener material
        A_m: minimum minor diameter area for the fastener threads
    Returns:
        float: allowable ultimate shear load for a fastener
    """
    P_su_allow = F_su * A_m
    return P_su_allow


def eq14(
        P_su_allow: float, 
        FS_u: float, 
        P_sL: float, 
        FF: float=1.15,
    ) -> float:
    """Calculate ultimate margin of safety for shear loading of a fastener, MS_u.
    
    nasa-std-5020b, equation 14, pg 29
    
    Args:
        P_su_allow: allowable ultimate shear load for a fastener
        FS_u: ultimate factor of safety
        P_sL: limit shear load acting on the shear plane
        FF: fitting factor
    Returns:
        float: ultimate margin of safety for shear loading of a fastener
    """
    assert FS_u >= 1.0, "error, safety factor, FS_u, must be >= 1.0"
    assert FF >= 1.0, "error, fitting factor, FF, must be >= 1.0"
    if P_sL == 0.0:
        return np.inf
    MS_u = P_su_allow / (FF * FS_u * P_sL) - 1.0
    return MS_u


############################################
# 4.4.2 Yield Design Loads
############################################


def eq15(
        P_ty_allow: float, 
        FS_y: float, 
        P_tL: float, 
        FF: float=1.15,
    ) -> float:
    """nasa-std-5020b, equation 15, pg 30
    
    Calculate margin of safety for yield under axial load, MS_y.
    
    For when separation occurs before yield.
    
    Args:
        P_ty_allow: allowable tensile load of the material
        FS_y:
        P_tL:
        FF: fitting factor
    """
    assert FS_y >= 1.0, "error, safety factor, FS_y, must be >= 1.0"
    assert FF >= 1.0, "error, fitting factor, FF, must be >= 1.0"
    if P_tL == 0.0:
        return np.inf
    MS_y = P_ty_allow / (FF * FS_y * P_tL) - 1.0
    return MS_y


def eq16(
        P_prime_ty: float, 
        FS_y: float, 
        P_tL: float, 
        FF: float=1.15, 
    ) -> float:
    """nasa-std-5020b, equation 16, pg 30
    
    Args:
        P_prime_ty: applied tensile load that causes the fastener load to exceed the fastening system’s allowable yield tensile load
        FS_y:
        P_tL: limit tensile load
        FF: fitting factor
    """
    assert FS_y >= 1.0, "error, safety factor, FS_y, must be >= 1.0"
    assert FF >= 1.0, "error, fitting factor, FF, must be >= 1.0"
    if P_tL == 0.0:
        return np.inf
    MS_y = P_prime_ty / (FF * FS_y * P_tL) - 1.0
    return MS_y


def eq17(
        n: float, 
        phi: float, 
        P_ty_allow: float, 
        P_p_max: float,
    ) -> float:
    """nasa-std-5020b, equation 17, pg 30
    
    Calculate applied tensile load that causes the fastener load to exceed the fastening system’s allowable yield tensile load if yielding occurs before separation, P_prime_ty.
    
    Args:
        n: load introduction factor
        phi: stiffness factor
        P_ty_allow: allowable tensile load of the material
        P_p_max: maximum initial preload
    """
    assert 0.0 <= n <= 1.0
    P_prime_ty = (1.0 / (n * phi)) * (P_ty_allow - P_p_max)
    return P_prime_ty


def eq18(
        F_ty: float, 
        F_tu: float, 
        P_tu_allow: float,
    ) -> float:
    """Estimate allowable yield tensile load, when value is not available.
    
    nasa-std-5020b, equation 18, pg 30
    
    Args:
        F_ty: yield strength
        F_tu: ultimate strength
        P_tu_allow: allowable ultimate load of the fastener in tension
    Returns:
        float: allowable yield tensile load
    """
    P_ty_allow = (F_ty / F_tu) * P_tu_allow
    return P_ty_allow
    

############################################
# 4.4.3 Separation Loads, pg 31
############################################


def eq19(
        P_p_min: float, 
        SF_sep: float, 
        P_tL: float,
        FF: float=1.15, 
    ) -> float:
    """Calculate margin of safety for separation, MS_sep.
    
    nasa-std-5020b, equation 19, pg 32
    
    Axial loading only.
    
    Args:
        P_p_min:
        SF_sep: separation factor of safety
        P_tL: 
        FF: fitting factor
    Returns:
        float: margin of safety for separation
    """
    assert FF >= 1.0, "error, fitting factor, FF, must be >= 1.0"
    MS_sep = P_p_min / (FF * FS_sep * P_tL) - 1.0
    return MS_sep


############################################
# 4.4.4 Combination of Loads, pg 32
############################################

# How do I use these inequalities in eq20 to eq23?
# compare to NASA-TM-106943 pg 17
# not sure why TM-106943 puts eval under sqrt...
# look in NASA/TM-2012-217454: doesn't really help, just shows data and same (almost) updated criteria equations

# how about: MS = 1.0 / eval - 1.0
# or MS = 1.0 - eval


def eq20mod(
        P_su: float, 
        P_su_allow: float, 
        P_tu: float, 
        P_tu_allow: float,
        f_bu: float,
        F_tu: float,
    ) -> float:
    """Calculate ultimate margin of safety for combined loading, MS_comb.
    
    nasa-std-5020b, modified equation 20, pg 33
    
    For when the full diameter body is in the shear plane.
    
    For when not accounting for plastic bending.
    
    Args:
        P_su:
        P_su_allow:
        P_tu:
        P_tu_allow:
        f_bu:
        F_tu: 
    Returns:
        float: ultimate margin of safety for combined loading
    """
    eq20 = (P_su / P_su_allow)**2.5 + (P_tu / P_tu_allow + f_bu / F_tu)**1.5
    MS_comb = 1.0 / eq20 - 1.0
    return MS_comb


def eq21mod(
        P_su: float, 
        P_su_allow: float, 
        P_tu: float, 
        P_tu_allow: float,
        f_bu: float,
        F_bu: float,
    ) -> float:
    """Calculate ultimate margin of safety for combined loading, MS_comb.
    
    nasa-std-5020b, modified equation 21, pg 33
    
    For when the full diameter body is in the shear plane.
    
    For when accounting for plastic bending.
    
    Args:
        P_su:
        P_su_allow:
        P_tu:
        P_tu_allow:
        f_bu:
        F_bu:
    Returns:
        float: ultimate margin of safety for combined loading
    """
    eq21 = (P_su / P_su_allow)**2.5 + (P_tu / P_tu_allow)**1.5 + f_bu / F_bu
    MS_comb = 1.0 / eq21 - 1.0
    return MS_comb


def eq22mod(
        P_su: float, 
        P_su_allow: float, 
        P_tu: float, 
        P_tu_allow: float,
        f_bu: float,
        F_tu: float,
    ) -> float:
    """Calculate ultimate margin of safety for combined loading, MS_comb.
    
    nasa-std-5020b, modified equation 22, pg 33
    
    For when the full diameter body is in the shear plane.
    
    For when not accounting for plastic bending.
    
    Args:
        P_su:
        P_su_allow:
        P_tu:
        P_tu_allow:
        f_bu:
        F_tu:
    """
    eq22 = (P_su / P_su_allow)**1.2 + (P_tu / P_tu_allow + f_bu / F_tu)**2
    MS_comb = 1.0 / eq22 - 1.0
    return MS_comb


def eq23mod(
        P_su: float, 
        P_su_allow: float, 
        P_tu: float, 
        P_tu_allow: float,
        f_bu: float,
        F_bu: float,
    ) -> float:
    """Calculate ultimate margin of safety for combined loading, MS_comb.
    
    nasa-std-5020b, modified equation 23, pg 34
    
    For when the full diameter body is in the shear plane.
    
    For when accounting for plastic bending.
    
    Args:
    
    
    """
    eq23 = (P_su / P_su_allow)**1.2 + (P_tu / P_tu_allow)**2 + f_bu / F_bu
    MS_comb = 1.0 / eq23 - 1.0
    return MS_comb


############################################
# A.2 Accounting for Preload Variation, pg 46
############################################


def eq24(T: float, K_nom: float, D: float) -> float:
    """Calculate initial nominal preload, P_pi_nom.
    
    nasa-std-5020b, equation 24, pg 46
    
    Args:
        T: nominal effective torque
        K_nom: nominal nut factor
        D: nominal bolt diameter
    Returns:
        float: initial nominal preload
    """
    assert D > 0.0
    assert K_nom > 0.0
    P_pi_nom = T / (K_nom * D)
    return P_pi_nom


def eq25(
        gamma: float, 
        T_max: float, 
        K_nom: float,
        D: float,
    ) -> float:
    """Calculate maximum initial preload, P_pi_max.
    
    nasa-std-5020b, equation 25, pg 46
    
    Args:
        gamma: preload variation
        T_max: maximum effective torque
        K_nom: nominal nut factor
        D: nominal bolt diameter
    Returns:
        float: max initial preload
    """
    assert gamma >= 0.0
    assert D > 0.0
    assert K_nom > 0.0
    P_pi_max = (1.0 + gamma) * T_max / (K_nom * D)
    return P_pi_max


def eq26a(
        gamma: float, 
        T_min: float, 
        K_nom: float,
        D: float,
    ) -> float:
    """Calculate minimum initial preload, P_pi_min.
    
    nasa-std-5020b, equation 26a, pg 46
    
    For use in separation analysis of separation-critical joints.
    
    Args:
        gamma: preload variation
        T_min: minimum effective torque
        K_nom: nominal nut factor
        D: nominal bolt diameter
    Returns:
        float: min initial preload
    """
    assert gamma >= 0.0
    assert D > 0.0
    assert K_nom > 0.0
    P_pi_min = (1.0 - gamma) * T_min / (K_nom * D)
    return P_pi_min


def eq26b(
        gamma: float, 
        n_f: int, 
        T_min: float, 
        K_nom: float,
        D: float,
    ) -> float:
    """Calculate minimum initial preload, P_pi_min.
    
    nasa-std-5020b, equation 26b, pg 47
    
    For use in separation analysis of joints that are not separation-critical and joint-slip analysis.
    
    Args:
        gamma: preload variation
        n_f: number of fasteners in the joint
        T_min: minimum effective torque
        K_nom: nominal nut factor
        D: nominal bolt diameter
    Returns:
        float: min initial preload
    """
    assert gamma >= 0.0
    assert D > 0.0
    assert K_nom > 0.0
    P_pi_min = (1.0 - gamma / np.sqrt(n_f)) * T_min / (K_nom * D)
    return P_pi_min


# eq27: T_max = T_s_max
# eq28: T_min = T_s_min
# eq29: T_max = T_s_max - T_br_min
# eq30: T_min = T_s_min - T_L_max

# eq31: P_pi_nom = 1/m *sum(P_pi_j)


def eq32(
        T: float, 
        D: float, 
        P_pi_nom: float,
    ) -> float: 
    """Calculate nominal nut factor, K_nom
    
    nasa-std-5020b, equation 32, pg 48
    
    Args:
        T:
        D: nominal bolt diameter
        P_pi_nom:
    Returns:
        float: nominal nut factor
    """
    assert D > 0.0
    assert P_pi_nom > 0.0
    K_nom = T / (D * P_pi_nom)
    return K_nom
    

############################################
# A.4 Load Introduction and Stiffness Factor, pg 51
############################################


def eq37(L_lp: float, L: float) -> float:
    """Calculate geometric load introduction factor, n.
    
    nasa-std-5020b, equation 37, pg 52
    
    See: The Mechanism of Bolt Loading, NASA-TM-108377
    
    Args:
        L_lp: length between loading planes
        L: total thickness of the joint
    Returns:
        float: geometric load introduction factor
    """
    assert L_lp >= 0.0, "error, L_lp must be >= 0.0"
    assert L > 0.0, "error, L must be > 0.0"
    n = L_lp / L
    assert n >= 0.0, "error, n must be >= 0"
    assert n <= 1.0, "error, n must be <= 1"
    return n



############################################
# A.4.1 Stiffness Based Load Introduction Factor, pg 53
############################################


def eq38() -> float:
    """nasa-std-5020b, equation 38, pg 
    
    See: The Mechanism of Bolt Loading, NASA-TM-108377
    
    """
    k = 0.0
    return k


# eq39:
# eq40:
# eq41:
# eq42:
# eq43:
# eq44: delta = P_t / K_eff
# eq45: delta = (P_tb - P_p) / K_12_45
# eq46: 


def eq47(
        P_p: float, 
        n: float, 
        phi: float, 
        P_t: float,
    ) -> float:
    """Calculate tensile load in a preloaded bolt, P_tb.
    
    nasa-std-5020b, equation 47, pg 56
    
    See: The Mechanism of Bolt Loading, NASA-TM-108377
    
    Args:
        P_p: preload
        n: load introduction factor
        phi: stiffness factor
        P_t: external applied tensile load
    Returns:
        float: tensile load in preloaded bolt
    """
    P_tb = P_p + n * phi * P_t
    return P_tb


def eq48(B: float, C: float) -> float:
    """Calculate stiffness based load introduction factor, n.
    
    nasa-std-5020b, equation 48, pg 56
    
    Expressed in terms of the clamped members being relieved.
    
    See: The Mechanism of Bolt Loading, NASA-TM-108377
    
    Args:
        B: stiffness coefficient
        C: stiffness coefficient
    Returns:
        float: stiffness based load introduction factor
    """
    n = (B + C) / (B * C)
    return n


# eq49: same as eq9
# eq50: intermediate
# eq51: intermediate


def eq52(A: float, D: float) -> float:
    """Calculate stiffness based load introduction factor, n.
    
    nasa-std-5020b, equation 52, pg 56
    
    Expressed in terms of the clamped members being compressed.
    
    See: The Mechanism of Bolt Loading, NASA-TM-108377
    
    Args:
        A: stiffness coefficient
        D: stiffness coefficient
    Returns:
        float: stiffness based load introduction factor
    """
    n = 1.0 - (A + D) / (A * D)
    return n


############################################
# A.4.2Limitation of the Geometry Based Load Introduction Factor, pg 57
############################################

# eq53: 1 / K_23_34 = n / k_c
# eq54:
# eq55:
# eq56:


def eq57(l4: float, l2: float, L: float) -> float:
    """Calculate geometric load introduction factor, n_G.
    
    nasa-std-5020b, equation 57, pg 57
    
    See: 
    -NSTS 08307
    -The Mechanism of Bolt Loading, NASA-TM-108377
    
    Args:
        l4: length to second loading plane
        l2: length to first loading plane
        L: total thickness of the joint
    Returns:
        float: geometric load introduction factor
    """
    assert l4 >= l2, "error: l4 must be >= l2"
    n_G = (l4 - l2) / L
    assert n_G >= 0.0, "error, nu must be >= 0"
    assert n_G <= 1.0, "error, nu must be <= 1"
    return n_G


############################################
# A.8 Theoretical Treatment of Interaction Equations, pg 66
# supplement to section 4.4.4
############################################

# eq60:
# eq61:
# eq62:
# eq63:
# eq64:
# eq65:
# eq66:
# eq67:
# eq68:
# eq69:
# eq70:
# eq71:
# eq72:
# eq73:
# eq74:
# eq75:
# eq76:
# eq77:
# eq78:
# eq79:
# eq80:

    
############################################
# A.10 Margin of safety for joint slip, pg 73
# supplement to sections 4.4.1 and 4.4.6
############################################


# eq81: P_f = mu * (n_f * P_p_nom - P_t_joint)
# eq82: mu*(n_f*P_p_min - a*FS*P_tL_joint) / (a*FS*P_sL_joint) - 1.0
# eq83: a = mu*n_f*P_p_min / (FS*(P_sl_joint + mu*P_tL_joint))
# eq84:
# eq85:
# eq86: MS_slip = mu*P_p_min / (FF*FS*(P_sL + mu*P_tL)) - 1.0


############################################
# Appendix C Justification for Fatigue Failure, pg 97
############################################


def eq87(n_i: list[float], N_i: list[float]) -> float:
    """Calculate cumulative damage according to Miner's rule.
    
    nasa-std-5020b, equation 87, pg 99
    
    D must be <= 1.0 to predict survival.
    
    Args:
        n_i: number of loading cycles at a given stress level
        N_i: the number of cycles to failure at that stress level
    Returns:
        float: cumulative damage
    """
    D = np.sum((n_i / N_i))
    return D


def main() -> None:
    # Tests:
    
    # bolt stiffness:
    k_b = 1.0
    
    # clamped parts stiffness:
    k_c = 1.0
    
    # stiffness factor:
    phi = eq9(
        k_b=k_b, 
        k_c=k_c,
    )
    print(f"stiffness factor, phi = {phi}")
    
    # length to second loading plane:
    l4 = 1.25
    
    # length to first loading plane:
    l2 = 0.75
    
    # total length of clamped parts:
    L = 2.0
    
    # geometric load introduction factor:
    n_G = eq57(
        l4=l4, 
        l2=l2, 
        L=L,
    )
    print(f"geometric load introduction factor, n_G = {n_G}")


if __name__ == "__main__":
    main()
    