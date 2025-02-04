"""file to hold the DataStorage class"""
from dataclasses import dataclass, field
from typing import Callable
from PIL.Image import Image
import image_generator
import image_generator.logic_circuit
import os

@dataclass
class DataStorage():
    """class to store information persistent across the program"""
    bool_func: str = field(default='')
    last_result: list[str] = field(default_factory=list)
    pipeline_steps_active: dict[str, any] = field(default_factory=dict)
    input_devices: dict[str, dict[str, any]] = field(default_factory=dict)
    output_devices: dict[str, dict[str, any]] = field(default_factory=dict)
    not_nor2_devices: dict[str, dict[str, any]] = field(default_factory=dict)

    def clear_devices(self) -> None:
        """Clear all device dictionaries"""
        self.input_devices.clear()
        self.output_devices.clear()
        self.not_nor2_devices.clear()

storage = DataStorage()
del DataStorage

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
del ImageDB

@dataclass
class ConfigManager:
    """Simple config manager"""
    _current_configs: dict = field(default_factory=dict)
    _config_files: dict = field(default_factory=dict)

    def __post_init__(self):
        self._load_configs()

    def _load_configs(self):
        """Load configurations from files"""
        config_files = {
            'map': 'map.config',
            'sim': 'sim.config',
            'syn': 'syn.config'
        }
        
        current_dir = os.path.dirname(os.path.dirname(__file__))
        arctic_gui_dir = os.path.dirname(current_dir)
        
        for config_name, filename in config_files.items():
            path = os.path.join(arctic_gui_dir, filename)
            self._config_files[config_name] = path
            
            if os.path.exists(path):
                config_content = {}
                with open(path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'): # Ignore comments and empty lines
                            key, value = line.split('=', 1)
                            config_content[key.strip()] = value.strip()
                self._current_configs[config_name] = config_content
            else:
                print(f"Warning: Config file not found at {path}")

    def update_config(self, config_name: str, key: str, value: str) -> None:
        """Update config value and write to file"""
        if config_name not in self._current_configs:
            raise ValueError(f"Unknown config: {config_name}")
        
        # Convert backslashes to forward slashes for paths
        if key == 'LIBRARY':
            value = value.replace('\\', '/')
        
        self._current_configs[config_name][key] = value
        self._write_config_to_file(config_name)

    def _write_config_to_file(self, config_name: str) -> None:
        """Write current configuration to file"""
        config_path = self._config_files[config_name]
        config = self._current_configs[config_name]
        
        with open(config_path, 'r') as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            if line.strip() and not line.strip().startswith('#'):
                key = line.split('=')[0].strip()
                if key in config:
                    new_lines.append(f"{key}={config[key]}\n")
                    continue
            new_lines.append(line)

        with open(config_path, 'w') as f:
            f.writelines(new_lines)

    def get_config(self, config_name: str, key: str) -> str:
        """Get current value for a config key"""
        return self._current_configs.get(config_name, {}).get(key)

config_manager = ConfigManager()