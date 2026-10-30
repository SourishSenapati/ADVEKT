"""
ADVEKT: The Autonomous Multi-Discipline Chemical & Mechanical Engineering CAE Suite
with Native RAEBYES Circuit Breaking.

The Invariant Velocity Field of Continuous Matter.
Lead Chemical & Process Engineer: Sourish Senapati
"""

import sys
from agentic_chemeng import *  # noqa: F401, F403
import agentic_chemeng as _backend

__version__ = "1.0.0"
__author__ = "Sourish Senapati"
__copyright__ = "Copyright (c) 2026 Sourish Senapati. All Rights Reserved."
__license__ = "ADVEKT Commercial & Intellectual Property Protection License v1.0"

# Expose core modules directly under advekt namespace
import agentic_chemeng.cli as cli
import agentic_chemeng.mcp as mcp
import agentic_chemeng.thermo as thermo
import agentic_chemeng.hydraulics as hydraulics
import agentic_chemeng.thermal as thermal
import agentic_chemeng.pressure_vessel as pressure_vessel
import agentic_chemeng.solidworks as solidworks
import agentic_chemeng.aspen_plus as aspen_plus
import agentic_chemeng.aspen_hysys as aspen_hysys
import agentic_chemeng.autocad as autocad
import agentic_chemeng.dwsim as dwsim
import agentic_chemeng.chemcad as chemcad
import agentic_chemeng.proii as proii
import agentic_chemeng.cantera as cantera
import agentic_chemeng.unisim as unisim
import agentic_chemeng.gproms as gproms
import agentic_chemeng.comsol as comsol
import agentic_chemeng.ansys as ansys
import agentic_chemeng.raebyes as raebyes
import agentic_chemeng.resilience as resilience

