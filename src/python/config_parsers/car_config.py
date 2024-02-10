from enum import Enum
import xml.etree.cElementTree as ET


DEFAULT_INSTALL_DIR = 'F:/WRC Generations/'

class SURFACE(Enum):
    GRAVEL = "GRAVEL"
    ASPHALT = "ASPHALT"

class TYRES(Enum):
    HARD_ASPHALT = "HARD_ASPHALT"
    HARD_GRAVEL = "HARD_GRAVEL"
    NAILED_ASPHALT = 'NAILED_ASPHALT'
    NAILED_SNOW = "NAILED_SNOW"
    SOFT_ASPHALT = "SOFT_ASPHALT"
    SOFT_GRAVEL = "SOFT_GRAVEL"
    SOFT_WET = "SOFT_WET"

class CarConfiguration:
    
    def __init__(self, car, install_dir=DEFAULT_INSTALL_DIR):
        self._dyn_car_dir = install_dir + "Common/Tuning/DYNA/CARS/"
        self._dyn_tyre_dir = install_dir + "Common/Tuning/DYNA/TYRES/"

        self._car = car
    
    @property
    def car(self):
        return self._car
    
    @property
    def dyn_car_dir(self):
        return self._dyn_car_dir
    
    @property
    def dyn_tyre_dir(self):
        return self._dyn_tyre_dir

    def get_car_prop(self, surface, prop_parent, prop_name):
        """
        param: surface
            surface can be GRAVEL or ASPHALT
        param: prop_parent
            Any of top level children in the xml, these are WrcVehicleSDK, front_left_wheel, front_right_wheel, rear_right_wheel, rear_left_wheel
        param: prop_name
            name of the property you want, i.e. - Brake Bias, Max Brake Torque etc.
        Returns value of th prop
        """
        # car enum values have prefixes to mark car class, L - Legendary, W1 - WRC1, W2 - WRC2, J - JWRC
        car_class_prefix = self.car.value.split('_')[0]
        car_name = self.car.value.split('_')[1]

        if car_class_prefix == 'L':
            car_class = "LEGENDS"
        elif car_class_prefix == 'W1':
            car_class = "WRC1"
        elif car_class_prefix == 'W2':
            car_class = "WRC2"
        elif car_class_prefix == "J":
            car_class = "WRCJ"

        if car_class != 'WRCJ':
            dyn_car_filepath = self.dyn_car_dir + f"{car_class}/{surface}_{car_name}.DYN"
        else:
            dyn_car_filepath = self.dyn_car_dir + f"{surface}_{car_name}.DYN"

        if not dyn_car_filepath:
            raise ValueError("Some issue with either car enums or surface passed")

        
        with open(dyn_car_filepath) as f:
            xml = f.read()
        enclosed_xml = "<data>"+xml+"</data>"
        
        root = ET.fromstring(enclosed_xml)
        prop_parent = root.find(f".//{prop_parent}")
        return prop_parent.find(f".//props/prop[@name='{prop_name}']").attrib['value']
    
    
    # TODO: This doesn't work at the moment, we need a map that maps names of cars in CARS/ with names of cars in TYRES/
    def get_tyre_prop(self, tyre, prop_parent, prop_name):
        """
        param: tyre
            tyre can be HARD_ASPHALT, HARD_GRAVEL etc.
        param: prop_parent
            Any of top level children in the xml, these are front_left_wheel, front_right_wheel, rear_right_wheel, rear_left_wheel
        param: prop_name
            name of the property you want, i.e. - Tire torque ratio etc.
        Returns value of th prop
        """
        car_name = self.car.value.split('_')[1]
        tyr_filepath = self.dyn_tyre_dir + f"{tyre}_{car_name}.TYR"
        
        with open(tyr_filepath) as f:
            xml = f.read()
        enclosed_xml = "<data>"+xml+"</data>"
        
        root = ET.fromstring(enclosed_xml)
        prop_parent = root.find(f".//{prop_parent}")
        return prop_parent.find(f".//*prop[@name='{prop_name}']").attrib['value']
    
