"""
CoolProp-OOP: An object-oriented wrapper for CoolProp thermodynamic properties.

This package provides an intuitive, object-oriented interface to CoolProp's thermodynamic
property calculations for both humid air and pure fluids. It simplifies property access
and calculations through two main classes: StateHA for humid air properties and StatePROPS
for pure fluid properties.

Features:
    - Easy-to-use object-oriented interface
    - Automatic property calculation and caching
    - Support for both humid air and pure fluid calculations
    - Consistent unit system (SI units)

Example Usage:
    >>> from coolprop_oop import StateHA, StatePROPS
    
    # Humid Air Example (20°C, 1 atm, 50% RH)
    >>> state = StateHA(['P', 101325, 'T', 293.15, 'R', 0.5])
    >>> print(f"{state.tempc:.1f}°C, {state.relhum*100:.0f}% RH")
    20.0°C, 50% RH
    
    # Pure Fluid Example (Water at 100°C, 1 atm)
    >>> water = StatePROPS(['P', 101325, 'T', 373.15, 'water'])
    >>> print(f"{water.tempc:.1f}°C, {water.press/1e5:.1f} bar")
    100.0°C, 1.0 bar

For more examples, see the examples directory in the package repository.
"""

from .coolprop_oop import StateHA, StatePROPS

__all__ = ['StateHA', 'StatePROPS'] 