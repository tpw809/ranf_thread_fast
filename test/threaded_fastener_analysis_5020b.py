import numpy as np


# components to analyze:
# bolt threads
# bolt head
# washers
# insert threads with bolt
# insert threads with part (parent material)
# nut threads
# internally threaded part
# clamped parts

# performance to analyze:
# preload
# joint slip
# fatigue
# separation
# bolt yield
# bolt rupture

# Preload Control Methods:
# torque -> sensitive to lubrication
# turn-of-nut
# turn-angle
# bolt stretch


# limit loads, shear and tension
F_limit_shear = 1.0
F_limit_tension = 1.0


# factor of safety is applied to limit load
# based on structural design command media
FS_yield = 1.1
FS_ultimate = 1.4
FS_test = 1.0

F_yield = F_limit * FS_yield
F_ultimate = F_limit * FS_ultimate



# Fitting Factor
# accounts for uncertainties in load paths and stresses
FF_min = 1.15


# Separation Factor of Safety:
# if joint separation credibly leads to catstrophic hazard:
FS_sep = FS_ultimate

# if joint separation credibly leads to critical hazard:
FS_sep = max(1.2, FS_yield)

# else:
FS_sep = max(1.0, FS_test)


# Max and Min Preload

# max preload:
# eq 1:
P_p_max = P_pi_max + P_deltat_max
# P_pi_max = max initial preload
# P_deltat_max = calculated max increase in preload for max or min temperatures

# min preload:
# eq 2:
P_p_min = P_pi_min - P_pr - P_pc - P_deltat_min
# P_pi_min = min initial preload
# P_pr = short term relaxation, 5% for metal, test derived everything else
# P_pc = creep loss, by analyis
# P_deltat_min = calculated max decrease in preload for max or min temperatures

# P_pi_nom = nominal preload applicable to installation
# gamma = preload variation
# c_max = max value of installation controlled parameter factor
# c_min = min value of installation controlled parameter factor



def torque_control_parameter_factor(
        trq_nom: float, 
        trq_max: float, 
        trq_min: float,
    ):
    """
    From NASA 5020B page 22, 23
    
    c_max = (trq_nom + trq_tol) / trq_nom
    c_min = (trq_nom - trq_tol) / trq_nom
    
    example:
    if torque control is used and the effective torque is 
    specified as 40 ± 2 N-m, then cmin = (40 – 2)/40 = 0.95
    
    Args:
        trq_nom (float): Nominal specified torque
        trq_max (float): Max allowable specified torque
        trq_min (float): Min allowable specified torque
    """
    
    c_min = trq_min / trq_nom
    c_max = trq_max / trq_nom
    return c_min, c_max



# n_f = number of fasteners in the joint
n_f = 6

# Maximum initial preload for strength and fatigue analysis:
# eq 3:
P_pi_max = c_max * (1.0 + gamma) * P_pi_nom

# for critical separation and fatigue analysis:
# eq 4:
P_pi_min = c_min * (1.0 - gamma) * P_pi_nom

# for non-critical separation and joint slip analysis:
# eq 5:
P_pi_min = c_min * (1.0 - gamma / np.sqrt(n_f)) * P_pi_nom


# 4.3.2 Nominal Preload
# [TFSR 6] Calculation of the nominal (mean) initial preload, Ppi-nom, shall be substantiated by tests of a minimum of six sets of the fastening system hardware per Table 2, Nominal Preload Determination, to determine the relationship between initial preload and the parameter controlled during installation (torque, turn-of-nut, turn-angle, or bolt stretch).


# 4.3.3 Preload Variation
# [TFSR 7] The preload variation, gamma, used to calculate the 
# minimum and maximum initial preload shall be based on the 
# criteria of Table 3, Preload Variation Determination.

# gamma = preload variation

preload_method = 'torque'  # 'turn_angle', 'bolt_stretch'


def preload_variation(preload_method):
    """
    From NASA 5020B Table 3, page 25
    """
    if preload_method == 'torque':
        # lubricated:
        gamma = 0.25
        # unlubricated:
        gamma = 0.35
    elif preload_method == 'turn_angle':
        gamma = 0.25
    elif preload_method == 'bolt_stretch':
        gamma = 0.10
    else:
        raise Exception('select valid preload method')
    return gamma



# 4.4.1 Ultimate Design Loads
# [TFSR 8] Threaded fastening system hardware shall withstand 
# ultimate design loads (limit load times the ultimate factor 
# of safety and fitting factor) without failure when subjected 
# to:
# a. The accompanying service environments (for example, 
# temperature) and
# b. A coefficient of friction between clamped parts equal 
# to zero (applicable only to verification by analysis, 
# not applicable to verification by test) (see TFSR 13).

# F_ultimate = FS_ultimate * FF_ultimate * F_limit



# Margin of Safety:
# if separation occurs before rupture:
# eq 6:
MS_ultimate = P_tu_allowable / (FF_ultimate * FS_ultimate * F_limit) - 1.0

# if rupture occurs before separation:
# eq 7:
MS_ultimate = P_prime_tu / (FF_ultimate * FS_ultimate * F_limit) - 1.0

# P_prime_tu = applied tensile load that causes the fastener 
# load to exceed the fastening systems allowable ultimate 
# tensile load

# P_tu_allowable = allowable ultimate load for the fastening system

# P_tL = F_limit

# Tensile load in a preloaded bolt:
# eq 8:
P_tb = P_p + n * phi * P_t
# P_p = preload
# P_t = applied tensile load
# n = load introduction factor
# phi = stiffness factor

# stiffness factor:
# eq 9:
phi = k_b / (k_b + k_c)
# k_b = stiffness of the bolt
# k_c = stiffness of the clamped parts local to the fastener

# Applied tensile load that causes bolt to exceed allowable ultimate tensile load for the fastening system:
# eq 10:
P_prime_tu = 1.0 / (n * phi) * (P_tu_allowable - P_p_max)

# Linearly projected load that causes separation when at maximum preload:
# eq 11:
P_prime_sep = P_p_max / (1.0 - n * phi)

# If P_prime_sep < P_prime_tu, then separation occurs before rupture, and ultimate margin of safety is determined by eq 6.
# Eq 7 used when rupture occurs before separation.

# Allowable ultimate shear load:
# when threads not in the shear plane:
# eq 12:
P_su_allowable = np.pi * D**2 * F_su / 4.0

# when threads are in the shear plane:
# eq 13: 
P_su_allowable = F_su * A_m
# A_m = minimum minor diameter area for the fastener threads

# Ultimate margin of safety for shear loading of fasteners:
# eq 14:
MS_ultimate = P_su_allowable / (FF * FS_ultimate * P_sL) - 1.0
# P_sL = limit shear load acting on the shear plane

# 4.4.2 Yield Design Loads
# [TFSR 9] Threaded fastening system hardware shall withstand 
# yield design loads (limit load times the yield factor of 
# safety and fitting factor) without detrimental yielding 
# or detrimental deformation when subjected to the 
# accompanying service environments (for example, temperature).

# Margin of safety for yield under axial load:
# eq 15:
MS_yield = P_ty_allow / (FF * FS_y * P_tL) - 1.0


# eq 16:
MS_yield = P_prime_ty / (FF * FS_y * P_tl) - 1.0

# applied tensile load that causes the fastener load to exceed the fastening systems allowable yield tensile load if yielding occurs before separation:
# eq 17:
p_prime_ty = (1.0 / (n * phi)) * (P_ty_allow - P_p_max)
# P_ty_allow = allowable tensile load of the material
# n = load introduction factor
# phi = stiffness factor

# eq 18:
P_ty_allow = (F_ty / F_tu) * P_tu_allow


# 4.4.3 Separation Loads
# [TFSR 10] Threaded fastening system hardware shall 
# withstand design separation loads (limit load times the 
# separation factor of safety and fitting factor) without 
# loss of compression between the joint members or 
# detrimental deformation due to separation when subjected 
# to the accompanying service environments (for example, 
# temperature).

# margin of safety for separation:
# eq 19:
MS_sep = P_p_min / (FF * FS_sep * P_tL) - 1.0
# FS_sep = separation factor of safety per section 4.2.3


# 4.4.4 Combination of Loads
# [TFSR 11] The limit, yield, ultimate, and separation 
# loads shall account for interaction of the combined 
# loading (simultaneously applied tensile, shear, and 
# bending loads) and under all design environmental 
# conditions.


# eq 20:
(P_su / P_su_allow)**2.5 + (P_tu / P_tu_allow + f_bu / F_tu)**1.5 <= 1.0

# eq 21:
(P_su / P_su_allow)**2.5 + (P_tu / P_tu_allow)**1.5 + (f_bu / F_bu) <= 1.0

# eq 22:
(P_su / P_su_allow)**1.2 + (P_tu / P_tu_allow + f_bu / F_tu)**2 <= 1.0

# eq 23:
(P_su / P_su_allow)**1.2 + (P_tu / P_tu_allow)**2 + (f_bu / F_bu) <= 1.0


# 4.4.5 Inclusion of Preload in Yield and Ultimate Load Strength
# [TFSR 12] If rupture occurs before separation, preload 
# shall be included in the determination of the total 
# tensile load in the preloaded bolt.

# 4.4.6 Use of Friction at Limit and Yield Load
# [TFSR 13] Use of friction to react shear loads shall only be permissible for analysis at limit load (alignment, fatigue, and fracture) or yield load.

# [TFSR 14] Unless otherwise substantiated by test, the coefficient of friction for joint-slip analysis shall be no greater than:
# (1) 0.20 for uncoated, non-lubricated metal surfaces that are cleaned by a qualified process and visibly clean at and after assembly.
# (2) 0.10 for all other surfaces, including nonmetallic (coated or uncoated) surfaces and metallic surfaces that are coated with any substance, including lubricant, paint, and conversion coating.


# 4.5 Fatigue Life
# [TFSR 15] All threaded fastening systems shall be designed to withstand the entire service life, including the life scatter factor specified by the program or project, and service environment without fatigue failure.


# 4.6 Locking Features
# 4.6.1 Preload Independent Locking Feature



# APPENDIX A
# EXPLANATION AND JUSTIFICATION OF FASTENER ANALYSIS CRITERIA
# A.2 

# eq 24:
P_pi_nom = T / (K_nom * D)
# D = nominal bolt diameter
# K_nom = nominal nut factor
# T = nominal effective torque

# eq 25:
P_pi_max = (1.0 + gamma) * T_max / (K_nom * D)
# gamma = preload variation
# T_max = max effective torque

# eq 26a:
P_pi_min = (1.0 - gamma) * T_min / (K_nom * D)
# gamma = preload variation
# T_max = max effective torque

# eq 26b:
P_pi_min = (1.0 - gamma / np.sqrt(n_f)) * T_min / (K_nom * D)


# eq 27:

# eq 28:

# T_s_max = max specified torque
# T_s_min = min specified torque
# T_br_min = min breakaway torque of locking feature
# T_L_max = max locking torque specified for the locking feature


# eq 32:
K_nom = T / (D * P_pi_nom)



# gamma_a_max = 
# gamma_a_min = 




# A.5 Bolt Analysis: 
# Separation before Rupture (Supplement to Section 4.4.5)



# A.6 Ultimate Margin of Safety for Tensile Loading with Linear Theory
# (Supplement to Section 4.4.1)



# A.7 Omission of Preload in Shear and Interaction Analyses 
# (Supplement to Sections 4.4.1 and 4.4.4)



# A.8 Theoretical Treatment of Interaction Equations 
# (Supplement to Section 4.4.4)

# sigma = stress tensor
sigma = np.array([
    [0,0,tau], 
    [0,0,0], 
    [tau,0,0],
])

# principal stresses:
S1 = 0
S2 = tau
S3 = -tau

# von Mises criterion:
# (S1 - S2)**2 + (S2 - S3)**2 + (S3 - S1)**2 <= 2.0*Fty**2

# F_ty = yield stress in tension
# F_sy = yield stress in shear

# F_sy = F_ty / np.sqrt(3.0)
# F_su = F_tu / np.sqrt(3.0)



# A.9 Determining if Fastener Yielding is Detrimental 
# for Separation or Joint Slip 
# (Supplement to Section 4.4.2)



# A.10 Margin of Safety for Joint Slip 
# (Supplement to Sections 4.4.1 and 4.4.6)

# P_f = friction load
# P_f = mu * (n_f * P_p_nom - P_t_joint)
# P_t_joint = total applied tensile load acting on the joint
# mu = coefficient of friction



# A.11 Margin of Safety for Bolted Joint Separation 
# (Supplement to Section 4.4.3)



# APPENDIX B
# BEST PRACTICES FOR LOCKING FEATURES


# Appendix C 
# Justification for low likelihood of fatigue failure

# Miner's Rule:
# D = sum_i=1^j (n_i / N_i) <= 1
# D = cumulative damage
# n_i = number of loading cycles at a given stress level
# N_i = number of cycles to failure at that stress level
# j = number of different stress levels
