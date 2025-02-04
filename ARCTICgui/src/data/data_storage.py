"""file to hold the DataStorage class"""
from dataclasses import dataclass, field
from typing import Callable
from PIL.Image import Image

@dataclass
class DataStorage():
    """Singleton class to store information persistent across the program"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataStorage, cls).__new__(cls)
            # Initialize default values here
            cls._instance.bool_func = ''
            cls._instance.last_result = []
            cls._instance.pipeline_steps_active = {}
            cls._instance.input_devices = {}
            cls._instance.output_devices = {}
        return cls._instance

    def __init__(self):
        """Initialize is called after __new__, but we don't need to do anything here"""
        pass

    def clear_devices(self):
        """Clear both input and output devices"""
        self.input_devices.clear()
        self.output_devices.clear()

# Create single instance
storage = DataStorage()

@dataclass
class ImageDB():
    _images:dict[str, str] = field(default_factory=dict)
    _hooks:list[Callable[[str], None]]= field(default_factory=list)
    def register(self, hook:Callable[[], None])->None:
        self._hooks.append(hook)
    def __getitem__(self, imgID:str)->str:
        # Simplified version for testing
        return self._images[imgID]
    def __setitem__(self, imgID:str, img:str)->None:
        self._images[imgID] = img
    def __delitem__(self, imgID:str)->str:
        del self._images[imgID]
    def ids(self)->list[str]:
        return list(self._images.keys())
    def clear(self)->None:
        self._images.clear()
    def update(self)->None:
        for fun in self._hooks:
            fun()

images = ImageDB()
