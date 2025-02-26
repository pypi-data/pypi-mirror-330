from CoolProp.CoolProp import HAPropsSI, PropsSI

class StateHA:
    def __init__(self, props=None):
        """
        Initialize a State object for humid air properties.
        
        Args:
            props: Optional list of property inputs for HAPropsSI.
                  If provided, the set method will be called automatically.
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
        Set the properties of the State object using the provided inputs.
        
        Args:
            props: List of property inputs for HAPropsSI.
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
            prop: The property to retrieve.
            
        Returns:
            The value of the requested property.
        """
        return HAPropsSI(prop, *self.props)

class StatePROPS:
    def __init__(self, props=None):
        """
        Initialize a State object for pure fluid properties using PropsSI.
        
        Args:
            props: Optional list of property inputs for PropsSI.
                  If provided, the set method will be called automatically.
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
        Set the properties of the State object using the provided inputs.
        
        Args:
            props: List of property inputs for PropsSI.
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
            prop: The property to retrieve.
            
        Returns:
            The value of the requested property.
        """
        return PropsSI(prop, *self.props) 