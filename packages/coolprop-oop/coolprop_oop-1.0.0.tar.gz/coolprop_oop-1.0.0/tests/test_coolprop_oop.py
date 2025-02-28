"""
Test suite for CoolProp OOP wrapper classes.

This module contains comprehensive tests for both StateHA (Humid Air) and 
StatePROPS (Pure Fluid) property calculators.

Tests include:
- Basic initialization and property calculation
- Input validation for all properties
- Under/over constraining behavior
- Invalid value handling
- Property updates and dependencies
- Error message formatting
"""

from coolprop_oop import StateHA, StatePROPS
import unittest
import warnings


class TestStateHA(unittest.TestCase):
    """Test cases for humid air properties calculator."""

    def setUp(self):
        # Suppress deprecation warnings during tests
        warnings.filterwarnings('ignore', category=DeprecationWarning)

    def test_initialization(self):
        """Verify that StateHA initializes correctly with properties."""
        state = StateHA()
        state.press = 101325
        state.tempk = 293.15
        state.relhum = 0.5
        self.assertAlmostEqual(state.relhum, 0.5, places=2)
        self.assertAlmostEqual(state.tempk, 293.15, places=2)
        self.assertAlmostEqual(state.press, 101325, places=0)

    def test_input_validation(self):
        """Test input validation for all properties."""
        state = StateHA()
        
        # Test temperature validation
        with self.assertRaisesRegex(ValueError, "must be above absolute zero"):
            state.tempk = -1
        with self.assertRaisesRegex(ValueError, "exceeding reasonable range"):
            state.tempk = 500  # > 200°C
            
        # Test pressure validation
        with self.assertRaisesRegex(ValueError, "must be positive"):
            state.press = -101325
        with self.assertRaisesRegex(ValueError, "below reasonable range"):
            state.press = 500  # < 1 kPa
        with self.assertRaisesRegex(ValueError, "exceeding reasonable range"):
            state.press = 1e8  # > 100 bar
            
        # Test relative humidity validation
        with self.assertRaisesRegex(ValueError, "cannot be negative"):
            state.relhum = -0.1
        with self.assertRaisesRegex(ValueError, "cannot exceed 1"):
            state.relhum = 1.5
            
        # Test humidity ratio validation
        with self.assertRaisesRegex(ValueError, "cannot be negative"):
            state.humrat = -0.001
        with self.assertRaisesRegex(ValueError, "exceeding reasonable range"):
            state.humrat = 1.5  # > 1 kg/kg
            
        # Test type validation
        with self.assertRaisesRegex(TypeError, "must be a number"):
            state.tempk = "293.15"

    def test_error_messages(self):
        """Test error messages when setting invalid states."""
        state = StateHA()
        state.press = 101325
        state.tempk = 293.15
        state.relhum = 0.5
        
        # Try to set a fourth constraint
        with self.assertRaisesRegex(ValueError, "Cannot set humrat - system is already fully constrained"):
            state.humrat = 0.01
            
        # Try to update with invalid value
        with self.assertRaisesRegex(ValueError, "Please validate all set properties"):
            state.relhum = 1.5

    def test_property_calculation(self):
        """Verify that calculated properties are physically reasonable."""
        state = StateHA()
        state.press = 101325
        state.tempk = 293.15
        state.relhum = 0.5
        # Wet bulb should be lower than dry bulb
        self.assertLess(state.wetbulb, state.tempk)
        # Humidity ratio should be positive
        self.assertGreater(state.humrat, 0)
        # Enthalpy should be reasonable for room temperature
        self.assertGreater(state.enthalpy, 20000)
        self.assertLess(state.enthalpy, 100000)

    def test_underconstraining(self):
        """Verify behavior when state is underconstrained."""
        state = StateHA()
        # No constraints
        self.assertIsNone(state.enthalpy)
        
        # One constraint
        state.tempk = 293.15
        self.assertIsNone(state.enthalpy)
        self.assertEqual(len(state._constraints_set), 1)
        
        # Two constraints
        state.press = 101325
        self.assertIsNone(state.enthalpy)
        self.assertEqual(len(state._constraints_set), 2)

    def test_property_updates(self):
        """Verify property dependencies when updating values."""
        state = StateHA()
        state.tempk = 293.15
        state.press = 101325
        state.relhum = 0.5
        
        # Store initial values
        initial_humrat = state.humrat
        initial_enthalpy = state.enthalpy
        
        # Update temperature and check that dependent properties change
        state.tempk = 303.15
        self.assertNotEqual(state.humrat, initial_humrat)
        self.assertNotEqual(state.enthalpy, initial_enthalpy)


class TestStatePROPS(unittest.TestCase):
    """Test cases for pure fluid properties calculator."""

    def setUp(self):
        warnings.filterwarnings('ignore', category=DeprecationWarning)
        self.state = StatePROPS()
        self.state.fluid = 'Water'

    def test_initialization(self):
        """Verify that StatePROPS initializes correctly."""
        self.state.press = 101325
        self.state.tempk = 293.15
        self.assertAlmostEqual(self.state.tempk, 293.15)
        self.assertAlmostEqual(self.state.press, 101325)

    def test_input_validation(self):
        """Test input validation for all properties."""
        # Test temperature validation
        with self.assertRaisesRegex(ValueError, "must be above absolute zero"):
            self.state.tempk = -1
        with self.assertRaisesRegex(ValueError, "exceeding reasonable range"):
            self.state.tempk = 2500  # > 1726.85°C
            
        # Test pressure validation
        with self.assertRaisesRegex(ValueError, "must be positive"):
            self.state.press = -101325
        with self.assertRaisesRegex(ValueError, "exceeding reasonable range"):
            self.state.press = 2e9  # > 10000 bar
            
        # Test density validation
        with self.assertRaisesRegex(ValueError, "must be positive"):
            self.state.dens = -1000
        with self.assertRaisesRegex(ValueError, "exceeding reasonable range"):
            self.state.dens = 2e5  # > 100000 kg/m³
            
        # Test quality validation
        with self.assertRaisesRegex(ValueError, "must be between 0 and 1"):
            self.state.quality = -0.1
        with self.assertRaisesRegex(ValueError, "must be between 0 and 1"):
            self.state.quality = 1.1
            
        # Test type validation
        with self.assertRaisesRegex(TypeError, "must be a number"):
            self.state.tempk = "293.15"

    def test_error_messages(self):
        """Test error messages when setting invalid states."""
        self.state.press = 101325
        self.state.tempk = 293.15
        
        # Try to set a third constraint
        with self.assertRaisesRegex(ValueError, "system is already fully constrained with 2 properties"):
            self.state.dens = 1000
            
        # Try to update with invalid value
        with self.assertRaisesRegex(ValueError, "Please validate all set properties"):
            self.state.press = -101325

    def test_property_calculation(self):
        """Verify that calculated properties are physically reasonable."""
        self.state.press = 101325
        self.state.tempk = 293.15
        
        # Test calculated properties
        self.assertIsNotNone(self.state.enthalpy)
        self.assertGreater(self.state.enthalpy, 0)
        self.assertIsNotNone(self.state.cp)
        self.assertGreater(self.state.cp, 0)
        self.assertIsNotNone(self.state.dens)
        self.assertGreater(self.state.dens, 0)
        
        # Quality should be None outside two-phase region
        self.assertAlmostEqual(self.state.quality, -1.0, places = 1)

    def test_fluid_validation(self):
        """Test fluid name validation."""
        with self.assertRaisesRegex(TypeError, "fluid must be a string"):
            self.state.fluid = 123

    def test_unsettable_properties(self):
        """Test that calculated properties cannot be set directly."""
        with self.assertRaisesRegex(AttributeError, "cannot be set directly"):
            self.state.enthalpy = 1000
        with self.assertRaisesRegex(AttributeError, "cannot be set directly"):
            self.state.entropy = 1000
        with self.assertRaisesRegex(AttributeError, "cannot be set directly"):
            self.state.cp = 1000
        with self.assertRaisesRegex(AttributeError, "cannot be set directly"):
            self.state.cv = 1000


if __name__ == '__main__':
    unittest.main() 