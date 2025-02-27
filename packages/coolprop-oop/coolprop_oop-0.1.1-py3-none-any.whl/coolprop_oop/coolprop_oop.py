from CoolProp.CoolProp import HAPropsSI, PropsSI

class StateHA:
    """
    A class representing the thermodynamic state of humid air.
    
    This class provides an object-oriented interface to CoolProp's HAPropsSI function
    for humid air properties. It automatically calculates and caches common properties
    for easy access.
    
    Attributes:
        tempk (float): Temperature in Kelvin
        tempc (float): Temperature in Celsius
        press (float): Pressure in Pa
        humrat (float): Humidity ratio in kg/kg
        wetbulb (float): Wet bulb temperature in K
        relhum (float): Relative humidity (0-1)
        vol (float): Specific volume in m³/kg
        enthalpy (float): Specific enthalpy in J/kg
        entropy (float): Specific entropy in J/kg-K
        dewpoint (float): Dew point temperature in K
        density (float): Density in kg/m³
        cp (float): Specific heat capacity at constant pressure in J/kg-K
    
    Example:
        >>> # Create state at 25°C, 1 atm, 60% RH
        >>> state = StateHA(['P', 101325, 'T', 298.15, 'R', 0.6])
        >>> print(f"Humidity ratio: {state.humrat:.4f} kg/kg")
        Humidity ratio: 0.0120 kg/kg
        >>> print(f"Dew point: {state.dewpoint-273.15:.1f}°C")
        Dew point: 16.7°C
    """
    
    def __init__(self, props=None):
        """
        Initialize a StateHA object for humid air properties.
        
        Args:
            props (list, optional): Property inputs for HAPropsSI in the format
                [prop1_name, prop1_value, prop2_name, prop2_value, prop3_name, prop3_value]
                where prop_name can be:
                - 'T': Temperature [K]
                - 'P': Pressure [Pa]
                - 'R': Relative humidity [-]
                - 'W': Humidity ratio [kg/kg]
                - 'B': Wet bulb temperature [K]
                - 'D': Dew point temperature [K]
                If provided, properties are calculated immediately.
        
        Example:
            >>> state = StateHA(['T', 293.15, 'P', 101325, 'R', 0.5])
        """
        self.props = None
        self.tempk = None
        self.tempc = None
        self.press = None
        self.humrat = None
        self.wetbulb = None
        self.relhum = None
        self.vol = None
        self.enthalpy = None
        self.entropy = None
        self.dewpoint = None
        self.density = None
        self.cp = None
        
        if props is not None:
            self.set(props)
    
    def set(self, props):
        """
        Set the properties of the StateHA object using the provided inputs.
        
        This method calculates all state properties based on the three input properties
        provided. It uses CoolProp's HAPropsSI function internally.
        
        Args:
            props (list): Property inputs for HAPropsSI in the format
                [prop1_name, prop1_value, prop2_name, prop2_value, prop3_name, prop3_value]
        
        Returns:
            StateHA: The current object for method chaining.
        
        Example:
            >>> state = StateHA()
            >>> state.set(['T', 293.15, 'P', 101325, 'R', 0.5])
            >>> print(f"{state.tempc:.1f}°C")
            20.0°C
        """
        self.props = props
        self.tempk = self.get_prop("T")
        self.tempc = self.tempk - 273.15
        self.press = self.get_prop("P")
        self.humrat = self.get_prop("W")
        self.wetbulb = self.get_prop("B")
        self.relhum = self.get_prop("R")
        self.vol = self.get_prop("V")
        self.enthalpy = self.get_prop("H")
        self.entropy = self.get_prop("S")
        self.dewpoint = self.get_prop("D")
        self.density = 1/self.vol
        self.cp = self.get_prop("C")
        
        return self
    
    def get_prop(self, prop):
        """
        Get a specific property using HAPropsSI.
        
        Args:
            prop (str): The property to retrieve. Valid options include:
                - 'T': Temperature [K]
                - 'P': Pressure [Pa]
                - 'W': Humidity ratio [kg/kg]
                - 'R': Relative humidity [-]
                - 'B': Wet bulb temperature [K]
                - 'D': Dew point temperature [K]
                - 'H': Specific enthalpy [J/kg]
                - 'S': Specific entropy [J/kg-K]
                - 'V': Specific volume [m³/kg]
                - 'C': Specific heat capacity [J/kg-K]
            
        Returns:
            float: The value of the requested property.
        
        Example:
            >>> state = StateHA(['T', 293.15, 'P', 101325, 'R', 0.5])
            >>> h = state.get_prop('H')  # Get specific enthalpy
        """
        return HAPropsSI(prop, *self.props)

class StatePROPS:
    """
    A class representing the thermodynamic state of a pure fluid.
    
    This class provides an object-oriented interface to CoolProp's PropsSI function
    for pure fluid properties. It automatically calculates and caches common properties
    for easy access.
    
    Attributes:
        tempk (float): Temperature in Kelvin
        tempc (float): Temperature in Celsius
        press (float): Pressure in Pa
        dens (float): Density in kg/m³
        enthalpy (float): Specific enthalpy in J/kg
        entropy (float): Specific entropy in J/kg-K
        quality (float): Vapor quality (0-1), or None if not in two-phase region
        cp (float): Specific heat capacity at constant pressure in J/kg-K
        cv (float): Specific heat capacity at constant volume in J/kg-K
    
    Example:
        >>> # Create state for water at 100°C, 1 atm
        >>> water = StatePROPS(['P', 101325, 'T', 373.15, 'water'])
        >>> print(f"Density: {water.dens:.1f} kg/m³")
        Density: 0.6 kg/m³
        >>> # Create state for R134a at 25°C, 10 bar
        >>> r134a = StatePROPS(['P', 1e6, 'T', 298.15, 'R134a'])
        >>> print(f"Density: {r134a.dens:.1f} kg/m³")
        Density: 1209.0 kg/m³
    """
    
    def __init__(self, props=None):
        """
        Initialize a StatePROPS object for pure fluid properties.
        
        Args:
            props (list, optional): Property inputs for PropsSI in the format
                [prop1_name, prop1_value, prop2_name, prop2_value, fluid_name]
                where prop_name can be:
                - 'T': Temperature [K]
                - 'P': Pressure [Pa]
                - 'D': Density [kg/m³]
                - 'H': Specific enthalpy [J/kg]
                - 'S': Specific entropy [J/kg-K]
                - 'Q': Vapor quality [-]
                If provided, properties are calculated immediately.
        
        Example:
            >>> state = StatePROPS(['T', 373.15, 'P', 101325, 'water'])
        """
        self.props = None
        self.tempk = None
        self.tempc = None
        self.press = None
        self.dens = None
        self.enthalpy = None
        self.entropy = None
        self.quality = None
        self.cp = None
        self.cv = None
        
        if props is not None:
            self.set(props)
    
    def set(self, props):
        """
        Set the properties of the StatePROPS object using the provided inputs.
        
        This method calculates all state properties based on the two input properties
        and fluid name provided. It uses CoolProp's PropsSI function internally.
        
        Args:
            props (list): Property inputs for PropsSI in the format
                [prop1_name, prop1_value, prop2_name, prop2_value, fluid_name]
        
        Returns:
            StatePROPS: The current object for method chaining.
        
        Example:
            >>> state = StatePROPS()
            >>> state.set(['T', 373.15, 'P', 101325, 'water'])
            >>> print(f"{state.tempc:.1f}°C")
            100.0°C
        """
        self.props = props
        self.tempk = self.get_prop("T")
        self.tempc = self.tempk - 273.15
        self.press = self.get_prop("P")
        self.dens = self.get_prop("D")
        self.enthalpy = self.get_prop("H")
        self.entropy = self.get_prop("S")
        self.quality = self.get_prop("Q")
        self.cp = self.get_prop("C")
        self.cv = self.get_prop("O")
        
        return self
    
    def get_prop(self, prop):
        """
        Get a specific property using PropsSI.
        
        Args:
            prop (str): The property to retrieve. Valid options include:
                - 'T': Temperature [K]
                - 'P': Pressure [Pa]
                - 'D': Density [kg/m³]
                - 'H': Specific enthalpy [J/kg]
                - 'S': Specific entropy [J/kg-K]
                - 'Q': Vapor quality [-]
                - 'C': Specific heat capacity at constant pressure [J/kg-K]
                - 'O': Specific heat capacity at constant volume [J/kg-K]
            
        Returns:
            float: The value of the requested property.
        
        Example:
            >>> state = StatePROPS(['T', 373.15, 'P', 101325, 'water'])
            >>> h = state.get_prop('H')  # Get specific enthalpy
        """
        return PropsSI(prop, *self.props) 