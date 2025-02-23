"""file to hold the DataStorage class"""
from dataclasses import dataclass, field
from typing import Callable
import os
from PIL.Image import Image

try:
    import image_generator
    import image_generator.logic_circuit
    IMAGE_GENERATOR_AVAILABLE = True
except ImportError:
    IMAGE_GENERATOR_AVAILABLE = False
    print("Warning: image_generator module not available - some features will be disabled")

@dataclass
class DataStorage():
    """class to store information persistent across the program"""
    bool_func: str = field(default='')
    last_result: list[str] = field(default_factory=list)
    pipeline_steps_active: dict[str, any] = field(default_factory=dict)
    input_devices: dict[str, dict[str, any]] = field(default_factory=dict)
    output_devices: dict[str, dict[str, any]] = field(default_factory=dict)
    not_nor2_devices: dict[str, dict[str, any]] = field(default_factory=dict)
    pipeline_is_running: bool = field(default_factory=bool)
    dictionary: dict[str, str] = field(default_factory=dict)

    def clear_devices(self) -> None:
        """Clear all device dictionaries"""
        self.input_devices.clear()
        self.output_devices.clear()
        self.not_nor2_devices.clear()

storage = DataStorage()

@dataclass
class ImageDB():
    _images:dict[str, str] = field(default_factory=dict)
    _hooks:list[Callable[[str], None]]= field(default_factory=list)
    def register(self, hook:Callable[[], None])->None:
        self._hooks.append(hook)
    def __getitem__(self, imgID:str)->str:
        img = self._images[imgID]
        if IMAGE_GENERATOR_AVAILABLE and img.endswith('.json'):
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

    def _load_config(self, path: str) -> dict[str, str]:
        """Loads

        Args:
            path (str): path to config file
        """
        config_content = {}
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'): # Ignore comments and empty lines
                    key, value = line.split('=', 1)
                    config_content[key.strip()] = value.strip()
        return config_content

    def _load_configs(self):
        """Load configurations from files"""
        config_files = {
            'map': 'map.config',
            'sim': 'sim.config',
            'syn': 'syn.config',
            'gui': 'gui.config'
        }

        current_dir = os.path.dirname(os.path.dirname(__file__))
        arctic_gui_dir = os.path.dirname(current_dir)

        for config_name, filename in config_files.items():
            path = os.path.join(arctic_gui_dir, filename)
            self._config_files[config_name] = path

            if os.path.exists(path):
                self._current_configs[config_name] = self._load_config(path)

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

    def load_language_dictionary(self, path: str) -> dict[str, str]:
        """Load language pack

        Args:
            path (str): path to dictionary

        Returns:
            dict: dictionary holding the language
        """
        try:
            return self._load_config(path)
        except (FileNotFoundError, TypeError):
            print(f"Warning: Language file not found at {path}")
            return {}

    def get_available_simulators(self) -> list[str]:
        """Get list of all available simulators from ARCTICsim directory
        
        Returns:
            list[str]: List of simulator directory names
        """
        current_dir = os.path.dirname(os.path.dirname(__file__))
        arctic_gui_dir = os.path.dirname(current_dir)
        arctic_sim_dir = os.path.join(os.path.dirname(arctic_gui_dir), 'ARCTICsim')
        
        simulators = []
        try:
            for dir_name in os.listdir(arctic_sim_dir):
                if dir_name.startswith('simulator_') and os.path.isdir(os.path.join(arctic_sim_dir, dir_name)):
                    simulators.append(dir_name)
        except FileNotFoundError:
            print(f"Warning: ARCTICsim directory not found at {arctic_sim_dir}")
            
        return simulators

    def load_active_simulator_settings(self) -> dict[str, str]:
        """Load settings from the active simulator's settings_config.cfg and store them in config manager
        
        The settings are stored in _current_configs['simulator_settings'] and can be accessed
        using get_config('simulator_settings', 'section.setting_name')
        
        Returns:
            dict[str, str]: Dictionary of settings from the active simulator
            
        Example:
            # Load settings when switching simulator
            config_manager.load_active_simulator_settings()
            
            # Access settings anywhere in the program
            threads = config_manager.get_config('simulator_settings', 'simulation.threads')
        """
        current_dir = os.path.dirname(os.path.dirname(__file__))
        arctic_gui_dir = os.path.dirname(current_dir)
        arctic_sim_dir = os.path.join(os.path.dirname(arctic_gui_dir), 'ARCTICsim')
        
        active_sim_path = self.get_config('sim', 'SIM_PATH')
        if not active_sim_path:
            return {}
            
        # Extract just the simulator directory name from the path
        active_sim_name = os.path.basename(active_sim_path.replace('../ARCTICsim/', ''))
        
        settings_path = os.path.join(arctic_sim_dir, active_sim_name, 'settings_config.cfg')
        
        if not os.path.exists(settings_path):
            print(f"Warning: settings_config.cfg not found at {settings_path}")
            return {}
            
        settings = {}
        with open(settings_path, 'r') as f:
            current_section = None
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if line.startswith('[') and line.endswith(']'):
                    current_section = line[1:-1]
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.split('#')[0].strip()  # Remove comments
                    if current_section:
                        key = f"{current_section}.{key}"
                    settings[key] = value
        
        # Store the settings in _current_configs
        self._current_configs['simulator_settings'] = settings
                    
        return settings

config_manager = ConfigManager()
del ConfigManager

try:
    storage.dictionary = config_manager.load_language_dictionary(config_manager.get_config('gui', 'LANGUAGE_PATH'))
except Exception as e:
    print(f"Warning: Could not load language dictionary: {e}")
    storage.dictionary = {}
