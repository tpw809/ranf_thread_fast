"""Database of english threads.

Units: in, in^2

UNC = unified thread coarse
UNF = unified thread fine
UNJC = unified thread coarse, controlled root
UNJF = unified thread fine, controlled root
UNEF = unified thread extra fine
UNJEF = unified thread extra fine, controlled root

Standards:

FED-STD-H28/1: Nomenclature, Definitions, and Letter Symbols for Screw Threads
FED-STD-H28/2: Unified Inch Screw Threads - UN and UNR Thread Forms
FED-STD-H28/4: Controlled Radius Root Screw Threads, UNJ Symbol
UNJ threads controlled by MIL-S-8879C (1991)

Thread Classes: tolerance and allowance
Classes 1A, 2A, 3A apply to external threads
Classes 1B, 2B, 3B apply to internal threads
Classes 3A & 3B: no no allowance or clearance for assembly

n = tpi = threads per inch = threads / inch
p = pitch = 1 / n

Sizes:
#0 = ~1/16 = 0.06
#1 = ~5/64 = 0.073
#2 = ~3/32 = 0.086
#3 = ~7/64 = 0.099
#4 = ~7/64 = 0.112
#5 = 1/8 = 0.125
#6 = ~9/64 = 0.138
#8 = ~5/32 = 0.1640
#10 = ~3/16 = 0.1900
#12 = ~7/32 = 0.2160
1/4 = 0.25
5/16 = 0.3125
3/8 = 0.375
7/16 = 0.4375
1/2 = 0.5
9/16 = 0.5625
5/8 = 0.625
3/4 = 0.75
7/8 = 0.875
1 = 1.0

For number series:
major_diameter = size_number * 0.013 + 0.060

"""

#########################
# UNC Coarse Thread:
#########################

UNC_ext_3_4_10 = {
    "type": "Thread",
    "name": "Unified Thread Coarse Size 3/4, 10tpi",
    "units": "english: in",
    'beta_deg': 30.0,  # deg
    "basic_major_diameter": 0.75,
    "tpi": 10,  # threads per inch = threads / inch
    "pitch": 1.0/10.0,  # in
    "external": True,
}

UNC_ext_7_8_9 = {
    "type": "Thread",
    "name": "Unified Thread Coarse Size 7/8, 9tpi",
    "units": "english: in",
    'beta_deg': 30.0,  # deg
    "basic_major_diameter": 0.875,
    "tpi": 9,  # threads per inch = threads / inch
    "pitch": 1.0/9.0,  # in
    "external": True,
}

#########################
# UNJC Coarse Thread, Controlled Root:
# from MIL-S-8879C, Table II, pg 18:
#########################

UNJC_ext_3_4_10 = {
    "type": "Thread",
    "name": "Unified Thread Coarse Size 3/4, 10tpi",
    "units": "english: in",
    'beta_deg': 30.0,  # deg
    "basic_major_diameter": 0.75,
    "tpi": 10,  # threads per inch = threads / inch
    "pitch": 1.0/10.0,  # in
    "external": True,
}

UNJC_ext_7_8_9 = {
    "type": "Thread",
    "name": "Unified Thread Coarse Size 7/8, 9tpi",
    "units": "english: in",
    'beta_deg': 30.0,  # deg
    "basic_major_diameter": 0.875,
    "tpi": 9,  # threads per inch = threads / inch
    "pitch": 1.0/9.0,  # in
    "external": True,
}


#########################
# UNF Fine Thread:
#########################

UNF_ext_3_4_16 = {
    "type": "Thread",
    "name": "Unified Thread Fine Size 3/4, 16tpi",
    "units": "english: in",
    'beta_deg': 30.0,  # deg
    "basic_major_diameter": 0.75,
    "tpi": 16,  # threads per inch = threads / inch
    "pitch": 1.0/16.0,  # in
    "external": True,
}


#########################
# UNJF Fine Thread, Controlled Root:
# from MIL-S-8879C, Table III, pg 20:
#########################

#########################
# External Threads:
#########################

UNJF_ext_10_32_class3A = {
    "type": "Thread",
    "name": "Unified Thread Fine Size #10, 32tpi",
    "units": "english: in",
    'beta_deg': 30.0,  # deg
    "basic_major_diameter": 0.19,
    "tpi": 32,  # threads per inch = threads / inch
    "pitch": 1.0/32.0,  # in
    "external": True,
    "class": "3A",
    "series": "UNJF",
    "min_major_diameter": 0.1840,
    "max_major_diameter": 0.1900,
    "min_pitch_diameter": 0.1674,
    "max_pitch_diameter": 0.1697,
    "min_minor_diameter": 0.1497,
    "max_minor_diameter": 0.1539,
    "min_root_radius": 0.0047,
    "max_root_radius": 0.0056,
}

UNJF_ext_1_4_28_class3A = {
    "type": "Thread",
    "name": "Unified Thread Fine Size 1/4, 28tpi",
    "units": "english: in",
    'beta_deg': 30.0,  # deg
    "basic_major_diameter": 0.25,
    "tpi": 28,  # threads per inch = threads / inch
    "pitch": 1.0/28.0,  # in
    "external": True,
    "class": "3A",
    "series": "UNJF",
    "min_major_diameter": 0.2435,
    "max_major_diameter": 0.2500,
    "min_pitch_diameter": 0.2243,
    "max_pitch_diameter": 0.2268,
    "min_minor_diameter": 0.2041,
    "max_minor_diameter": 0.2088,
    "min_root_radius": 0.0054,
    "max_root_radius": 0.0064,
}

UNJF_ext_3_8_24_class3A = {
    "type": "Thread",
    "name": "Unified Thread Fine Size 3/8, 24tpi",
    "units": "english: in",
    'beta_deg': 30.0,  # deg
    "basic_major_diameter": 0.375,
    "tpi": 24,  # threads per inch = threads / inch
    "pitch": 1.0/24.0,  # in
    "external": True,
    "class": "3A",
    "series": "UNJF",
    "min_major_diameter": 0.3678,
    "max_major_diameter": 0.3750,
    "min_pitch_diameter": 0.3450,
    "max_pitch_diameter": 0.3479,
    "min_minor_diameter": 0.3214,
    "max_minor_diameter": 0.3268,
    "min_root_radius": 0.0063,
    "max_root_radius": 0.0075,
}

UNJF_ext_7_8_14_class3A = {
    "type": "Thread",
    "name": "Unified Thread Fine Size 7/8, 14tpi",
    "units": "english: in",
    'beta_deg': 30.0,  # deg
    "basic_major_diameter": 0.875,
    "tpi": 14,  # threads per inch = threads / inch
    "pitch": 1.0/14.0,  # in
    "external": True,
    "class": "3A",
    "series": "UNJF",
    "min_major_diameter": 0.8747,
    "max_major_diameter": 0.8750,
    "min_pitch_diameter": 0.8245,
    "max_pitch_diameter": 0.8286,
    "min_minor_diameter": 0.7841,
    "max_minor_diameter": 0.7925,
    "min_root_radius": 0.0107,
    "max_root_radius": 0.0129,
}


#########################
# Internal Threads:
#########################

UNJF_int_3_8_24_class3A = {
    "type": "Thread",
    "name": "Unified Thread Fine Size 3/8, 24tpi",
    "units": "english: in",
    'beta_deg': 30.0,  # deg
    "basic_major_diameter": 0.375,
    "tpi": 24,  # threads per inch = threads / inch
    "pitch": 1.0/24.0,  # in
    "internal": True,
    "class": "3B",
    "series": "UNJF",
    "min_major_diameter": 0.3750,
    # "max_major_diameter": 0.0,
    "min_pitch_diameter": 0.3479,
    "max_pitch_diameter": 0.3516,
    "min_minor_diameter": 0.3344,
    "max_minor_diameter": 0.3418,
    "min_root_radius": 0.00,
    "max_root_radius": 0.00,
}

#########################
# UNJEF Extra Fine Thread, Controlled Root radius:
# from MIL-S-8879C, Table IV, pg 21:
#########################

UNJEF_ext_12_32 = {
    "type": "Thread",
    "name": "Unified Thread Extra Fine Size #12, 32tpi",
    "units": "english: in",
    'beta_deg': 30.0,  # deg
    "basic_major_diameter": 0.2160,
    "tpi": 32,  # threads per inch = threads / inch
    "pitch": 1.0/32.0,  # in
    "external": True,
}

UNJEF_ext_1_4_32 = {
    "type": "Thread",
    "name": "Unified Thread Extra Fine Size 1/4, 32tpi",
    "units": "english: in",
    'beta_deg': 30.0,  # deg
    "basic_major_diameter": 0.2500,
    "tpi": 32,  # threads per inch = threads / inch
    "pitch": 1.0/32.0,  # in
    "external": True,
}

UNJEF_ext_5_16_32 = {
    "type": "Thread",
    "name": "Unified Thread Extra Fine Size 5/16, 32tpi",
    "units": "english: in",
    'beta_deg': 30.0,  # deg
    "basic_major_diameter": 0.3125,
    "tpi": 32,  # threads per inch = threads / inch
    "pitch": 1.0/32.0,  # in
    "external": True,
}

UNJEF_ext_3_8_32 = {
    "type": "Thread",
    "name": "Unified Thread Extra Fine Size 3/8, 32tpi",
    "units": "english: in",
    'beta_deg': 30.0,  # deg
    "basic_major_diameter": 0.3750,
    "tpi": 32,  # threads per inch = threads / inch
    "pitch": 1.0/32.0,  # in
    "external": True,
}


def main() -> None:
    import json
    
    print("\nEnglish Unified Thread Database:\n")
    
    print("\nUNC Series:\n")
    
    print("\nUNF Series:\n")
    
    print("\nUNEF Series:\n")
    
    
    print("\nUNJC Series:\n")
    
    print("\nUNJF Series:\n")
    print(json.dumps(UNJF_ext_10_32_class3A, indent=4))
    print(json.dumps(UNJF_ext_1_4_28_class3A, indent=4))
    print(json.dumps(UNJF_ext_3_8_24_class3A, indent=4))
    
    print("\nUNJEF Series:\n")
    
    
    
if __name__ == "__main__":
    main()
    