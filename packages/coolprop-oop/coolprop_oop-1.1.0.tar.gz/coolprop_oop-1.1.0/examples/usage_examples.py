#!/usr/bin/env python3
"""
CoolProp-OOP Usage Examples

This file demonstrates the usage of the CoolProp-OOP package for thermodynamic property calculations.
"""

from coolprop_oop import StateHA, StatePROPS

def example_humid_air_basic():
    """
    Basic example of using StateHA for humid air properties
    """
    print("\n=== Basic Humid Air Properties ===")
    
    # Create a state for humid air at 20°C, 1 atm, 50% RH
    state = StateHA()
    state.press = 101325    # Pressure in Pa
    state.tempc = 20        # Temperature in °C
    state.relhum = 0.5      # Relative humidity (0-1)
    
    # Access and print properties
    print(f"Temperature: {state.tempc:.2f}°C")
    print(f"Pressure: {state.press:.0f} Pa")
    print(f"Relative Humidity: {state.relhum * 100:.1f}%")
    print(f"Humidity Ratio: {state.humrat:.6f} kg/kg")
    print(f"Wet Bulb Temperature: {state.wetbulb - 273.15:.2f}°C")
    print(f"Dew Point: {state.dewpoint - 273.15:.2f}°C")
    print(f"Enthalpy: {state.enthalpy:.2f} J/kg")
    print(f"Entropy: {state.entropy:.2f} J/kg-K")
    print(f"Density: {state.density:.4f} kg/m³")
    print(f"Volume: {state.vol:.4f} m³/kg")
    print(f"Specific Heat Capacity: {state.cp:.2f} J/kg-K")

def example_humid_air_alternative_properties():
    """
    Example of using different combinations of properties to define a humid air state
    """
    print("\n=== Alternative Humid Air Property Combinations ===")
    
    # Create a state using wet bulb temperature instead of relative humidity
    state = StateHA()
    state.press = 101325        # Pressure in Pa
    state.tempc = 25            # Temperature in °C
    state.wetbulb = 273.15 + 18 # Wet bulb temperature in K
    
    print("State defined with temperature, pressure, and wet bulb temperature:")
    print(f"Temperature: {state.tempc:.2f}°C")
    print(f"Pressure: {state.press:.0f} Pa")
    print(f"Wet Bulb Temperature: {state.wetbulb - 273.15:.2f}°C")
    print(f"Calculated Relative Humidity: {state.relhum * 100:.1f}%")
    print(f"Calculated Humidity Ratio: {state.humrat:.6f} kg/kg")
    
    # Create a state using humidity ratio instead of relative humidity
    state2 = StateHA()
    state2.press = 101325  # Pressure in Pa
    state2.tempc = 25      # Temperature in °C
    state2.humrat = 0.010  # Humidity ratio in kg/kg
    
    print("\nState defined with temperature, pressure, and humidity ratio:")
    print(f"Temperature: {state2.tempc:.2f}°C")
    print(f"Pressure: {state2.press:.0f} Pa")
    print(f"Humidity Ratio: {state2.humrat:.6f} kg/kg")
    print(f"Calculated Relative Humidity: {state2.relhum * 100:.1f}%")
    
    # Create a state using dew point temperature
    state3 = StateHA()
    state3.press = 101325        # Pressure in Pa
    state3.tempc = 25            # Temperature in °C
    state3.dewpoint = 273.15 + 15 # Dew point temperature in K
    
    print("\nState defined with temperature, pressure, and dew point:")
    print(f"Temperature: {state3.tempc:.2f}°C")
    print(f"Pressure: {state3.press:.0f} Pa")
    print(f"Dew Point: {state3.dewpoint - 273.15:.2f}°C")
    print(f"Calculated Relative Humidity: {state3.relhum * 100:.1f}%")
    
    # Show which properties are constraining the state
    print(f"\nConstraints for the last state: {state3.constraints}")

def example_humid_air_error_handling():
    """
    Example of error handling and input validation in humid air calculations
    """
    print("\n=== Humid Air Error Handling and Validation ===")
    
    # Example of trying to set an invalid temperature (below absolute zero)
    try:
        state = StateHA()
        state.tempc = -300
    except ValueError as e:
        print(f"Error setting invalid temperature: {e}")
    
    # Example of trying to set an invalid relative humidity (greater than 1)
    try:
        state = StateHA()
        state.relhum = 1.5
    except ValueError as e:
        print(f"Error setting invalid relative humidity: {e}")
    
    # Example of trying to over-constrain the system
    try:
        state = StateHA()
        state.tempc = 25
        state.press = 101325
        state.relhum = 0.5
        # This would be a 4th constraint, which is not allowed
        state.wetbulb = 295
    except ValueError as e:
        print(f"Error over-constraining the system: {e}")
    
    # Example of setting inconsistent properties
    try:
        state = StateHA()
        state.tempc = 25
        state.press = 101325
        # Setting a dew point higher than dry bulb is physically impossible
        state.dewpoint = 303.15  # 30°C dew point, which is > 25°C dry bulb
    except ValueError as e:
        print(f"Error setting inconsistent properties: {e}")

def example_pure_fluid_basic():
    """
    Basic example of using StatePROPS for pure fluid properties
    """
    print("\n=== Basic Pure Fluid Properties (Water) ===")
    
    # Create a state for water at 100°C, 1 atm
    state = StatePROPS(fluid='Water')  # Set fluid first
    state.tempc = 100     # Temperature in °C
    state.press = 101325  # Pressure in Pa
    
    # Access and print properties
    print(f"Temperature: {state.tempc:.2f}°C")
    print(f"Pressure: {state.press:.0f} Pa")
    print(f"Density: {state.dens:.2f} kg/m³")
    print(f"Enthalpy: {state.enthalpy:.2f} J/kg")
    print(f"Entropy: {state.entropy:.2f} J/kg-K")
    print(f"Specific Heat Capacity (cp): {state.cp:.2f} J/kg-K")
    print(f"Specific Heat Capacity (cv): {state.cv:.2f} J/kg-K")
    
    # Check quality (None for single-phase states)
    quality = state.quality
    if quality is None:
        print("Quality: Not applicable (not in two-phase region)")
    else:
        print(f"Quality: {quality:.4f}")
    
    # Display state constraints information
    constraints = state.constraints
    print("\n--- State Information ---")
    print(f"Set properties: {', '.join(constraints['properties'])}")
    print(f"Fluid: {constraints['fluid']}")
    print(f"State is complete: {constraints['is_complete']}")
    print(f"Phase status: {constraints['status']}")
    print(f"CoolProp edition: {constraints['edition']}")

def example_refrigerant_properties():
    """
    Example of using StatePROPS for refrigerant properties
    """
    print("\n=== Refrigerant Properties (R134a) ===")
    
    # Create a state for R134a at 25°C, 10 bar
    r134a = StatePROPS(fluid='R134a')
    r134a.tempc = 25        # Temperature in °C
    r134a.press = 1000000   # Pressure in Pa (10 bar)
    
    # Access and print properties
    print(f"Temperature: {r134a.tempc:.2f}°C")
    print(f"Pressure: {r134a.press/100000:.2f} bar")
    print(f"Density: {r134a.dens:.2f} kg/m³")
    print(f"Enthalpy: {r134a.enthalpy:.2f} J/kg")
    print(f"Entropy: {r134a.entropy:.2f} J/kg-K")
    
    # Check quality
    quality = r134a.quality
    if quality is None:
        print("Quality: Not applicable (not in two-phase region)")
    else:
        print(f"Quality: {quality:.4f}")
    
    # Display state information
    constraints = r134a.constraints
    print(f"Phase status: {constraints['status']}")

def example_two_phase_properties():
    """
    Example of working with two-phase (saturated) conditions
    """
    print("\n=== Two-Phase Properties (Saturated Steam) ===")
    
    # Create a state for saturated steam (quality = 1)
    steam = StatePROPS(fluid='Water')
    steam.tempc = 100    # Temperature in °C
    steam.quality = 1    # Saturated vapor
    
    # Access and print properties
    print(f"Temperature: {steam.tempc:.2f}°C")
    print(f"Calculated Pressure: {steam.press:.0f} Pa")
    print(f"Density: {steam.dens:.4f} kg/m³")
    print(f"Enthalpy: {steam.enthalpy:.2f} J/kg")
    print(f"Quality: {steam.quality:.2f}")
    
    # Create a state for saturated liquid (quality = 0)
    water = StatePROPS(fluid='Water')
    water.tempc = 100    # Temperature in °C
    water.quality = 0    # Saturated liquid
    
    print("\nSaturated liquid water at same temperature:")
    print(f"Temperature: {water.tempc:.2f}°C")
    print(f"Calculated Pressure: {water.press:.0f} Pa")
    print(f"Density: {water.dens:.2f} kg/m³")
    print(f"Enthalpy: {water.enthalpy:.2f} J/kg")
    print(f"Quality: {water.quality:.2f}")
    
    # Calculate latent heat of vaporization
    latent_heat = steam.enthalpy - water.enthalpy
    print(f"\nLatent heat of vaporization: {latent_heat:.2f} J/kg")

def example_pure_fluid_error_handling():
    """
    Example of error handling in pure fluid calculations
    """
    print("\n=== Pure Fluid Error Handling and Validation ===")
    
    # Example of setting fluid after properties
    try:
        state = StatePROPS()
        state.tempc = 25      # Won't work - fluid not set
        state.press = 101325  # Won't work - fluid not set
    except ValueError as e:
        print(f"Error: {e}")
    
    # Example of over-constraining a pure fluid state
    try:
        state = StatePROPS(fluid='Water')
        state.tempc = 25
        state.press = 101325
        # Pure fluids only allow 2 properties to be set
        state.dens = 997
    except ValueError as e:
        print(f"Error over-constraining the system: {e}")
    
    # Example of setting inconsistent properties
    try:
        state = StatePROPS(fluid='R134a')
        state.tempc = 25
        # Setting quality > 0 at this temperature would be inconsistent with the phase diagram
        state.quality = 0.5
    except ValueError as e:
        print(f"Error setting inconsistent properties: {e}")

def run_all_examples():
    """Run all examples"""
    print("=== CoolProp-OOP Usage Examples ===")
    
    # Humid air examples
    example_humid_air_basic()
    example_humid_air_alternative_properties()
    example_humid_air_error_handling()
    
    # Pure fluid examples
    example_pure_fluid_basic()
    example_refrigerant_properties()
    example_two_phase_properties()
    example_pure_fluid_error_handling()
    
    print("\n=== All examples completed successfully! ===")

if __name__ == "__main__":
    run_all_examples() 