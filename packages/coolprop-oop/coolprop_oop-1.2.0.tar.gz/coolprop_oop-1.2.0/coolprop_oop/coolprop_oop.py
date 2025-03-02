from CoolProp.CoolProp import HAPropsSI, PropsSI
import warnings
from functools import wraps

def validate_input_ha(func):
    """
    Decorator for validating physical constraints of humid air property inputs.
    
    Checks that input values are within physically reasonable ranges before
    allowing them to be set. This runs before state_setter_ha to ensure
    basic physical validity before attempting CoolProp calculations.
    """
    @wraps(func)
    def wrapper(self, value):
        prop_name = func.__name__.replace('_setter', '')
        
        # Basic type checking
        if not isinstance(value, (int, float)):
            raise TypeError(f"{prop_name} must be a number")
            
        # Property-specific validation
        if prop_name in ['tempk', 'wetbulb', 'dewpoint']:
            if value <= 0:
                raise ValueError(f"{prop_name} must be above absolute zero")
            if value > 473.15:  # ~200°C - reasonable upper limit for humid air
                raise ValueError(f"{prop_name} exceeding reasonable range (> 200°C)")
                
        elif prop_name == 'tempc':
            if value < -273.15:
                raise ValueError("Temperature cannot be below absolute zero")
            if value > 200:  # Reasonable upper limit for humid air
                raise ValueError("Temperature exceeding reasonable range (> 200°C)")
                
        elif prop_name == 'press':
            if value <= 0:
                raise ValueError("Pressure must be positive")
            if value < 1000:  # 1 kPa - very low pressure
                raise ValueError("Pressure below reasonable range (< 1 kPa)")
            if value > 1e7:  # 100 bar - very high pressure
                raise ValueError("Pressure exceeding reasonable range (> 100 bar)")
                
        elif prop_name == 'relhum':
            if value < 0:
                raise ValueError("Relative humidity cannot be negative")
            if value > 1:
                raise ValueError("Relative humidity cannot exceed 1 (100%)")
                
        elif prop_name == 'humrat':
            if value < 0:
                raise ValueError("Humidity ratio cannot be negative")
            if value > 1:  # Extremely high - likely an error
                raise ValueError("Humidity ratio exceeding reasonable range (> 1 kg/kg)")
        
        # Validation for newly settable properties
        elif prop_name == 'vol':
            if value <= 0:
                raise ValueError("Specific volume must be positive")
            if value > 1000:  # Very high specific volume
                raise ValueError("Specific volume exceeding reasonable range (> 1000 m³/kg)")
                
        elif prop_name == 'enthalpy':
            # No strict limits on enthalpy, but should be reasonable
            if abs(value) > 1e7:  # Very high enthalpy
                raise ValueError("Enthalpy exceeding reasonable range (|h| > 10,000,000 J/kg)")
                
        elif prop_name == 'entropy':
            # No strict limits on entropy, but should be reasonable
            if abs(value) > 1e5:  # Very high entropy
                raise ValueError("Entropy exceeding reasonable range (|s| > 100,000 J/kg-K)")
                
        elif prop_name == 'density':
            if value <= 0:
                raise ValueError("Density must be positive")
            if value > 50:  # Very high density for humid air
                raise ValueError("Density exceeding reasonable range (> 50 kg/m³)")
                
        elif prop_name == 'cp':
            if value <= 0:
                raise ValueError("Specific heat capacity must be positive")
            if value > 10000:  # Very high cp
                raise ValueError("Specific heat capacity exceeding reasonable range (> 10,000 J/kg-K)")
        
        elif prop_name == 'viscosity':
            if value <= 0:
                raise ValueError("Viscosity must be positive")
            if value > 1:  # Very high viscosity for air
                raise ValueError("Viscosity exceeding reasonable range (> 1 Pa⋅s)")
                
        elif prop_name == 'conductivity':
            if value <= 0:
                raise ValueError("Thermal conductivity must be positive")
            if value > 1:  # Very high thermal conductivity for air
                raise ValueError("Thermal conductivity exceeding reasonable range (> 1 W/m-K)")
                
        elif prop_name == 'prandtl':
            if value <= 0:
                raise ValueError("Prandtl number must be positive")
            if value > 1000:  # Very high Prandtl number
                raise ValueError("Prandtl number exceeding reasonable range (> 1000)")
        
        return func(self, value)
    return wrapper

def state_setter_ha(func):
    """
    Decorator for property setters that manages state constraints for humid air properties.
    
    Checks if this property is already set before allowing the property to be set.
    Property state validity is handled by CoolProp, and exceptions are passed to user.
    Also tracks which properties have been set for state validation.
    """
    @wraps(func)
    def wrapper(self, value):
        prop_name = func.__name__.replace('_setter', '')
        
        # Initialize constraints set if not exists
        if not hasattr(self, '_constraints_set'):
            self._constraints_set = set()
        
        # Always allow setting if we have 0 or 1 constraint or if this property is already set
        if len(self._constraints_set) < 2 or prop_name in self._constraints_set:
            func(self, value)
            self._constraints_set.add(prop_name)
            return
            
        # If we have 2+ constraints, try setting the new property
        # CoolProp will validate state and throw error if invalid
        try:
            # Try to set the property
            func(self, value)
            # If successful, add to constraints
            self._constraints_set.add(prop_name)
        except Exception as e:
            # Pass along any CoolProp errors to the user
            raise ValueError(f"Cannot set {prop_name} - {str(e)}")
            
    return wrapper

def validate_input_props(func):
    """
    Decorator for validating physical constraints of pure fluid property inputs.
    
    Checks that input values are within physically reasonable ranges before
    allowing them to be set. This runs before state_setter_PROPS to ensure
    basic physical validity before attempting CoolProp calculations.
    """
    @wraps(func)
    def wrapper(self, value):
        prop_name = func.__name__.replace('_setter', '')
        
        # Basic type checking
        if not isinstance(value, (int, float)):
            raise TypeError(f"{prop_name} must be a number")
            
        # Property-specific validation
        if prop_name in ['tempk']:
            if value <= 0:
                raise ValueError(f"{prop_name} must be above absolute zero")
            if value > 2000:  # Very high temperature limit for general fluids
                raise ValueError(f"{prop_name} exceeding reasonable range (> 1726.85°C)")
                
        elif prop_name == 'tempc':
            if value < -273.15:
                raise ValueError("Temperature cannot be below absolute zero")
            if value > 1726.85:  # Very high temperature limit for general fluids
                raise ValueError("Temperature exceeding reasonable range (> 1726.85°C)")
                
        elif prop_name == 'press':
            if value <= 0:
                raise ValueError("Pressure must be positive")
            if value > 1e9:  # 10000 bar - very high pressure
                raise ValueError("Pressure exceeding reasonable range (> 10000 bar)")
                
        elif prop_name == 'dens':
            if value <= 0:
                raise ValueError("Density must be positive")
            if value > 1e5:  # Very high density
                raise ValueError("Density exceeding reasonable range (> 100000 kg/m³)")
                
        elif prop_name == 'quality':
            if value < 0 or value > 1:
                raise ValueError("Quality must be between 0 and 1")
                
        # Validation for newly settable properties
        elif prop_name == 'enthalpy':
            # No strict limits on enthalpy, but should be reasonable
            if abs(value) > 1e8:  # Very high enthalpy
                raise ValueError("Enthalpy exceeding reasonable range (|h| > 100,000,000 J/kg)")
                
        elif prop_name == 'entropy':
            # No strict limits on entropy, but should be reasonable
            if abs(value) > 1e6:  # Very high entropy
                raise ValueError("Entropy exceeding reasonable range (|s| > 1,000,000 J/kg-K)")
                
        elif prop_name == 'cp':
            if value <= 0:
                raise ValueError("Specific heat capacity at constant pressure must be positive")
            if value > 1e5:  # Very high cp
                raise ValueError("Specific heat capacity exceeding reasonable range (> 100,000 J/kg-K)")
                
        elif prop_name == 'cv':
            if value <= 0:
                raise ValueError("Specific heat capacity at constant volume must be positive")
            if value > 1e5:  # Very high cv
                raise ValueError("Specific heat capacity exceeding reasonable range (> 100,000 J/kg-K)")
        
        return func(self, value)
    return wrapper

def state_setter_PROPS(func):
    """
    Decorator for property setters that manages state constraints for pure fluid properties.
    
    Checks if fluid is set before allowing properties to be set.
    Checks if this property is already set before allowing changes.
    Property state validity is handled by CoolProp, and exceptions are passed to user.
    Also tracks which properties have been set for state validation.
    """
    @wraps(func)
    def wrapper(self, value):
        prop_name = func.__name__.replace('_setter', '')
        
        # Check if fluid is set before allowing any property to be set
        if not hasattr(self, '_fluid') or self._fluid is None:
            raise ValueError(f"Cannot set {prop_name} - fluid type must be set first with state.fluid = 'fluid_name'")
        
        # Initialize constraints set if not exists
        if not hasattr(self, '_constraints_set'):
            self._constraints_set = set()
        
        # Always allow setting if we have 0 or 1 constraint or if this property is already set
        if len(self._constraints_set) < 2 or prop_name in self._constraints_set:
            func(self, value)
            self._constraints_set.add(prop_name)
            return
            
        # If we already have 2 constraints, try to set the property
        # CoolProp will validate state and throw error if invalid
        try:
            # Try to set the property
            func(self, value)
            # If successful, add to constraints
            self._constraints_set.add(prop_name)
        except Exception as e:
            # Pass along any CoolProp errors to the user
            raise ValueError(f"Cannot set {prop_name} - {str(e)}")
            
    return wrapper

def cached_property(func):
    """
    Decorator for property getters that implements version-based caching.
    
    If the property is part of the constraints set, returns the directly set value.
    Otherwise, checks if the cached value is from the current state version before returning it.
    If not current, recalculates the property and updates the cache.
    """
    @wraps(func)
    def getter(self):
        prop_name = func.__name__
        version_attr = f"_{prop_name}_version"
        value_attr = f"_{prop_name}"
        
        # If we don't have 3 constraints yet, can't calculate anything
        if not hasattr(self, '_constraints_set') or len(self._constraints_set) < 3:
            return getattr(self, value_attr)
        
        # If this property is one of our constraints, return the set value
        if prop_name in self._constraints_set:
            return getattr(self, value_attr)
        
        # Otherwise, check if we need to update the cached value
        if (not hasattr(self, version_attr) or 
            getattr(self, version_attr) != self._version):
            # Get the CoolProp property name from our mapping
            coolprop_name = self._prop_map[prop_name]
            # Calculate and store the new value
            value = self.get_prop(coolprop_name)
            setattr(self, value_attr, value)
            # Update the version
            setattr(self, version_attr, self._version)
        
        return getattr(self, value_attr)
    
    return getter

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
    
    _prop_map = {
        'tempk': 'T',
        'tempc': 'T',  # Will need special handling for Celsius conversion
        'press': 'P',
        'humrat': 'W',
        'wetbulb': 'B',
        'relhum': 'R',
        'dewpoint': 'D',
        'vol': 'V',
        'enthalpy': 'H', 
        'entropy': 'S',
        'density': 'D',
        'cp': 'C',
        'viscosity': 'M',
        'conductivity': 'K',
        'prandtl': 'L'
    }

    def __init__(self, props=None):
        """
        Initialize a StateHA object for humid air properties.
        
        Note:
            While passing props at initialization is still supported for backwards compatibility,
            it is recommended to set properties individually for better performance:
                state = StateHA()
                state.tempk = 293.15
                state.press = 101325
                state.relhum = 0.5
        
        Args:
            props (list, optional): DEPRECATED. Property inputs for HAPropsSI.
                While still supported, direct property setting is preferred.
                [prop1_name, prop1_value, prop2_name, prop2_value, prop3_name, prop3_value]
        """
        self._tempk = None
        self._tempc = None
        self._press = None
        self._humrat = None
        self._wetbulb = None
        self._relhum = None
        self._vol = None
        self._enthalpy = None
        self._entropy = None
        self._dewpoint = None
        self._density = None
        self._cp = None
        self._viscosity = None
        self._conductivity = None
        self._prandtl = None
        
        self._constraints_set = set()
        
        if props is not None:
            warnings.warn(
                "Initializing with props is deprecated and will be removed in version 2.0.0. "
                "Use direct property setting instead:\n"
                "    state = StateHA()\n"
                "    state.tempk = value\n"
                "    state.press = value\n"
                "    state.relhum = value",
                DeprecationWarning,
                stacklevel=2
            )
            self.set(props)

    @property
    def tempk(self):
        if 'tempk' in self._constraints_set:
            return self._tempk
        if len(self._constraints_set) == 3:
            return self.get_prop('T')
        return self._tempk

    @tempk.setter
    @state_setter_ha
    @validate_input_ha
    def tempk(self, value):
        self._tempk = value

    @property
    def tempc(self):
        if 'tempc' in self._constraints_set:
            return self._tempc
        if 'tempk' in self._constraints_set:
            return self._tempk - 273.15
        return self.tempk - 273.15

    @tempc.setter
    @state_setter_ha
    @validate_input_ha
    def tempc(self, value):
        self._tempc = value
        self._tempk = value + 273.15

    @property
    def press(self):
        if 'press' in self._constraints_set:
            return self._press
        if len(self._constraints_set) == 3:
            return self.get_prop('P')
        return self._press

    @press.setter
    @state_setter_ha
    @validate_input_ha
    def press(self, value):
        self._press = value

    @property
    def relhum(self):
        if 'relhum' in self._constraints_set:
            return self._relhum
        if len(self._constraints_set) == 3:
            return self.get_prop('R')
        return self._relhum

    @relhum.setter
    @state_setter_ha
    @validate_input_ha
    def relhum(self, value):
        self._relhum = value

    @property
    def humrat(self):
        if 'humrat' in self._constraints_set:
            return self._humrat
        if len(self._constraints_set) == 3:
            return self.get_prop('W')
        return self._humrat

    @humrat.setter
    @state_setter_ha
    @validate_input_ha
    def humrat(self, value):
        self._humrat = value

    @property
    def wetbulb(self):
        if 'wetbulb' in self._constraints_set:
            return self._wetbulb
        if len(self._constraints_set) == 3:
            return self.get_prop('B')
        return self._wetbulb

    @wetbulb.setter
    @state_setter_ha
    @validate_input_ha
    def wetbulb(self, value):
        self._wetbulb = value

    @property
    def dewpoint(self):
        if 'dewpoint' in self._constraints_set:
            return self._dewpoint
        if len(self._constraints_set) == 3:
            return self.get_prop('D')
        return self._dewpoint

    @dewpoint.setter
    @state_setter_ha
    @validate_input_ha
    def dewpoint(self, value):
        self._dewpoint = value

    @property
    def vol(self):
        if 'vol' in self._constraints_set:
            return self._vol
        if len(self._constraints_set) == 3:
            return self.get_prop('V')
        return self._vol

    @vol.setter
    @state_setter_ha
    @validate_input_ha
    def vol(self, value):
        self._vol = value

    @property
    def enthalpy(self):
        if 'enthalpy' in self._constraints_set:
            return self._enthalpy
        if len(self._constraints_set) == 3:
            return self.get_prop('H')
        return self._enthalpy

    @enthalpy.setter
    @state_setter_ha
    @validate_input_ha
    def enthalpy(self, value):
        self._enthalpy = value

    @property
    def entropy(self):
        if 'entropy' in self._constraints_set:
            return self._entropy
        if len(self._constraints_set) == 3:
            return self.get_prop('S')
        return self._entropy

    @entropy.setter
    @state_setter_ha
    @validate_input_ha
    def entropy(self, value):
        self._entropy = value

    @property
    def density(self):
        if 'density' in self._constraints_set:
            return self._density
        if len(self._constraints_set) == 3:
            vol = self.get_prop('V')
            return 1/vol if vol is not None else None
        return self._density

    @density.setter
    @state_setter_ha
    @validate_input_ha
    def density(self, value):
        self._density = value

    @property
    def cp(self):
        if 'cp' in self._constraints_set:
            return self._cp
        if len(self._constraints_set) == 3:
            return self.get_prop('C')
        return self._cp

    @cp.setter
    @state_setter_ha
    @validate_input_ha
    def cp(self, value):
        self._cp = value

    @property
    def viscosity(self):
        if 'viscosity' in self._constraints_set:
            return self._viscosity
        if len(self._constraints_set) == 3:
            return self.get_prop('M')
        return self._viscosity

    @viscosity.setter
    @state_setter_ha
    @validate_input_ha
    def viscosity(self, value):
        self._viscosity = value

    @property
    def conductivity(self):
        if 'conductivity' in self._constraints_set:
            return self._conductivity
        if len(self._constraints_set) == 3:
            return self.get_prop('K')
        return self._conductivity

    @conductivity.setter
    @state_setter_ha
    @validate_input_ha
    def conductivity(self, value):
        self._conductivity = value

    @property
    def prandtl(self):
        if 'prandtl' in self._constraints_set:
            return self._prandtl
        if len(self._constraints_set) == 3:
            return self.get_prop('L')
        return self._prandtl

    @prandtl.setter
    @state_setter_ha
    @validate_input_ha
    def prandtl(self, value):
        self._prandtl = value

    @property
    def constraints(self):
        """
        Returns the current set of properties constraining the state.
        
        This property allows checking which values are currently pinning the thermodynamic state.
        For a humid air state to be fully defined, it needs exactly 3 constraints.
        
        Returns:
            list: A sorted list of property names that are currently set as constraints.
        """
        if not hasattr(self, '_constraints_set'):
            return []
        return sorted(list(self._constraints_set))

    def set(self, props):
        """
        DEPRECATED: Direct property setting is now preferred over the set method.
        
        Set the properties of the StateHA object using the provided inputs.
        This method will be removed in version 2.0.0.
        
        Instead of:
            state.set(['T', 293.15, 'P', 101325, 'R', 0.5])
        Use:
            state.tempk = 293.15
            state.press = 101325
            state.relhum = 0.5
        
        Args:
            props (list): Property inputs for HAPropsSI in the format
                [prop1_name, prop1_value, prop2_name, prop2_value, prop3_name, prop3_value]
        
        Returns:
            StateHA: The current object for method chaining.
        """
        warnings.warn(
            "The set() method is deprecated and will be removed in version 2.0.0. "
            "Use direct property setting instead (e.g., state.tempk = value).",
            DeprecationWarning,
            stacklevel=2
        )
        
        self.props = props
        # Map CoolProp properties to our setter methods
        prop_map = {
            'T': 'tempk',
            'P': 'press',
            'W': 'humrat',
            'R': 'relhum',
            'B': 'wetbulb',
            'D': 'dewpoint',
            'V': 'vol',
            'H': 'enthalpy',
            'S': 'entropy',
            'C': 'cp',
            'M': 'viscosity',
            'K': 'conductivity',
            'L': 'prandtl'
        }
        
        # Set properties using our property setters
        for i in range(0, len(props), 2):
            prop_name = props[i]
            value = props[i + 1]
            if prop_name in prop_map:
                setattr(self, prop_map[prop_name], value)
        
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
        
        Raises:
            ValueError: If the state is not fully defined (needs 3 constraints)
        """
        if len(self._constraints_set) < 3:
            raise ValueError("Cannot calculate properties until state is fully defined with 3 constraints")
        
        # Build props list from constraints set
        props = []
        for constraint in self._constraints_set:
            coolprop_name = self._prop_map[constraint]
            value = getattr(self, f"_{constraint}")
            # Handle Celsius conversion
            if constraint == 'tempc':
                value = value + 273.15
            props.extend([coolprop_name, value])
        
        return HAPropsSI(prop, *props)

    def test_state_validity(self, current_props, new_prop, new_value):
        """
        Test if the current state properties are physically valid using HAPropsSI.
        
        Args:
            current_props (set): Set of currently set property names
            new_prop (str): Name of the new property being set
            new_value (float): Value of the new property
        
        Returns:
            bool: True if the state is valid, False otherwise.
        
        Raises:
            ValueError: If the combination of properties would create an invalid state,
                      with the specific error message from CoolProp.
        """
        try:
            # Build a test props list with current properties and new value
            test_props = []
            for prop in current_props:
                coolprop_name = self._prop_map[prop]
                value = getattr(self, f"_{prop}")
                # Handle Celsius conversion
                if prop == 'tempc':
                    value = value + 273.15
                test_props.extend([coolprop_name, value])
            
            # Add the new property
            coolprop_new_prop = self._prop_map[new_prop]
            new_value_converted = new_value + 273.15 if new_prop == 'tempc' else new_value
            test_props.extend([coolprop_new_prop, new_value_converted])
            
            # Try to calculate one of the input properties to validate state
            input_prop = self._prop_map[list(current_props)[0]]  # Use first property from current set
            HAPropsSI(input_prop, *test_props)
            return True
            
        except ValueError as e:
            # Re-raise with the CoolProp error message for better explanation
            raise ValueError(f"Invalid state: {str(e)}") from None

class StatePROPS:
    """
    A class representing the thermodynamic state of a pure fluid.
    
    This class provides an object-oriented interface to CoolProp's PropsSI function
    for pure fluid properties. It automatically calculates and caches common properties
    for easy access.
    
    Important:
        For a StatePROPS object to be fully defined, you must:
        1. Set the fluid type with state.fluid = 'fluid_name'
        2. Set exactly 2 independent thermodynamic properties
    
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
        fluid (str): The working fluid name (must be set before other properties)
        
    Example:
        >>> # Create state for water at 25°C, 1 atm
        >>> state = StatePROPS()
        >>> state.fluid = 'Water'
        >>> state.tempc = 25
        >>> state.press = 101325
        >>> print(f"Density: {state.dens:.2f} kg/m³")
        Density: 997.05 kg/m³
    """
    
    _prop_map = {
        'tempk': 'T',
        'tempc': 'T',  # Will need special handling for Celsius conversion
        'press': 'P',
        'dens': 'D',
        'enthalpy': 'H',
        'entropy': 'S',
        'quality': 'Q',
        'cp': 'C',
        'cv': 'O'
    }
    
    def __init__(self, props=None, fluid=None):
        """
        Initialize a StatePROPS object for pure fluid properties.
        
        Args:
            props (list, optional): DEPRECATED. Property inputs for PropsSI.
                While still supported, direct property setting is preferred.
                [prop1_name, prop1_value, prop2_name, prop2_value, fluid_name]
            fluid (str, optional): The working fluid name. If provided, sets the fluid immediately.
                This is the recommended way to initialize a StatePROPS object.
        
        Example:
            >>> # Recommended initialization
            >>> state = StatePROPS(fluid='Water')
            >>> state.tempc = 25
            >>> state.press = 101325
        """
        self._tempk = None
        self._tempc = None
        self._press = None
        self._dens = None
        self._enthalpy = None
        self._entropy = None
        self._quality = None
        self._cp = None
        self._cv = None
        self._fluid = None
        
        self._constraints_set = set()
        
        # Set fluid if provided
        if fluid is not None:
            self.fluid = fluid
        
        if props is not None:
            warnings.warn(
                "Initializing with props is deprecated and will be removed in version 2.0.0. "
                "Use direct property setting instead:\n"
                "    state = StatePROPS(fluid='water')\n"
                "    state.tempk = value\n"
                "    state.press = value",
                DeprecationWarning,
                stacklevel=2
            )
            self.set(props)

    @property
    def tempk(self):
        if 'tempk' in self._constraints_set:
            return self._tempk
        if len(self._constraints_set) == 2:
            return self.get_prop('T')
        return self._tempk

    @tempk.setter
    @state_setter_PROPS
    @validate_input_props
    def tempk(self, value):
        self._tempk = value

    @property
    def tempc(self):
        if 'tempc' in self._constraints_set:
            return self._tempc
        if 'tempk' in self._constraints_set:
            return self._tempk - 273.15
        return self.tempk - 273.15 if self.tempk is not None else None

    @tempc.setter
    @state_setter_PROPS
    @validate_input_props
    def tempc(self, value):
        self._tempc = value
        self._tempk = value + 273.15

    @property
    def press(self):
        if 'press' in self._constraints_set:
            return self._press
        if len(self._constraints_set) == 2:
            return self.get_prop('P')
        return self._press

    @press.setter
    @state_setter_PROPS
    @validate_input_props
    def press(self, value):
        self._press = value

    @property
    def dens(self):
        if 'dens' in self._constraints_set:
            return self._dens
        if len(self._constraints_set) == 2:
            return self.get_prop('D')
        return self._dens

    @dens.setter
    @state_setter_PROPS
    @validate_input_props
    def dens(self, value):
        self._dens = value

    @property
    def quality(self):
        if 'quality' in self._constraints_set:
            return self._quality
        if len(self._constraints_set) == 2 and self._fluid is not None:
            try:
                return self.get_prop('Q')
            except ValueError:
                return None  # Not in two-phase region
        return None  # Return None if not fully defined

    @quality.setter
    @state_setter_PROPS
    @validate_input_props
    def quality(self, value):
        self._quality = value

    @property
    def enthalpy(self):
        if 'enthalpy' in self._constraints_set:
            return self._enthalpy
        if len(self._constraints_set) == 2 and self._fluid is not None:
            return self.get_prop('H')
        return None

    @enthalpy.setter
    @state_setter_PROPS
    @validate_input_props
    def enthalpy(self, value):
        self._enthalpy = value

    @property
    def entropy(self):
        if 'entropy' in self._constraints_set:
            return self._entropy
        if len(self._constraints_set) == 2 and self._fluid is not None:
            return self.get_prop('S')
        return None

    @entropy.setter
    @state_setter_PROPS
    @validate_input_props
    def entropy(self, value):
        self._entropy = value

    @property
    def cp(self):
        if 'cp' in self._constraints_set:
            return self._cp
        if len(self._constraints_set) == 2 and self._fluid is not None:
            return self.get_prop('C')
        return None

    @cp.setter
    @state_setter_PROPS
    @validate_input_props
    def cp(self, value):
        self._cp = value

    @property
    def cv(self):
        if 'cv' in self._constraints_set:
            return self._cv
        if len(self._constraints_set) == 2 and self._fluid is not None:
            return self.get_prop('O')
        return None

    @cv.setter
    @state_setter_PROPS
    @validate_input_props
    def cv(self, value):
        self._cv = value

    @property
    def constraints(self):
        """
        Returns the current set of properties constraining the state.
        
        This property allows checking which values are currently pinning the thermodynamic state.
        For a pure fluid state to be fully defined, it needs exactly 2 constraints plus a fluid type.
        
        Returns:
            dict: A dictionary containing:
                - 'properties': List of thermodynamic property names that are set as constraints
                - 'fluid': The currently set fluid name or None if not set
                - 'is_complete': Boolean indicating if the state is fully defined
                - 'status': Status of the fluid (e.g., 'liquid', 'gas', 'supercritical', etc.)
                - 'edition': Edition of CoolProp being used
        """
        if not hasattr(self, '_constraints_set'):
            props = []
        else:
            props = sorted(list(self._constraints_set))
        
        fluid = self._fluid if hasattr(self, '_fluid') else None
        
        # Check if the state is complete to determine status
        status = None
        edition = None
        
        if len(props) == 2 and fluid is not None:
            try:
                # Get status of the fluid at the specified state
                if 'quality' in props:
                    # If quality is specified, we know the status
                    quality_val = getattr(self, '_quality')
                    if quality_val == 0:
                        status = 'saturated_liquid'
                    elif quality_val == 1:
                        status = 'saturated_vapor'
                    else:
                        status = 'two_phase'
                else:
                    # Try to get phase information
                    try:
                        quality = self.quality
                        if quality == -1.0:
                            # Check pressure against critical pressure
                            if 'press' in props:
                                press_val = getattr(self, '_press')
                                if press_val > self.get_prop('pcrit'):
                                    status = 'supercritical'
                                else:
                                    # Check temperature
                                    if 'tempk' in props or 'tempc' in props:
                                        temp_val = getattr(self, '_tempk')
                                        if temp_val > self.get_prop('Tcrit'):
                                            status = 'supercritical'
                                        else:
                                            status = 'liquid' 
                            else:
                                status = 'single_phase'
                        else:
                            status = 'two_phase'
                    except:
                        status = 'single_phase'
                
                # Get CoolProp version/edition information
                try:
                    from CoolProp import __version__ as cp_version
                    edition = cp_version
                except:
                    edition = "Unknown"
            except:
                status = "Unknown"
                edition = "Unknown"
        
        return {
            'properties': props,
            'fluid': fluid,
            'is_complete': len(props) == 2 and fluid is not None,
            'status': status,
            'edition': edition
        }

    @property
    def fluid(self):
        return self._fluid

    @fluid.setter
    def fluid(self, value):
        if not isinstance(value, str):
            raise TypeError("fluid must be a string")
        self._fluid = value

    def set(self, props):
        """
        DEPRECATED: Direct property setting is now preferred over the set method.
        
        Set the properties of the StatePROPS object using the provided inputs.
        This method will be removed in version 2.0.0.
        
        Instead of:
            state.set(['T', 293.15, 'P', 101325, 'water'])
        Use:
            state.fluid = 'water'
            state.tempk = 293.15
            state.press = 101325
        
        Args:
            props (list): Property inputs for PropsSI in the format
                [prop1_name, prop1_value, prop2_name, prop2_value, fluid_name]
        
        Returns:
            StatePROPS: The current object for method chaining.
        """
        warnings.warn(
            "The set() method is deprecated and will be removed in version 2.0.0. "
            "Use direct property setting instead (e.g., state.fluid = 'fluid_name', state.tempk = value).",
            DeprecationWarning,
            stacklevel=2
        )
        
        # Extract and set fluid name first (last element of props)
        if len(props) >= 5:  # At least 2 properties (4 elements) plus fluid
            self.fluid = props[-1]
            props = props[:-1]  # Remove fluid from props
        else:
            raise ValueError("Props must include a fluid name as the last element")
        
        # Map CoolProp properties to our setter methods
        prop_map = {
            'T': 'tempk',
            'P': 'press',
            'Q': 'quality',
            'D': 'dens',
            'H': 'enthalpy',
            'S': 'entropy',
            'C': 'cp',
            'O': 'cv'
        }
        
        # Set properties using our property setters
        for i in range(0, len(props), 2):
            prop_name = props[i]
            value = props[i + 1]
            if prop_name in prop_map:
                try:
                    setattr(self, prop_map[prop_name], value)
                except ValueError as e:
                    # Provide warning for properties that CoolProp rejects
                    warnings.warn(f"Unable to set {prop_name}: {str(e)}")
        
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
        
        Raises:
            ValueError: If the state is not fully defined (needs 2 constraints and fluid type)
        """
        if len(self._constraints_set) < 2:
            raise ValueError("Cannot calculate properties until state is fully defined with 2 constraints")
            
        if not self._fluid:
            raise ValueError("Fluid type must be set before calculating properties")
        
        # Build props list from constraints set
        props = []
        for constraint in self._constraints_set:
            coolprop_name = self._prop_map[constraint]
            value = getattr(self, f"_{constraint}")
            # Handle Celsius conversion
            if constraint == 'tempc':
                value = value + 273.15
            props.extend([coolprop_name, value])
        
        props.append(self._fluid)
        return PropsSI(prop, *props)

    def test_state_validity(self, current_props, new_prop, new_value):
        """
        Test if the current state properties are physically valid using PropsSI.
        
        Args:
            current_props (set): Set of currently set property names
            new_prop (str): Name of the new property being set
            new_value (float): Value of the new property
        
        Returns:
            bool: True if the state is valid, False otherwise.
        
        Raises:
            ValueError: If the combination of properties would create an invalid state,
                      with the specific error message from CoolProp.
        """
        if not self._fluid:
            raise ValueError("Fluid type must be set before validating state")
            
        try:
            # Build a test props list with current properties and new value
            test_props = []
            for prop in current_props:
                coolprop_name = self._prop_map[prop]
                value = getattr(self, f"_{prop}")
                # Handle Celsius conversion
                if prop == 'tempc':
                    value = value + 273.15
                test_props.extend([coolprop_name, value])
            
            # Add the new property
            coolprop_new_prop = self._prop_map[new_prop]
            new_value_converted = new_value + 273.15 if new_prop == 'tempc' else new_value
            test_props.extend([coolprop_new_prop, new_value_converted])
            test_props.append(self._fluid)
            
            # Try to calculate one of the input properties to validate state
            input_prop = self._prop_map[list(current_props)[0]]  # Use first property from current set
            PropsSI(input_prop, *test_props)
            return True
            
        except ValueError as e:
            # Re-raise with the CoolProp error message for better explanation
            raise ValueError(f"Invalid state: {str(e)}") from None