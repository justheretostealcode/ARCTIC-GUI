"""file to hold the DataStorage class"""
from dataclasses import dataclass, field
from typing import Callable
from PIL.Image import Image
import image_generator
import image_generator.logic_circuit
@dataclass
class DataStorage():
    """class to store information persistent across the program"
    """
    bool_func: str = field(default='')
    last_result:list[str] = field(default_factory=list)
    pipeline_steps_active = {}

storage = DataStorage()

@dataclass
class ImageDB():
    _images:dict[str, str] = field(default_factory=dict)
    _hooks:list[Callable[[str], None]]= field(default_factory=list)
    def register(self, hook:Callable[[], None])->None:
        self._hooks.append(hook)
    def __getitem__(self, imgID:str)->str:
        img = self._images[imgID]
        if img.endswith('.json'):
            with open(img, 'r') as file:
                path = img[:-4]+'jpeg'
                image:Image = image_generator.logic_circuit.gen(file.read(), {})
                image.save(path)
                img = path
        return img
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
