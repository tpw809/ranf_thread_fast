"""Equations from NASA-TM-106943

Preloaded Joint Analysis Methodology for Space Flight Systems

Jeffrey A. Chambers

References:
1. Criteria for Preloaded Bolts. NSTS-08307, 1989.
2. Barrett, R.T.: Fastener Design Manual. NASA RP-1228, 1990.
3. Wood, C.M.: Standard Threaded Fasteners, Torque Limits For. MSFC-STD-486B, Nov. 1992.
4. Shigley, J.E.; and Mischke, C.R.: Fastening, Joining, and Connecting, A Mechanical Designers' Workbook.
McGraw-Hill Publishing Co., New York, 1990.
5. Payload Flight Equipment Requirements for Safety-Critical Structures. JA-418, Rev. A, 1989.
6. Shigley, J.E.; and Mitchell, L.D.: Mechanical Engineering Design, Fourth Ed., McGraw-Hill Publishing Co., New
York, 1983.
7. Bruhn, E.E: Analysis and Design of Flight Vehicle Structures. Jacobs Publishing, Co., Carmel, Indiana, 1973.
8. Federal Standard: Screw-Thread Standards For Federal Service. FED-STD-H28, 1978.
9. Metallic Materials and Elements for Aerospace Vehicle Structures. MIL-HDBK-5E 1990.
10. Astronautic Structures Manual. NASA TM X-73305, vol. I, 1975.
11. Nut, Self Locking, 250 °E 450 °F, and 800 °E MIL-N-25027E 1994.
"""
import numpy as np


########################################################
# A286 Alloy Fastener Properties: pg 7
########################################################

# [ksi], material ultimate tensile strength:
F_tu = 130.0

# [ksi], material tensile yield strength:
F_ty = 85.0

# [ksi], material ultimate shear strength:
F_su = 85.0

# [ksi], shear yield strength: 
# may be assumed to be 0.577 * F_ty
F_sy = 0.577 * F_ty

# bearing strength?
# F_b = 1.5 * ???

########################################################
# Determining Bolt Preload: pg 3
########################################################


def eq1(
        T: float, 
        K: float, 
        D: float, 
        u: float,
    ) -> float:
    """NASA-TM-106943, equation 1, pg 4
    
    P_0 = nominal bolt preload
    
    Args:
        T = applied torque
        D = nominal diameter
        K = nut factor, factor applied to account for the effects of friction in the torquing elements (both in the threads and under the bolt head/nut)
        u = preload uncertainty factor
    Returns:
        nominal bolt preload
    """
    P_0_max = T / (K * D) * (1.0 + u)
    P_0_min = T / (K * D) * (1.0 - u)
    return P_0_min, P_0_max


def eq2(
        D_p: float, 
        D: float, 
        psi: float, 
        alpha: float, 
        mu: float, 
        mu_c: float,
    ) -> float:
    """NASA-TM-106943, equation 2, pg 4
    
    K = nut factor
    
    sec = 1/cos
    
    Args:
        D_p: mean thread diameter
        D: nominal fastener shank diameter
        psi: thread helix (lead) angle, rad 
        alpha: thread angle, rad
        mu: coefficient of friction between threads
        mu_c: coefficient of friction between bolt head or nut and abutment
    Returns:
        float: estimated nut factor
    """
    # K = D_p / (2.0 * D) * ((np.tan(psi) + mu * np.sec(alpha)) / (1.0 - mu * np.tan(psi) * np.sec(alpha))) + 0.625 * mu_c
    K = D_p / (2.0 * D) * ((np.tan(psi) + mu / np.cos(alpha)) / (1.0 - mu * np.tan(psi) / np.cos(alpha))) + 0.625 * mu_c
    return K


# NASA-TM-106943, equation 3, pg 4
# assume 65% of tensile yield = preload_stress_ratio
# T_KD = T / (K * D)
# T_KD = 0.65 * F_ty * A_t
# T = preload_stress_ratio * F_ty * A_t * K * D
# A_t = tensile area
# F_ty = tensile yeild strength
# K = nut factor
# D = nominal bolt diameter


def eq4(D: float, p: float) -> float:
    """NASA-TM-106943, equation 4:, pg 5
    
    A_t =  tensile area (min cross section area of bolt)
    
    Args:
        D: nominal diameter
        p: thread pitch
    Returns:
        float: tensile area (min cross section area of bolt)
    """
    A_t = (np.pi / 4.0) * (D - 0.9743*p)**2
    return A_t


# NASA-TM-106943, equation 5, pg 5
# more specific equation 3:
# T_KD = 0.65 * 85000 * A_t 
# T_KD = 55250 * A_t


def eq6(
        P_th: float, 
        K_b: float, 
        alpha_b: float, 
        L: float, 
        delta_T: float,
    ) -> float:
    """NASA-TM-106943, equation 6, pg 5
    
    delta_b = bolt deflection due to temperature change
    
    Args:
        alpha_b: bolt coefficient of thermal expansion
        K_b: bolt stiffness
        P_th: axial bolt load due to thermal effects
        L: fastener grip length
        delta_T: change in temperature
    Returns:
        float: bolt deflection due to temperature change
    """
    delta_b = P_th / K_b + alpha_b * L * delta_T
    return delta_b


def eq7(
        P_th: float, 
        K_j: float, 
        alpha_j: float, 
        L: float, 
        delta_T: float,
    ) -> float:
    """NASA-TM-106943, equation 7, pg 5
    
    delta_j = abutment deflection due to temperature change.
    
    Args:
        alpha_j: joint abutment coefficient of thermal expansion
        K_j: joint stiffness
        P_th: axial bolt load due to thermal effects
        L: fastener grip length
        delta_T: change in temperature
    Returns:
        float: abutment deflection due to temperature change
    """
    delta_j = P_th / K_j + alpha_j * L * delta_T
    return delta_j


# NASA-TM-106943, equation 8, pg 5
# intermediate algebra to get to 10

# NASA-TM-106943, equation 9, pg 5
# intermediate algebra to get to 10


def eq10(
        K_b: float, 
        K_j: float, 
        L: float, 
        delta_T: float, 
        alpha_j: float, 
        alpha_b: float,
    ) -> float:
    """NASA-TM-106943, equation 10, pg 5
    
    Args:
        K_b: bolt stiffness
        K_j: joint stiffness
        L: fastener grip length
        delta_T: change in temperature
        alpha_b: bolt coefficient of thermal expansion
        alpha_j: joint abutment coefficient of thermal expansion
    Returns:
        float: change in preload due to thermal effects
    """
    P_th = ((K_b * K_j) / (K_b + K_j)) * L * delta_T * (alpha_j - alpha_b)
    return P_th


def eq11(
        P_0_min: float, 
        relaxation_ratio: float=0.05,
    ) -> float:
    """NASA-TM-106943, equation 11, pg 6
    
    Calculate preload loss due to embedment relaxation.
    
    Args:
        P_0_min: minimum expected bolt preload
        relaxation_ratio: expected percentage preload loss
    Returns:
        float: preload loss due to embedment relaxation
    """
    P_relax = relaxation_ratio * P_0_min
    return P_relax


def eq12(
        T: float, 
        K: float, 
        D: float, 
        u: float, 
        P_th: float,
    ) -> float:
    """NASA-TM-106943, equation 12, pg 6
    
    Calculate max expected preload in the joint.
    
    Args:
        T: applied torque
        D: nominal diameter
        K: nut factor
        u: preload uncertainty factor
        P_th: axial bolt load due to thermal effects
    Returns:
        float: max expected preload in the joint
    """
    P_0_max = T/(K*D) * (1.0 + u) + P_th
    return P_0_max


def eq13(T, D, K, u, P_th, P_relax) -> float:
    """NASA-TM-106943, equation 13, pg 7
    
    P_o_min = min expected preload in the joint
    
    Args:
        T: applied torque
        D: nominal diameter
        K: nut factor
        u: preload uncertainty factor
        P_th: axial bolt load due to thermal effects
    Returns:
        float: min expected preload in the joint
    """
    P_0_min = T / (K*D) * (1.0 - u) - P_th - P_relax
    return P_0_min


def eq14(T: float, K: float, D: float) -> float:
    """NASA-TM-106943, equation 14, pg 7
    
    simplified equation 12, manually torqued, no thermal:
    
    Args:
        T: applied torque
        D: nominal diameter
        K: nut factor
    Returns:
        float: max expected preload in the joint
    """
    P_0_max = T/(K*D) * 1.25
    return P_0_max


def eq15(T: float, K: float, D: float) -> float:
    """NASA-TM-106943, equation 15, pg 7
    
    simplified equation 13, manually torqued, no thermal
    
    assumed relaxation percentage
    
    Args:
        T: applied torque
        D: nominal diameter
        K: nut factor
    Returns:
        float: min expected preload in the joint
    """
    P_0_min = T/(K*D) * 0.75 - 0.05 * P_0_min
    return P_0_min


def eq16(T: float, K: float, D: float) -> float:
    """NASA-TM-106943, equation 16, pg 7
    
    simplified equation 15
    
    assumed relaxation percentage
    
    Args:
        T: applied torque
        D: nominal diameter
        K: nut factor
    Returns:
        float: min expected preload in the joint
    """
    P_0_min = T/(K*D) * 0.714
    return P_0_min


########################################################
# Fastener Axial Load: pg 8
########################################################


def eq17(
        P_0_max: float, 
        SF: float, 
        n: float, 
        phi: float, 
        P_et: float,
    ) -> float:
    """NASA-TM-106943, equation 17, pg 8
    
    Calculate total axial load in the fastener.
    
    Safety factor is not applied to the preload!
    
    Args:
        P_0_max(float): max expected preload in the joint
        SF(float): factor of safety
        P_et(float): resultant external load directed at the joint
        n(float): loading plane factor
        phi(float): joint stiffness factor
    Returns:
        float: total axial load in the fastener
    """
    P_b = P_0_max + (SF * n * phi * P_et)
    return P_b


# NASA-TM-106943, equation 18, pg 10
# n = distance between loading planes / total thickness of joint
# For update, see NASA TM 108377


def eq19(delta_P_b: float, delta_P_j: float) -> float:
    """NASA-TM-106943, equation 19, pg 10
    
    Calculate external tensile loading, P_et.
    
    Args:
        delta_P_b: change in axial bolt load
        delta_P_j: change in joint load
    Returns:
        float: external tensile loading
    """
    P_et = delta_P_b + delta_P_j
    return P_et


def eq20(
        P_0: float, 
        delta_b: float, 
        delta_j: float, 
        n: float, 
        delta: float,
    ) -> float:
    """NASA-TM-106943, equation 20, pg 10
    
    Calculate change in axial bolt load, delta_P_b.
    
    Args:
        P_o: nominal bolt preload
        delta_b: bolt deflection
        n: loading plane factor
        delta_j: joint abutment deflection
        delta: bolt deflection due to external load
    Returns:
        float: change in axial bolt load
    """
    delta_P_b = (P_0 / (delta_b + (1.0-n)*delta_j)) * delta
    return delta_P_b


def eq21(
        P_0: float, 
        n: float, 
        delta_j: float, 
        delta: float,
    ) -> float:
    """NASA-TM-106943, equation 21, pg 10
    
    Calculate change in joint load, delta_P_j.
    
    Args:
        P_0: nominal bolt preload
        n: loading plane factor
        delta_j: joint abutment deflection
        delta: bolt deflection due to external load
    Returns:
        float: change in joint load
    """
    delta_P_j = (P_0 / (n * delta_j)) * delta
    return delta_P_j


# NASA-TM-106943, equation 22, pg 11

# NASA-TM-106943, equation 23, pg 11

# NASA-TM-106943, equation 24, pg 11

# NASA-TM-106943, equation 25, pg 11


def eq26() -> float:
    """NASA-TM-106943, equation 26, pg 11
    
    """
    delta_b = P_o / K_b
    return delta_b


# NASA-TM-106943, equation 27, pg 11

# NASA-TM-106943, equation 28, pg 11
P_et = delta_P_b * ((K_b + K_j) / (n * K_b))


def eq29(K_b: float, K_j: float) -> float:
    """NASA-TM-106943, equation 29, pg 11
    
    Calculate stiffness factor (or load factor), phi.
    
    Args:
        K_b: bolt stiffness
        K_j: joint stiffness
    Returns:
        float: stiffness factor 
    """
    phi = K_b / (K_b + K_j)
    return phi


def eq30(
        n: float, 
        phi: float, 
        P_et: float,
    ) -> float:
    """NASA-TM-106943, equation 30, pg 11
    
    Calculate change in axial bolt load, delta_P_b.
    
    Args:
        P_et: resultant external load directed at the joint
        n: loading plane factor
        phi: joint stiffness factor
    Returns:
        float: change in axial bolt load
    """
    delta_P_b = n * phi * P_et
    return delta_P_b


########################################################
# Configuration 1: pg 12
# Hex, Socket, or Pan Head Through Bolt + Nut
########################################################


def eq31():
    """NASA-TM-106943, equation 31, pg 12
    
    Configuration 1
    
    Args:
        l_1:
        l_2:
        l_n:
    
    """
    L = l_1 + l_2 + ... + l_n
    return L


def eq32() -> float:
    """NASA-TM-106943, equation 32, pg 12
    
    Calculate bolt stiffness, K_b.
    
    Args:
        A:
        E_b:
        L:
    """
    K_b = A * E_b / L
    return K_b


# NASA-TM-106943, equation 33, pg 12
# joint stiffness:


def eq34(L) -> float:
    """NASA-TM-106943, equation 34, pg 12
    
    Calculate joint composite modulus, E_j.
    
    Args:
        L: total clamped length
        l_1:
        E_1:
        l_2:
        E_2:
        l_n:
        E_n:
    """
    E_j = L / ((l_1 / E_1) + (l_2 / E_2) + ... + (l_n / E_n))
    return E_j


def eq35() -> float:
    """NASA-TM-106943, equation 35, pg 12
    
    """
    n = (l_1 / 2.0 + l_2 + ... + l_n / 2.0) + l_1 + l_2 + ... + l_n
    return n


########################################################
# Configuration 2: pg 12
# Flat Head Through Bolt + Nut
########################################################

# equation 36:

# equation 37:
# bolt stiffness:
K_b = A * E_b / L

# equation 38:

# equation 39:

# equation 40:

# equation 41:


########################################################
# Configuration 3: pg 13
# Hex, Socket, or Pan Head Bolt Threaded Into final Part
########################################################

# equation 42:
L = l_1 + l_2 + ... + (l_n - L_i / 2.0)

# equation 43:
# bolt stiffness:
K_b = A * E_b / L

# equation 44:
K_j = np.pi * E_j * D / (np.log(5.0*((2.0*L + 0.5*D)/(2.0*L + 2.5*D))))

# equation 45:
E_j = L / (l1 / E_1 + l2 / E_2 + ... + ((l_n - L_i/2.0)/E_n))


def eq46() -> float:
    """equation 46, pg 
    
    """
    n = (l_1/2 + l_2 + ... + (l_n - L_i/2)) / (l_1 + l_2 + ... + l_n)
    return n


########################################################
# Configuration 4: pg 14
# Flat Head Bolt Threaded Into final Part
########################################################


def eq47() -> float:
    """NASA-TM-106943, equation 47, pg 
    
    Args:
        l_1:
        l_h:
    """
    L = (l_1 - l_h/2.0) + l_2 + ... + (l_n - L_i / 2.0)
    return L


def eq48() -> float:
    """NASA-TM-106943, equation 48, pg 
    
    # bolt stiffness:
    Args:
        A:
        E_b:
        L:
    """
    K_b = A * E_b / L
    return K_b


def eq49() -> float:
    """NASA-TM-106943, equation 49, pg 
    
    Args:
        E_j:
        D:
        L:
        d_w:
    """
    K_j = np.pi * E_j * D / np.log(((L + d_w - D)*(d_w + D)) / ((L + d_w + D)*(d_w - D))
    return K_j


def eq50() -> float:
    """equation 50, pg 
    
    Args:
    
    """
    d_w = d_h + D / 2.0
    return d_w


def eq51(L, l_2, E_2) -> float:
    """equation 51, pg
    
    """
    E_j = L / (() + l_2/E_2 + ... + ())
    return E_j


def eq52() -> float:
    """equation 52, pg 
    
    """
    n = ((l_1 - l_h / 2.0) + l_2 + ... + (l_n - L_i/2.0)) / (l_1 + l_2 + ... + l_n)
    return n


########################################################
# Fastener Strength Criteria: pg 15
########################################################

########################################################
# Tension Only Criteria: pg 15
########################################################


def eq53(tensile_allowable, P_b) -> float:
    """NASA-TM-106943, equation 53, pg 15
    
    margin of safety
    
    Args:
    
    """
    MS = (tensile_allowable / P_b) - 1.0
    return MS


########################################################
# Shear Only Criteria: pg 16
########################################################


def eq54(
        V: float, 
        shear_allowable: float, 
        SF: float,
    ) -> float:
    """NASA-TM-106943, equation 54, pg 16
    
    Calculate margin of safety against ???
    
    Args:
        V = externally applied shear load
    Returns:
        float: margin of safety against ???
    """
    MS = (shear_allowable / (SF * V)) - 1.0
    return MS


def eq55(F_su, A_s) -> float:
    """NASA-TM-106943, equation 55, pg 16
    
    Calculate shear allowable.
    
    Args:
        F_su: material ultimate shear strength
        A_s: shear area
    Returns:
        float: shear allowable
    """
    shear_allowable = F_su * A_s
    return shear_allowable


########################################################
# Combined Tension and Shear: pg 16
########################################################

# NASA-TM-106943, equation 56, pg 16
# R_t**2 + R_s**3 <= 1.0
# See update in NASA-STD-5020 based on NASA-TM-2012-217454


def eq57() -> float:
    """NASA-TM-106943, equation 57, pg 16
    
    axial (tension) load ratio:
    
    """
    R_t = P_b / bending_allowable
    return R_t


# NASA-TM-106943, equation 58, pg 16
# shear load ratio:
R_s = SF * V / shear_allowable


def eq59(R_t: float, R_s: float) -> float:
    """NASA-TM-106943, equation 59, pg 16
    
    margin of safety for combined tension and shear
    
    See update in NASA-STD-5020 based on NASA-TM-2012-217454
    
    Args:
        R_t: axial load ratio
        R_s: shear load ratio
    Returns:
        float: margin of safety for combined tension and shear
    """
    print("warning: deprecated, see updated criteria based on NASA-TM-2012-217454...")
    MS = (1.0 / np.sqrt(R_t**2 + R_s**3)) - 1.0
    return MS


########################################################
# Combined Tension, Shear, Bending: pg 17
########################################################

# NASA-TM-106943, equation 60, pg 17
# relation must hold for combination of tension, shear, bending:
# (R_t + R_b)**2 + R_s**3 <= 1.0
# See update in NASA-STD-5020 based on NASA-TM-2012-217454


def eq61(SF: float, M: float, bending_allowable: float) -> float:
    """NASA-TM-106943, equation 61, pg 17
    
    bending load ratio
    
    Args:
    
    """
    R_b = SF * M / bending_allowable
    return R_b


def eq62(R_t: float, R_b: float, R_s: float) -> float:
    """NASA-TM-106943, equation 62, pg 17
    
    margin of safety
    
    See update in NASA-STD-5020 based on NASA-TM-2012-217454
    
    Args:
        R_t:
        R_b:
        R_s:
    """
    print("warning: deprecated, see updated criteria based on NASA-TM-2012-217454...")
    MS = (1.0 / np.sqrt((R_t + R_b)**2 + R_s**3)) - 1.0
    return MS


########################################################
# Bolt Thread Shear: pg 18
########################################################


def eq63(L_e: float, D_minor_int: float) -> float:
    """NASA-TM-106943, equation 63, pg 18
    
    Calculate shear area of the bolt thread.
    
    Args:
        L_e: engaged length of bolt thread
        D_minor_int: minor pitch diameter, internal threads
    Returns:
        float: shear area of the bolt thread
    """
    A_s = 5.0 * np.pi * L_e * D_minor_int / 8.0
    return A_s


def eq64(F_su: float, A_s: float) -> float:
    """NASA-TM-106943, equation 64, pg 18
    
    Calculate ultimate load, P_ult.
    
    Args:
        F_su: material ultimate shear strength
        A_s: 
    Returns:
        float: ultimate load
    """
    P_ult = F_su * A_s
    return P_ult


def eq65(P_ult: float, P_b: float) -> float:
    """NASA-TM-106943, equation 65, pg 18
    
    Calculate margin of safety against bolt thread shear.
    
    Args:
        P_ult: ultimate tensile load
        P_b: total axial bolt load
    Returns:
        float: margin of safety against bolt thread shear
    """
    MS = P_ult / P_b - 1.0
    return MS


########################################################
# Joint Separation Criteria: pg 18
########################################################


# def eq66(n: float, phi: float, P_et: float) -> float:
#     """NASA-TM-106943, equation 66, pg 19
#     
#     Args:
#         n:
#         phi:
#         P_et:
#     """
#     DeltaP_b = n * phi * P_et
#     return DeltaP_b


def eq67(
        n: float, 
        phi: float, 
        P_et: float,
    ) -> float:
    """NASA-TM-106943, equation 67, pg 19
    
    Calculate load trying to separate the joint.
    
    Args:
        n: loading plane factor
        phi: joint stiffness factor
        P_et: total externally applied axial load
    Returns:
        float: load causing separation
    """
    P_sep = (1.0 - n * phi) * P_et
    return P_sep


def eq68(
        P_0_min: float, 
        P_sep: float, 
        SF: float=1.2,
    ) -> float:
    """NASA-TM-106943, equation 68, pg 19
    
    Calculate margin of safety against joint separation.
    
    Recommended factor of safety:
    1.2 for structural applications
    1.4 for pressure applications
    
    Args:
        P_0_min: minimum expected bolt preload
        P_sep: load trying to separate the joint
        SF: safety factor againt joint separation
    Return:
        float: margin of safety against joint separation
    """
    MS = (P_0_min / (SF * P_sep)) - 1.0
    return MS



########################################################
# Shear Tear Out: pg 19
########################################################


def eq69():
    """NASA-TM-106943, equation 69, pg 19
    
    """
    P_ult = F_su * A_s
    return P_ult


def eq70(t: float, e: float, D: float) -> float:
    """NASA-TM-106943, equation 70, pg 19
    
    A_s = shear area
    
    Args:
        t: thickness of sheet or lug
        e: perpendicular distance from hole center to free egde of the sheet
        D: nominal fastener diameter
    
    Returns:
        float: shear area
    """
    A_s = 2.0 * t * (e - D / 2.0)
    return A_s


def eq71(P_ult: float, SF: float, V: float) -> float:
    """NASA-TM-106943, equation 71, pg 20
    
    margin of safety
    
    Args:
    
    """
    MS = P_ult / (SF * V) - 1.0
    return MS


########################################################
# Bolt Bearing: pg 20
########################################################


def eq72(F_br: float, A_br: float) -> float:
    """NASA-TM-106943, equation 72, pg 20
    bearing load capability:
    Args:
        F_br = material bearing (yield or ultimate) strength
        A_br = bearing area
    Returns:
        float: bearing load capability
    """
    P_br = F_br * A_br
    return P_br


def eq73(D: float, t: float) -> float:
    """NASA-TM-106943, equation 73, pg 20
    
    bearing area
    
    Args:
        D: through hole diameter ?
        t: thickness
    Returns:
        float: bearing area
    """
    A_br = D * t
    return A_br


def eq74(P_br: float, SF: float, V: float) -> float:
    """NASA-TM-106943, equation 74, pg 20
    
    Args:
        P_br: bearing load capability
        SF:
        V:
    Returns:
        float: margin of safety to bolt bearing failure
    """
    MS = P_br / (SF * V) - 1.0
    return MS


########################################################
# Bearing Under the Bolt Head: pg 21
########################################################


def eq75(d_h: float, d_t: float) -> float:
    """NASA-TM-106943, equation 75, pg 21
    
    A_br = bearing area
    
    Args:
        d_h: minimum contact diameter of the bolt head or washer
        d_t: maximum diameter of the through hole
    Returns:
        float: bearing area
    """
    A_br = np.pi * (d_h**2 - d_t**2) / 4.0
    return A_br


########################################################
# Threaded Insert Analysis: pg 21
########################################################


def eq76(L_e: float, D_major_ext: float) -> float:
    """NASA-TM-106943, equation 76, pg 21
    
    A_s = thread shear area available to resist axial loading of the bolt
    
    Args:
        L_e: thread engagement length or nut thickness
        D_major_ext: major pitch diameter, external threads
    Returns:
        float: thread shear area available to resist axial loading of the bolt
    """
    A_s = 3.0 * np.pi * L_e * D_major_ext / 4.0
    return A_s


########################################################
# Insert Internal Thread Failure: pg 21
########################################################


def eq77(F_su: float, A_s: float) -> float:
    """NASA-TM-106943, equation 77, pg 21
    
    P_ult = insert ultimate allowable pull-out strength
    
    Args:
        F_su: material ultimate shear strength
        A_s: fastener shear cross sectional area
    Returns:
        float: insert ultimate allowable pull-out strength
    """
    P_ult = F_su * A_s
    return P_ult


########################################################
# Insert External Thread Failure: pg 22
########################################################


def eq78(F_su: float, A_s: float) -> float:
    """NASA-TM-106943, equation 78, pg 22
    
    P_ult = insert external thread pull-out strength
    
    Args:
        F_su: material ultimate shear strength
        A_s: fastener shear cross sectional area
    Returns:
        float: insert external thread pull-out strength
    """
    P_ult = F_su * A_s
    return P_ult


########################################################
# Insert Parent Material Thread Failure: pg 23
########################################################


def eq79(F_su: float, A_s: float) -> float:
    """NASA-TM-106943, equation 79, pg 23
    
    P_ult = insert parent material pull out strength
    
    Args:
        F_su(float): material ultimate shear strength
        A_s(float): fastener shear cross sectional area
    Returns:
        float: insert parent material pull out strength
    """
    P_ult = F_su * A_s
    return P_ult


########################################################
# Margin of Safety Criteria: pg 24
########################################################


def eq80(P_ult: float, P_b: float) -> float:
    """NASA-TM-106943, equation 80, pg 24
    
    MS = margin of safety
    
    Args:
        P_ult(float): strength
        P_b(float): total axial bolt load
    Returns:
        float: margin of safey to ???
    """
    MS = (P_ult / P_b) - 1.0
    return MS


########################################################
# Nut Strength: pg 25
########################################################


def eq81(A_t: float) -> float:
    """NASA-TM-106943, equation 81, pg 25
    
    P_ult = nut strength of standard MS class II nuts
    
    Args:
        A_t(float): tensile area
    Returns:
        float: nut strength of standard MS class II nuts
    """
    print("\nwarning, eq81, this is hardcoded in english units...\n")
    P_ult = 125000.0 * A_t
    return P_ult
