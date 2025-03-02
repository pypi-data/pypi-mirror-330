# CoolProp-OOP

An object-oriented wrapper for [CoolProp](http://www.coolprop.org/) thermodynamic properties. This library provides an intuitive, Pythonic interface to CoolProp's functionality for both humid air and pure fluid property calculations.

## Features

- **Object-oriented interface** to CoolProp's functionality
- **Property validation** to prevent physically impossible states
- **All thermodynamic properties are directly settable** - enthalpy, entropy, and any other property can be used as a constraint
- **Automatic caching** of calculated properties for better performance
- Support for both **Humid Air** (`StateHA`) and **Pure Fluids** (`StatePROPS`)
- Comprehensive **state validation** with helpful error messages
- **Fully Pythonic API** with property-based getters and setters

## Installation

```bash
pip install coolprop-oop
```

## Usage

### Humid Air Properties

```python
from coolprop_oop import StateHA

# Create a state for humid air (OOP style, recommended)
state = StateHA()
state.tempc = 20      # Temperature in °C
state.press = 101325  # Pressure in Pa
state.relhum = 0.5    # Relative humidity (0-1)

# Access properties
print(f"Temperature: {state.tempc:.1f}°C")
print(f"Relative Humidity: {state.relhum * 100:.0f}%")
print(f"Humidity Ratio: {state.humrat:.6f} kg/kg")
print(f"Dew Point: {state.dewpoint - 273.15:.1f}°C")
print(f"Enthalpy: {state.enthalpy:.1f} J/kg")
print(f"Density: {state.density:.4f} kg/m³")

# Check which properties are currently constraining the state
print(f"Constraints: {state.constraints}")  # ['press', 'relhum', 'tempc']

# You can also set properties like enthalpy directly
state2 = StateHA()
state2.press = 101325   # Pressure in Pa
state2.relhum = 0.7     # Relative humidity (0-1)
state2.enthalpy = 50000 # Enthalpy in J/kg
print(f"Temperature from enthalpy: {state2.tempc:.1f}°C")
```

### Pure Fluid Properties

```python
from coolprop_oop import StatePROPS

# Create a state for water (OOP style, recommended)
state = StatePROPS(fluid='Water')  # Set fluid first
state.tempc = 100     # Temperature in °C
state.press = 101325  # Pressure in Pa

# Access properties
print(f"Temperature: {state.tempc:.1f}°C")
print(f"Pressure: {state.press/1000:.2f} kPa")
print(f"Density: {state.dens:.2f} kg/m³")
print(f"Enthalpy: {state.enthalpy:.1f} J/kg")
print(f"Quality: {state.quality}")  # None if not in two-phase region

# Get extensive state information
constraints = state.constraints
print(f"Fluid state: {constraints['status']}")  # e.g., 'liquid', 'gas', 'two_phase'
print(f"Set properties: {', '.join(constraints['properties'])}")

# You can also define state using enthalpy and pressure
state2 = StatePROPS(fluid='R134a')
state2.press = 500000   # Pressure in Pa
state2.enthalpy = 420000 # Enthalpy in J/kg
print(f"Temperature: {state2.tempc:.1f}°C")
print(f"Quality: {state2.quality}")  # Vapor quality if in two-phase region
```

## Error Handling and Validation

The library automatically validates inputs to prevent physically impossible states:

```python
try:
    state = StateHA()
    state.tempc = -300  # Below absolute zero
except ValueError as e:
    print(f"Error: {e}")  # "Error: Temperature cannot be below absolute zero"

# The library lets CoolProp perform advanced state validation
try:
    state = StatePROPS(fluid='Water')
    state.tempc = 25
    # Try to set incompatible properties - CoolProp will reject this
    state.entropy = 10000
except ValueError as e:
    print(f"Error: {e}")
```

## Documentation

For more examples and detailed API documentation, see the examples directory in the GitHub repository.

## License

MIT 