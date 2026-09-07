"""MS20033 thru MS20046 Component Data

Bolt, Machine, Hexagon Head 1200 F

Material is A286 per AMS 5731, AMS 5732, or AMS 5737

Rev C, 1970

Threads UNFJ-3A per MIL-S-8879

Designed for use with MS20500 and MS20501 Nuts

Sizes:
MS20033: #10 = 3/16 = 0.1875
MS20034: 1/4 = 0.25
MS20035: 5/16 = 0.3125
MS20036: 3/8 = 0.375
MS20037: 7/16 = 0.4375
MS20038: 1/2 = 0.5
MS20039: 9/16 = 0.5625
MS20040: 5/8 = 0.625
MS20042: 3/4 = 0.75
MS20044: 7/8 = 0.875
MS20045: 1 = 1.0

Units: in, lb

Procurement Spec is MIL-B-7874B
"""

# #10 (3/16):
MS20033 = {
    "name": "MS20033",
    "units": "english: in, lb",
    "thread": "UNFJ-3A-0.1900-32",
    "hex_flats_A_min": 0.365,
    "hex_flats_A_max": 0.377,
    "hex_points_B_ref": 0.430,
    "head_height_max": 0.141,
    "head_height_min": 0.109,
    "shank_diameter_min": 0.186,
    "shank_diameter_max": 0.189,
    "head_diameter_min": 0.359,
    "head_diameter_max": 0.391,
    "grip_length": 0,
    "total_length": 0,
    "min_tensile_break_strength": 3000,
}

# 1/4:
MS20034 = {
    "name": "MS20034",
    "units": "english: in, lb",
    "thread": "UNFJ-3A-0.2500-28",
    
    "grip_length": 0,
    "total_length": 0,
    "min_tensile_break_strength": 5400,
}

# 5/16:
MS20035 = {
    "name": "MS20035",
    "units": "english: in, lb",
    "thread": "UNFJ-3A-0.3125-24",
    
    "grip_length": 0,
    "total_length": 0,
    "min_tensile_break_strength": 8600,
}

# 3/8:
MS20036 = {
    "name": "MS20036",
    "units": "english: in, lb",
    "thread": "UNFJ-3A-0.3750-24",
    
    "grip_length": 0,
    "total_length": 0,
    "min_tensile_break_strength": 13300,
}

# 7/16:
MS20037 = {
    "name": "MS20037",
    "units": "english: in, lb",
    "thread": "UNFJ-3A-0.4375-20",
    
    "grip_length": 0,
    "total_length": 0,
    "min_tensile_break_strength": 18000,
}

# 1/2:
MS20038 = {
    "name": "MS20038",
    "units": "english: in, lb",
    "thread": "UNFJ-3A-0.5000-20",
    
    "grip_length": 0,
    "total_length": 0,
    "min_tensile_break_strength": 24000,
}

# 9/16:
MS20039 = {
    "name": "MS20039",
    "units": "english: in, lb",
    "thread": "UNFJ-3A-0.5625-18",
    
    "grip_length": 0,
    "total_length": 0,
    "min_tensile_break_strength": 30500,
}

# 5/8 in:
MS20040 = {
    "name": "MS20040",
    "units": "english: in, lb",
    "thread": "UNFJ-3A-0.6250-18",
    
    "grip_length": 0,
    "total_length": 0,
    "min_tensile_break_strength": 38100,
}

# 3/4 in:
MS20042 = {
    "name": "MS20042",
    "units": "english: in, lb",
    "thread": "UNFJ-3A-0.7500-16",
    
    "grip_length": 0,
    "total_length": 0,
    "min_tensile_break_strength": 55300,
}

# 7/8 in:
MS20044 = {
    "name": "MS20044",
    "units": "english: in, lb",
    "thread": "UNFJ-3A-0.8750-14",
    
    "grip_length": 0,
    "total_length": 0,
    "min_tensile_break_strength": 75500,
}

# 1 in:
MS20045 = {
    "name": "MS20045",
    "units": "english: in, lb",
    "thread": "UNFJ-3A-1.0000-12",
    
    "grip_length": 0,
    "total_length": 0,
    "min_tensile_break_strength": 98400,
}


def main() -> None:
    # example modify dictionary:
    my_bolt = MS20033
    my_bolt["grip_length"] = 1.0
    my_bolt["total_length"] = 1.5
    print(my_bolt)
    
    
if __name__ == "__main__":
    main()
    