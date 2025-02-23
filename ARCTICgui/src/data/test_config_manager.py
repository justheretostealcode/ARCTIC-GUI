"""Test file for ConfigManager's simulator-related functions"""
try:
    import data_storage
except Exception as e:
    print(f"Warning: Error during import: {e}")
    exit(1)

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
    print(f"Current simulator: {cm.get_config('sim', 'SIM_PATH')}")
    
    # Load settings for current simulator
    settings = cm.load_active_simulator_settings()
    print("\nAll settings:")
    for key, value in settings.items():
        print(f"- {key}: {value}")
        
    # Example of accessing specific settings
    print("\nAccessing specific settings:")
    print(f"Number of threads: {cm.get_config('simulator_settings', 'simulation.threads')}")
    print(f"Library path: {cm.get_config('simulator_settings', 'simulation.library')}")
    print(f"Error tolerance: {cm.get_config('simulator_settings', 'simulation.err')}")
    
    # Example of accessing settings from different sections
    print("\nSettings by section:")
    print("Debug settings:")
    print(f"- Verbosity: {cm.get_config('simulator_settings', 'debug.verbosity')}")
    print("\nRequired settings:")
    print(f"- Structure: {cm.get_config('simulator_settings', 'required.structure')}")
    print(f"- Assignment: {cm.get_config('simulator_settings', 'required.assignment')}")

if __name__ == "__main__":
    main()
