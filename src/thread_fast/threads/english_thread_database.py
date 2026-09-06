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

"""

#########################
# UNC Coarse Thread:
#########################

UNC_ext_3_4_10 = {
    "name": "Unified Thread Coarse Size 3/4, 10tpi",
    "units": "english: in",
    "basic_major_diameter": 0.75,
    "tpi": 9,  # threads per inch = threads / inch
    "pitch": 1.0/9.0,
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
