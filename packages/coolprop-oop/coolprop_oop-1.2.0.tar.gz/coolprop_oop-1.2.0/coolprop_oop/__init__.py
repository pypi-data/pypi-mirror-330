"""
CoolProp-OOP: An object-oriented wrapper for CoolProp thermodynamic properties.

This package provides an intuitive, object-oriented interface to CoolProp's thermodynamic
property calculations for both humid air and pure fluids. It simplifies property access
and calculations through two main classes: StateHA for humid air properties and StatePROPS
for pure fluid properties.

Features:
    - Object-oriented interface with property-based getters and setters
    - Automatic property validation to prevent physically impossible states
    - State constraint management to prevent overconstraining the system
    - All thermodynamic properties are directly settable (enthalpy, entropy, viscosity, etc.)
    - Automatic property calculation and caching for better performance
    - Support for both humid air and pure fluid calculations
    - Consistent unit system (SI units)

Example Usage:
    >>> from coolprop_oop import StateHA, StatePROPS
    
    # Humid Air Example (20°C, 1 atm, 50% RH)
    >>> state = StateHA()
    >>> state.tempc = 20        # Temperature in °C
    >>> state.press = 101325    # Pressure in Pa
    >>> state.relhum = 0.5      # Relative humidity (0-1)
    >>> print(f"{state.tempc:.1f}°C, {state.relhum*100:.0f}% RH, w={state.humrat:.6f} kg/kg")
    20.0°C, 50% RH, w=0.007295 kg/kg
    
    # Pure Fluid Example (Water at 100°C, 1 atm)
    >>> water = StatePROPS(fluid='Water') 
    >>> water.tempc = 100       # Temperature in °C
    >>> water.press = 101325    # Pressure in Pa
    >>> print(f"{water.tempc:.1f}°C, {water.press/1e5:.2f} bar, ρ={water.dens:.1f} kg/m³")
    100.0°C, 1.01 bar, ρ=958.4 kg/m³

    # Setting derived properties directly
    >>> water2 = StatePROPS(fluid='Water')
    >>> water2.press = 101325   # Pressure in Pa
    >>> water2.enthalpy = 2000000  # Enthalpy in J/kg
    >>> print(f"Temperature: {water2.tempc:.1f}°C, Quality: {water2.quality:.3f}")

For more examples, see the examples directory in the package repository.
"""

from .coolprop_oop import StateHA, StatePROPS

__version__ = "1.2.0"
__all__ = ['StateHA', 'StatePROPS'] 