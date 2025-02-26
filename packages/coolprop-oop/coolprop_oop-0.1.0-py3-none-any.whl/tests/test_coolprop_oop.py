import unittest
from coolprop_oop import StateHA, StatePROPS

class TestStateHA(unittest.TestCase):
    def test_initialization(self):
        """Test that StateHA initializes correctly with properties."""
        state = StateHA(['P', 101325, 'T', 293.15, 'R', 0.5])
        self.assertAlmostEqual(state.tempc, 20.0, places=1)
        self.assertAlmostEqual(state.press, 101325.0, places=0)
        self.assertAlmostEqual(state.relhum, 0.5, places=2)
        
    def test_property_calculation(self):
        """Test that calculated properties are reasonable."""
        state = StateHA(['P', 101325, 'T', 293.15, 'R', 0.5])
        # Humidity ratio should be positive
        self.assertGreater(state.humrat, 0)
        # Wet bulb should be less than dry bulb for unsaturated air
        self.assertLess(state.wetbulb, state.tempk)
        # Dew point should be less than dry bulb for unsaturated air
        self.assertLess(state.dewpoint, state.tempk)

class TestStatePROPS(unittest.TestCase):
    def test_initialization(self):
        """Test that StatePROPS initializes correctly with properties."""
        state = StatePROPS(['P', 101325, 'T', 373.15, 'water'])
        self.assertAlmostEqual(state.tempc, 100.0, places=1)
        self.assertAlmostEqual(state.press, 101325.0, places=0)
        
    def test_property_calculation(self):
        """Test that calculated properties are reasonable."""
        state = StatePROPS(['P', 101325, 'T', 373.15, 'water'])
        # Density should be positive
        self.assertGreater(state.dens, 0)
        # Enthalpy should be positive for water at 100°C
        self.assertGreater(state.enthalpy, 0)
        # Specific heat should be positive
        self.assertGreater(state.cp, 0)

if __name__ == '__main__':
    unittest.main() 