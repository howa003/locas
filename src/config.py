
'''
This file contains the configuration for the project.
'''

LOG_PERCENTAGE = 1  # At what percentage of the total number of steps should a log message be printed.

STEF_BOLT_CONST = 5.670374419 * 10 ** -8  # Stefan-Boltzmann constant

RADIATION_IN = 1  # Should radiation  be taken into account for the inner surface? 0 no; 1 yes;
RADIATION_OUT = 1  # Should radiation be taken into account for the outer surface? 0 no; 1 yes;

RADIAL = 1  # Should heat conduction be calculated using polar coordinates? 0 no; 1 yes; 0 means classic 1D conduction

PHASE_ENDS_MAX = (300, 1800, 7200, 86400)  # Maximum lengths of LOCA phases in seconds

CONCRETE_CONDUCTIVITY_LIMIT = 1  # Which equation for concrete conductivity should be used? 0 lower limit; 1 upper limit

AIR_FLOW = 1  # What type of air flow should be used? 0 only laminar; 1 laminar and turbulent

