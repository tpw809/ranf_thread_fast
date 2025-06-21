# User Guides

## Safety Factors

Safety factors provide additional conservatism against uncertainty, usually associated with the applied load.
Values for safety factors will usually be provided by standards documents or program command media.

### Ultimate Safety Factor

Safety factor against ultimate failure (rupture).

A good starting safety factor for ultimate failure is: SF_u = 1.4

NASA-STD-5001 is an example of a structural factors of safety requirements document.

### Yield Safety Factor

Safety factor against yield (plastic deformation).

A good starting safety factor for yield failure is: SF_u = 1.2

NASA-STD-5001 is an example of a structural factors of safety requirements document.

### Separation Safety Factor

NASA-STD-5020B provides guidance on separation factor of safety.

SF_sep = 1.2

### Fitting Factor

NASA-STD-5020B provides guidance on separation factor of safety.

FF = 1.15


## Materials

A286

Inconel 718

CRES 300 series


### Components
-Fastener
-Nut or Nut Plate
-Insert
-Washers
-Clamped Parts
-Lubricants
-Coatings


### Material Properties

-Modulus of elasticity
-Coefficient of thermal expansion
-Tensile Yield Strength
-Tensile Ultimate Strength
-Shear Ultimate Strength
-Bearing (Contact) Strength



## Failure Modes and Margins of Safety

Margins of safety are often written for known failure modes such that a margin greater than 0.0 is acceptable.

Margins of safety are often written in the form of:

MS = (capability / application requirement) - 1
or
MS = (allowable / actual) - 1

indicating the capability is greater than the application requirement.
The application requirement typically is modified with safety factors to account for uncertainties and reduce the risk posture.
The capability is usually the minimum expected. 


Threaded Fastener failure modes include:
-joint separation or loss of adequate joint preload
-fastener yielding
-fastener rupture (ultimate failure)
-thread shear (fastener, nut, insert internal, insert external, parent internal)
-joint bearing
-bolt bearing
-shear tear out
-joint slip


## Preload

Most joints rely on preload to perform adequately.
The preload is a tension in the fastener and compression in the clamped parts.

The issue with preload is primarily with respect to installation and knowing what the actual preload is. 
Most joints cannot afford to implement direct preload measurement, so it must be controlled some other way which will have significant uncertainty.

See MIL-HDBK-60 in the references section.

Common means of installation to control preload include:
-torque
-turn of the nut / head
-bolt elongation
-ultrasonic measurement
-preload indicating washers

## Washers

Always use a washer unless there is a very good reason you can't.

The purpose of washers includes:
-protect the clamped part bearing surface
-control coefficient of friction between fastener head and bearing surface
-protect the radius joining the head and shank on the fastener
-provide a hard bearing surface for the head or nut


## Load Application Factor

The load application factor accounts for the effective stiffness that is loaded and unloaded in the fastener as external load is applied.

There is a geometric and stiffness based method for estimating load application factor.

TODO: show 3 extreme cases and compare goodness, show stiffness diagrams

