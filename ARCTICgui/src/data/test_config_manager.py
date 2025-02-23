"""Test file for ConfigManager's simulator-related functions"""
import os
import random
import time

try:
    import data_storage
except Exception as e:
    print(f"Warning: Error during import: {e}")
    exit(1)

def get_simulator_config_path() -> str:
    """Helper function to get path to active simulator's config file using same logic as ConfigManager"""
    current_dir = os.path.dirname(os.path.dirname(__file__))
    arctic_gui_dir = os.path.dirname(current_dir)
    arctic_sim_dir = os.path.join(os.path.dirname(arctic_gui_dir), 'ARCTICsim')
    
    active_sim_path = data_storage.config_manager.get_config('sim', 'SIM_PATH')
    if not active_sim_path:
        return ''
        
    active_sim_name = os.path.basename(active_sim_path.replace('../ARCTICsim/', ''))
    return os.path.join(arctic_sim_dir, active_sim_name, 'settings_config.cfg')

def read_raw_config(path: str, section: str, key: str) -> str:
    """Helper function to read value directly from config file"""
    current_section = None
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                continue
            if '=' in line and not line.startswith('#'):
                if current_section == section:
                    k, v = line.split('=', 1)
                    if k.strip() == key:
                        return v.split('#')[0].strip()
    return ''

def generate_test_param_name() -> str:
    """Generate unique parameter name based on timestamp"""
    return f"test_param_{int(time.time())}"

def main():
    """Main test function"""
    cm = data_storage.config_manager
    
    # Test getting available simulators
    print("=== Available Simulators ===")
    simulators = cm.get_available_simulators()
    print(f"Found {len(simulators)} simulators:")
    for sim in simulators:
        print(f"- {sim}")
    print()

    # Test loading and accessing simulator settings
    print("=== Active Simulator Settings ===")
    active_sim = cm.get_config('sim', 'SIM_PATH')
    print(f"Current simulator: {active_sim}")
    
    # Reload settings for current simulator
    settings = cm.reload_simulator_settings()
    print("\nAll settings:")
    for key, value in settings.items():
        print(f"- {key}: {value}")
    
    # Test updating simulator settings
    print("\n=== Testing Settings Update ===")
    
    # Get current values for comparison
    old_threads = cm.get_config('simulator_settings', 'simulation.threads')
    try:
        old_threads_int = int(old_threads) if old_threads and old_threads.lower() != 'none' else 4  # Default to 4 if not set
    except ValueError:
        old_threads_int = 4  # Default to 4 if not a valid number
    
    # Generate new random value based on old value
    timestamp = int(time.time())
    new_threads = str(max(2, old_threads_int + (timestamp % 5) + 2))  # Ensure it's at least 2
    
    print(f"Current threads value: {old_threads or 'not set'}")
    print(f"Updating threads to: {new_threads}")
    cm.update_config('simulator_settings', 'simulation.threads', new_threads)
    
    # Verify the change in memory
    updated_value = cm.get_config('simulator_settings', 'simulation.threads')
    print(f"New value in memory: {updated_value}")
    
    # Get path to config file using same logic as ConfigManager
    config_path = get_simulator_config_path()
    if not config_path:
        print("Error: Could not determine simulator config path")
        return
    
    file_value = read_raw_config(config_path, 'simulation', 'threads')
    print(f"New value in file: {file_value}")
    
    # Verify that they match
    if new_threads == updated_value == file_value:
        print("✓ Update successful - values match in memory and file")
    else:
        print("✗ Update failed - values don't match")
        print(f"Expected: {new_threads}")
        print(f"In memory: {updated_value}")
        print(f"In file: {file_value}")
    
    # Restore the original value
    # print(f"\nRestoring original value: {old_threads}")
    # cm.update_config('simulator_settings', 'simulation.threads', old_threads)
    
    # Test adding new unique setting
    print("\n=== Testing Adding New Setting ===")
    new_param_name = generate_test_param_name()
    
    test_value = str((int(time.time()) % 10000) + 1)  # Will be between 1 and 10000
    
    print(f"Adding new setting 'simulation.{new_param_name}' with value: {test_value}")
    cm.update_config('simulator_settings', f'simulation.{new_param_name}', test_value)
    
    # Verify the new setting in memory
    added_value = cm.get_config('simulator_settings', f'simulation.{new_param_name}')
    print(f"New setting in memory: {added_value}")
    
    # Verify the new setting in file
    file_value = read_raw_config(config_path, 'simulation', new_param_name)
    print(f"New setting in file: {file_value}")
    
    if test_value == added_value == file_value:
        print("✓ Add successful - values match in memory and file")
    else:
        print("✗ Add failed - values don't match")
        print(f"Expected: {test_value}")
        print(f"In memory: {added_value}")
        print(f"In file: {file_value}")
    
    print(f"\nTest complete! Added new parameter: simulation.{new_param_name} = {test_value}")

if __name__ == "__main__":
    main()
