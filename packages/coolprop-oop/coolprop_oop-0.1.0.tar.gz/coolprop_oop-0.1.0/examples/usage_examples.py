#!/usr/bin/env python3

from coolprop_oop import StateHA, StatePROPS

def test_humid_air():
    print("\n=== Testing Humid Air Properties ===")
    # Create a state for humid air at 20°C, 1 atm, 50% RH
    state = StateHA(['P', 101325, 'T', 293.15, 'R', 0.5])
    
    # Access and print properties
    print(f"Temperature: {state.tempc:.2f}°C")
    print(f"Pressure: {state.press:.0f} Pa")
    print(f"Relative Humidity: {state.relhum * 100:.1f}%")
    print(f"Humidity Ratio: {state.humrat:.6f} kg/kg")
    print(f"Wet Bulb Temperature: {state.wetbulb - 273.15:.2f}°C")
    print(f"Dew Point: {state.dewpoint - 273.15:.2f}°C")
    print(f"Enthalpy: {state.enthalpy:.2f} J/kg")
    print(f"Density: {state.density:.4f} kg/m³")

def test_pure_fluid():
    print("\n=== Testing Pure Fluid Properties ===")
    # Create a state for water at 100°C, 1 atm
    state = StatePROPS(['P', 101325, 'T', 373.15, 'water'])
    
    # Access and print properties
    print(f"Temperature: {state.tempc:.2f}°C")
    print(f"Pressure: {state.press:.0f} Pa")
    print(f"Density: {state.dens:.2f} kg/m³")
    print(f"Enthalpy: {state.enthalpy:.2f} J/kg")
    print(f"Entropy: {state.entropy:.2f} J/kg-K")
    print(f"Specific Heat Capacity (cp): {state.cp:.2f} J/kg-K")
    
    # Test refrigerant properties (R134a at 25°C, 10 bar)
    print("\n--- Testing Refrigerant (R134a) ---")
    r134a = StatePROPS(['P', 1000000, 'T', 298.15, 'R134a'])
    print(f"Temperature: {r134a.tempc:.2f}°C")
    print(f"Pressure: {r134a.press/100000:.2f} bar")
    print(f"Density: {r134a.dens:.2f} kg/m³")
    print(f"Quality: {r134a.quality}")

if __name__ == "__main__":
    print("Testing CoolProp-OOP Package")
    test_humid_air()
    test_pure_fluid()
    print("\nAll tests completed successfully!") 