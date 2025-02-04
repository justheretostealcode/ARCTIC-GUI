"""Test script for json_parser functionality"""
import sys
from pathlib import Path

# Add the parent directory to Python path to make modules visible
sys.path.append(str(Path(__file__).parent.parent))

from data.json_parser import find_devices_by_primitive, update_storage_with_devices
from data.data_storage import storage  # This will now get the same instance

def test_parser():
    """Test function to check parser functionality"""
    # Use absolute path to the JSON file
    json_path = Path(__file__).parent.parent.parent.parent / "ARCTICsim" / "simulator_nonequilibrium" / "data" / "gate_libs" / "gate_lib_yeast_generated_mean_fit_2024-03-11.json"
    
    if not json_path.exists():
        print(f"Error: JSON file not found at {json_path}")
        return
        
    print(f"Using JSON file: {json_path}")
    
    print("Testing device search...")
    
    # Test general device search
    devices = find_devices_by_primitive(
        json_path=str(json_path),  # Convert Path to string
        primitives=["INPUT", "OUTPUT_OR2", "OUTPUT_BUFFER"],
        fields_to_extract=["name", "color", "identifier", "primitive_identifier"]
    )
    
    # print(f"\nRaw devices data:")
    # for device in devices:
    #     print(f"Device details: {device}")
    
    # print("\nFound devices:")
    # for device in devices:
    #     print(f"Name: {device['name']}, Type: {device['primitive_identifier']}")
    
    # Test storage update
    # print("\nTesting storage update...")
    update_storage_with_devices(str(json_path))  # Convert Path to string
    
    # print("\nChecking storage contents:")
    print(f"Input devices count: {len(storage.input_devices)}")
    print(f"Output devices count: {len(storage.output_devices)}")
    
    print("\nInput devices in storage:")
    for device_id, info in storage.input_devices.items():
        print(f"ID: {device_id}, Name: {info['name']}, Color: {info['color']}")
    
    print("\nOutput devices in storage:")
    for device_id, info in storage.output_devices.items():
        print(f"ID: {device_id}, Name: {info['name']}, Color: {info['color']}")

if __name__ == "__main__":
    test_parser()
