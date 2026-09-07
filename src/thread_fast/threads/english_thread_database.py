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
    "name": "Unified Thread Coarse Size 3/4, 10tpi",
    "units": "english: in",
    "basic_major_diameter": 0.75,
    "tpi": 10,  # threads per inch = threads / inch
    "pitch": 1.0/10.0,
    "external": True,
}

UNC_ext_7_8_9 = {
    "name": "Unified Thread Coarse Size 7/8, 9tpi",
    "units": "english: in",
    "basic_major_diameter": 0.875,
    "tpi": 9,  # threads per inch = threads / inch
    "pitch": 1.0/9.0,
    "external": True,
}

#########################
# UNF Fine Thread:
#########################

UNF_ext_3_4_16 = {
    "name": "Unified Thread Fine Size 3/4, 16tpi",
    "units": "english: in",
    "basic_major_diameter": 0.75,
    "tpi": 16,  # threads per inch = threads / inch
    "pitch": 1.0/16.0,
    "external": True,
}


#########################
# UNJF Fine Thread, Controlled Root:
#########################

# from MIL-S-8879C, Table III, pg 20:
UNJF_ext_1_4_28_class3A = {
    "name": "Unified Thread Fine Size 1/4, 28tpi",
    "units": "english: in",
    "basic_major_diameter": 0.25,
    "tpi": 28,  # threads per inch = threads / inch
    "pitch": 1.0/28.0,
    "external": True,
    "class": "3A",
    "series": "UNJF",
    "min_major_diameter": 0.2,
    "max_major_diameter": 0.2,
    "min_pitch_diameter": 0.2,
    "max_pitch_diameter": 0.2,
    "min_minor_diameter": 0.2,
    "max_minor_diameter": 0.2,
    "min_root_radius": 0.00,
    "max_root_radius": 0.00,
}

# from MIL-S-8879C, Table III, pg 20:
UNJF_ext_3_8_24_class3A = {
    "name": "Unified Thread Fine Size 3/8, 24tpi",
    "units": "english: in",
    "basic_major_diameter": 0.375,
    "tpi": 24,  # threads per inch = threads / inch
    "pitch": 1.0/24.0,
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

# from MIL-S-8879C, Table III, pg 20:
UNJF_ext_7_8_14_class3A = {
    "name": "Unified Thread Fine Size 7/8, 14tpi",
    "units": "english: in",
    "basic_major_diameter": 0.875,
    "tpi": 14,  # threads per inch = threads / inch
    "pitch": 1.0/14.0,
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
# UNF Extra Fine Thread:
#########################

UNEF_ext_12_32 = {
    "name": "Unified Thread Extra Fine Size #12, 32tpi",
    "units": "english: in",
    "basic_major_diameter": 0.2160,
    "tpi": 32,  # threads per inch = threads / inch
    "pitch": 1.0/32.0,
    "external": True,
}

UNEF_ext_1_4_32 = {
    "name": "Unified Thread Extra Fine Size 1/4, 32tpi",
    "units": "english: in",
    "basic_major_diameter": 0.25,
    "tpi": 32,  # threads per inch = threads / inch
    "pitch": 1.0/32.0,
    "external": True,
}
