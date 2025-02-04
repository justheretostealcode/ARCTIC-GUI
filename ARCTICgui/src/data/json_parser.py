"""Module for parsing gate library JSON files and extracting device information"""

import json
from typing import List, Dict, Any
from .data_storage import storage  # Use relative import

def find_devices_by_primitive(json_path: str, 
                            primitives: List[str], 
                            fields_to_extract: List[str]) -> List[Dict[str, Any]]:
    """Generic function to find devices with specific primitive identifiers"""
    try:
        # Try different encodings
        encodings = ['utf-8', 'utf-8-sig', 'latin-1']
        data = None
        
        for encoding in encodings:
            try:
                with open(json_path, 'r', encoding=encoding) as file:
                    data = json.load(file)
                break
            except UnicodeDecodeError:
                continue
            except json.JSONDecodeError:
                continue
                
        if data is None:
            raise ValueError("Could not read JSON file with any supported encoding")

        # Find matching devices manually
        results = []
        for device in data:
            if 'primitive_identifier' in device:
                # Check if any of the primitives match
                if any(prim in device['primitive_identifier'] for prim in primitives):
                    # Extract requested fields
                    extracted = {}
                    for field in fields_to_extract:
                        extracted[field] = device.get(field)
                    results.append(extracted)
            
        return results
            
    except FileNotFoundError:
        print(f"Error: Could not find file at {json_path}")
    except Exception as e:
        print(f"Error parsing JSON file: {str(e)}")
        # print(f"Full error: {repr(e)}")
    return []

def update_storage_with_devices(json_path: str) -> None:
    """Find input/output devices and update storage with essential information"""
    devices = find_devices_by_primitive(
        json_path=json_path,
        primitives=["INPUT", "OUTPUT_OR2", "OUTPUT_BUFFER"],
        fields_to_extract=["name", "color", "identifier", "primitive_identifier"]
    )
    
    # print(f"Debug: Found {len(devices)} devices")
    
    # Clear existing data
    storage.input_devices.clear()
    storage.output_devices.clear()
    
    # Update storage with new data
    for device in devices:
        device_id = device['identifier']
        device_info = {
            'name': device['name'],
            'color': device['color']
        }
        
        # print(f"Debug: Processing device {device_id}:")
        # print(f"Debug: - full device data: {device}")
        # print(f"Debug: - primitive_identifier: {device['primitive_identifier']}")
        
        primitive_id = device['primitive_identifier']
        if isinstance(primitive_id, list):
            if 'INPUT' in primitive_id:
                # print(f"Debug: - storing as INPUT")
                storage.input_devices[device_id] = device_info
            elif any(x in primitive_id for x in ['OUTPUT_OR2', 'OUTPUT_BUFFER']):
                # print(f"Debug: - storing as OUTPUT")
                storage.output_devices[device_id] = device_info
        # else:
            # print(f"Debug: Warning - primitive_identifier is not a list: {primitive_id}")
