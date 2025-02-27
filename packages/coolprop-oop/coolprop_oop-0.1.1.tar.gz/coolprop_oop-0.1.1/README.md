# CoolProp-OOP

An object-oriented wrapper for CoolProp thermodynamic properties.

## Installation

```bash
pip install coolprop-oop
```

## Usage

### Humid Air Properties

```python
from coolprop_oop import StateHA

# Create a state for humid air
state = StateHA(['P', 101325, 'T', 293.15, 'R', 0.5])

# Access properties
print(f"Temperature: {state.tempc}°C")
print(f"Relative Humidity: {state.relhum * 100}%")
print(f"Humidity Ratio: {state.humrat} kg/kg")
```

### Pure Fluid Properties

```python
from coolprop_oop import StatePROPS

# Create a state for water
state = StatePROPS(['P', 101325, 'T', 373.15, 'water'])

# Access properties
print(f"Temperature: {state.tempc}°C")
print(f"Pressure: {state.press} Pa")
print(f"Density: {state.dens} kg/m³")
```

## License

MIT 