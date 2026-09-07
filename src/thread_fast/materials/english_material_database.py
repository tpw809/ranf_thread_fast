"""Material Database in English Units

E: psi = lb/in^2
cte: in/in/F
Sxx: psi = lb/in^2
"""

a286_mat_dict = {
    'type': 'Material',
    'units': 'english: lb, in, psi, F',
    'name': 'A286 (Alloy 660)',
    'E': 29.0e6,  # modulus of elasticity
    'nu': 0.3,  # Poisson's ratio
    'cte': 9.2e-6,  # coefficient of thermal expansion
    'Sty': 95e3,  # tensile yield strength
    'Stu': 180e3,  # tensile ultimate strength
    #'Ssy': ,  # shear yield strength
    'Ssu': 108e3,  # shear ultimate strength
    #'Scy': ,  # contact (bearing) yield strength
    #'Scu': ,  # contact (bearing) ultimate strength
}

inconel_718_mat_dict = {
    'type': 'Material',
    'units': 'english: lb, in, psi, F',
    'name': 'Inconel718',
    'E': 29.0e6,  # modulus of elasticity
    'nu': 0.29,  # Poisson's ratio
    'cte': 7.15e-6,  # coefficient of thermal expansion
    'Sty': 150e3,  # tensile yield strength
    'Stu': 180e3,  # tensile ultimate strength
    #'Ssy': ,  # shear yield strength
    #'Ssu': ,  # shear ultimate strength
    #'Scy': ,  # contact (bearing) yield strength
    #'Scu': ,  # contact (bearing) ultimate strength
}

mp35n_mat_dict = {
    'type': 'Material',
    'units': 'english: lb, in, psi, F',
    'name': 'MP35N',
    'E': 0,  # modulus of elasticity
    'nu': 0,  # Poisson's ratio
    'cte': 0,  # coefficient of thermal expansion
    'Sty': 0,  # tensile yield strength
    'Stu': 0,  # tensile ultimate strength
    #'Ssy': ,  # shear yield strength
    #'Ssu': ,  # shear ultimate strength
    #'Scy': ,  # contact (bearing) yield strength
    #'Scu': ,  # contact (bearing) ultimate strength
}

SS15_5PH_H1025_mat_dict = {
    'type': 'Material',
    'units': 'english: lb, in, psi, F',
    'name': '15-5PH-H1025',
    'E': 28.5e6,  # modulus of elasticity
    'nu': 0.27,  # Poisson's ratio
    'cte': 6.0e-6,  # coefficient of thermal expansion
    'Sty': 145e3,  # tensile yield strength
    'Stu': 155e3,  # tensile ultimate strength
    #'Ssy': ,  # shear yield strength
    #'Ssu': ,  # shear ultimate strength
    #'Scy': ,  # contact (bearing) yield strength
    #'Scu': ,  # contact (bearing) ultimate strength
}

nitronic60_lvl3_cold_worked_mat_dict = {
    'type': 'Material',
    'units': 'english: lb, in, psi, F',
    'name': 'Nitronic 60 Level 3 Cold Worked',
    'E': 0,  # modulus of elasticity
    'nu': 0,  # Poisson's ratio
    'cte': 0,  # coefficient of thermal expansion
    'Sty': 0,  # tensile yield strength
    'Stu': 0,  # tensile ultimate strength
    #'Ssy': ,  # shear yield strength
    #'Ssu': ,  # shear ultimate strength
    #'Scy': ,  # contact (bearing) yield strength
    #'Scu': ,  # contact (bearing) ultimate strength
}

CRES301_mat_dict = {
    'type': 'Material',
    'units': 'english: lb, in, psi, F',
    'name': '301 CRES (18-8)',
    'E': 28.0e6,  # modulus of elasticity
    'nu': 0.28,  # Poisson's ratio
    'cte': 9.2e-6,  # coefficient of thermal expansion
    'Sty': 110e3,  # tensile yield strength
    'Stu': 150e3,  # tensile ultimate strength
    #'Ssy': ,  # shear yield strength
    #'Ssu': ,  # shear ultimate strength
    #'Scy': ,  # contact (bearing) yield strength
    #'Scu': ,  # contact (bearing) ultimate strength
}

Al7075_T6_mat_dict = {
    'type': 'Material',
    'units': 'english: lb, in, psi, F',
    'name': 'Aluminum 7075-T6',
    'E': 10.4e6,  # modulus of elasticity
    'nu': 0.33,  # Poisson's ratio
    'cte': 12.9e-6,  # coefficient of thermal expansion
    'Sty': 73e3,  # tensile yield strength
    'Stu': 83e3,  # tensile ultimate strength
    #'Ssy': ,  # shear yield strength
    #'Ssu': ,  # shear ultimate strength
    #'Scy': ,  # contact (bearing) yield strength
    #'Scu': ,  # contact (bearing) ultimate strength
}

Al6061_T6_mat_dict = {
    'type': 'Material',
    'units': 'english: lb, in, psi, F',
    'name': 'Aluminum 6061-T6',
    'E': 10.0e6,  # modulus of elasticity
    'nu': 0.33,  # Poisson's ratio
    'cte': 13.1e-6,  # coefficient of thermal expansion
    'Sty': 40e3,  # tensile yield strength
    'Stu': 45e3,  # tensile ultimate strength
    #'Ssy': ,  # shear yield strength
    #'Ssu': ,  # shear ultimate strength
    #'Scy': ,  # contact (bearing) yield strength
    #'Scu': ,  # contact (bearing) ultimate strength
}

ti6al4v_grade5_mat_dict = {
    'type': 'Material',
    'units': 'english: lb, in, psi, F',
    'name': 'Titanium Ti6Al4V Grade 5',
    'E': 16.5e6,  # modulus of elasticity
    'nu': 0.33,  # Poisson's ratio
    'cte': 5.0e-6,  # coefficient of thermal expansion
    'Sty': 120e3,  # tensile yield strength
    'Stu': 130e3,  # tensile ultimate strength
    #'Ssy': ,  # shear yield strength
    #'Ssu': ,  # shear ultimate strength
    #'Scy': ,  # contact (bearing) yield strength
    #'Scu': ,  # contact (bearing) ultimate strength
}

SS440C_mat_dict = {
    'type': 'Material',
    'units': 'english: lb, in, psi, F',
    'name': 'SS440C',
    'E': 29e6,  # modulus of elasticity
    'nu': 0.28,  # Poisson's ratio
    'cte': 5.6e-6,  # coefficient of thermal expansion
    'Sty': 250e3,  # tensile yield strength
    'Stu': 270e3,  # tensile ultimate strength
    #'Ssy': ,  # shear yield strength
    #'Ssu': ,  # shear ultimate strength
    #'Scy': ,  # contact (bearing) yield strength
    #'Scu': ,  # contact (bearing) ultimate strength
}


def main() -> None:
    print(a286_mat_dict)
    print(inconel_718_mat_dict)
    print(mp35n_mat_dict)
    print(SS15_5PH_H1025_mat_dict)
    print(nitronic60_lvl3_cold_worked_mat_dict)
    print(CRES301_mat_dict)
    print(Al7075_T6_mat_dict)
    print(Al6061_T6_mat_dict)
    print(ti6al4v_grade5_mat_dict)
    print(SS440C_mat_dict)
    
    
if __name__ == "__main__":
    main()
    