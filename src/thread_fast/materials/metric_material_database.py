"""Material Database in Metric Units

E: MPa = N/mm
cte: mm/mm/C
Sxx: MPa = N/mm
"""

a286_mat_dict = {
    'type': 'Material',
    'units': 'metric: N, mm, MPa, C',
    'name': 'A286',
    'E': 201e3,  # modulus of elasticity
    'nu': 0.3,  # Poisson's ratio
    'cte': 16.4e-6,  # coefficient of thermal expansion
    'Sty': 586,  # tensile yield strength
    'Stu': 896,  # tensile ultimate strength
    #'Ssy': ,  # shear yield strength
    #'Ssu': ,  # shear ultimate strength
    #'Scy': ,  # contact (bearing) yield strength
    #'Scu': ,  # contact (bearing) ultimate strength
}

inconel_718_mat_dict = {
    'type': 'Material',
    'units': 'metric: N, mm, MPa, C',
    'name': 'Inconel718',
    'E': 205e3,  # modulus of elasticity
    'nu': 0.29,  # Poisson's ratio
    'cte': 13e-6,  # coefficient of thermal expansion
    'Sty': 1100,  # tensile yield strength
    'Stu': 1375,  # tensile ultimate strength
    #'Ssy': ,  # shear yield strength
    #'Ssu': ,  # shear ultimate strength
    #'Scy': ,  # contact (bearing) yield strength
    #'Scu': ,  # contact (bearing) ultimate strength
}

mp35n_mat_dict = {
    'type': 'Material',
    'units': 'metric: N, mm, MPa, C',
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
    'units': 'metric: N, mm, MPa, C',
    'name': '15-5PH-H1025',
    'E': 198e3,  # modulus of elasticity
    'nu': 0.28,  # Poisson's ratio
    'cte': 10.8e-6,  # coefficient of thermal expansion
    'Sty': 1000,  # tensile yield strength
    'Stu': 1069,  # tensile ultimate strength
    #'Ssy': ,  # shear yield strength
    #'Ssu': ,  # shear ultimate strength
    #'Scy': ,  # contact (bearing) yield strength
    #'Scu': ,  # contact (bearing) ultimate strength
}

nitronic60_lvl3_cold_worked_mat_dict = {
    'type': 'Material',
    'units': 'metric: N, mm, MPa, C',
    'name': 'Nitronic 60 Level 3 Cold Worked',
    'E': 180e3,  # modulus of elasticity
    'nu': 0.3,  # Poisson's ratio
    'cte': 15.8e-6,  # coefficient of thermal expansion
    'Sty': 896,  # tensile yield strength
    'Stu': 1103,  # tensile ultimate strength
    #'Ssy': ,  # shear yield strength
    #'Ssu': ,  # shear ultimate strength
    #'Scy': ,  # contact (bearing) yield strength
    #'Scu': ,  # contact (bearing) ultimate strength
}

CRES301_dict = {
    'type': 'Material',
    'units': 'metric: N, mm, MPa, C',
    'name': '301 CRES (18-8)',
    'E': 195e3,  # modulus of elasticity
    'nu': 0.28,  # Poisson's ratio
    'cte': 16.6e-6,  # coefficient of thermal expansion
    'Sty': 517,  # tensile yield strength
    'Stu': 862,  # tensile ultimate strength
    #'Ssy': ,  # shear yield strength
    #'Ssu': ,  # shear ultimate strength
    #'Scy': ,  # contact (bearing) yield strength
    #'Scu': ,  # contact (bearing) ultimate strength
}

Al7075_T6_mat_dict = {
    'type': 'Material',
    'units': 'metric: N, mm, MPa, C',
    'name': 'Aluminum 7075-T6',
    'E': 71.7e3,  # modulus of elasticity
    'nu': 0.33,  # Poisson's ratio
    'cte': 23.6e-6,  # coefficient of thermal expansion
    'Sty': 503,  # tensile yield strength
    'Stu': 572,  # tensile ultimate strength
    #'Ssy': ,  # shear yield strength
    #'Ssu': ,  # shear ultimate strength
    #'Scy': ,  # contact (bearing) yield strength
    #'Scu': ,  # contact (bearing) ultimate strength
}

Al6061_T6_mat_dict = {
    'type': 'Material',
    'units': 'metric: N, mm, MPa, C',
    'name': 'Aluminum 6061-T6',
    'E': 68.9e3,  # modulus of elasticity
    'nu': 0.33,  # Poisson's ratio
    'cte': 23.6e-6,  # coefficient of thermal expansion
    'Sty': 276,  # tensile yield strength
    'Stu': 310,  # tensile ultimate strength
    #'Ssy': ,  # shear yield strength
    #'Ssu': ,  # shear ultimate strength
    #'Scy': ,  # contact (bearing) yield strength
    #'Scu': ,  # contact (bearing) ultimate strength
}

ti6al4v_grade5_mat_dict = {
    'type': 'Material',
    'units': 'metric: N, mm, MPa, C',
    'name': 'Titanium Ti6Al4V Grade 5',
    'E': 114e3,  # modulus of elasticity
    'nu': 0.33,  # Poisson's ratio
    'cte': 8.6e-6,  # coefficient of thermal expansion
    'Sty': 790,  # tensile yield strength
    'Stu': 860,  # tensile ultimate strength
    #'Ssy': ,  # shear yield strength
    #'Ssu': ,  # shear ultimate strength
    #'Scy': ,  # contact (bearing) yield strength
    #'Scu': ,  # contact (bearing) ultimate strength
}
