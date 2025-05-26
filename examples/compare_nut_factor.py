import numpy as np
import thread_fast
import thread_fast.nsts_08307a as nsts_08307a
import thread_fast.nasa_tm_106943 as nasa_tm_106943
import thread_fast.nasa_std_5020 as nasa_std_5020

# conversion factors:
deg_to_rad = np.pi / 180.0
psi_to_MPa = 0.00689476

# [mm/thread], screw pitch: for M5 coarse thread
pitch = 0.8
print(f"pitch = {pitch} [mm/thread]")

# Basic major diameter of external threads (bolt):
D = 5.0

# [mm], fastener major (outer) diameter:
D_major = 4.976

# [mm], fastener minor diameter:
D_minor = 4.134

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
# alpha = np.arctan(1.0 / (n_0 * np.pi * E_in))
# print(f"alpha = {alpha} [rad]")
# print(f"alpha = {alpha / deg_to_rad} [deg]")

# [rad], thread half angle:
beta = 30.0 * deg_to_rad
print(f"beta = {beta} [rad]")

# Effective radius of torqued element-to-joint bearing forces = 1/2 x (Ro + Ri)
R_e = 0.5 * (D / 2.0 + 8.5 / 2.0)
print(f"R_e = {R_e} [mm]")

# check if TM-106942 should be using half angle:
# [rad], thread angle:
alpha2 = 60.0 * deg_to_rad
print(f"alpha2 = {alpha2} [rad]")


K_kb = thread_fast.kubler_bulten_nut_factor(
    P=pitch, 
    d_2=E, 
    mu_t=0.15, 
    mu_b=0.15, 
    d_w=2.0*R_e, 
    d=D,
)
print(f"K_kb = {K_kb}")


K_08307 = nsts_08307a.nut_factor(
    R_t=r_m, 
    R_e=R_e, 
    mu_t_min=0.1,
    mu_t_typ=0.15, 
    mu_t_max=0.2,
    mu_b_min=0.1,
    mu_b_typ=0.15, 
    mu_b_max=0.2,
    alpha=psi, 
    beta=beta, 
    D=D,
)
print(f"K_08307 = {K_08307}")


K_106943 = nasa_tm_106943.eq2(
    D_p=E, 
    D=D, 
    psi=psi, 
    alpha=beta, 
    mu=0.15, 
    mu_c=0.15,
)
print(f"K_106943 = {K_106943}")
