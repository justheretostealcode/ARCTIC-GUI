"""
Path configuration for ParaSBOLv.
Ensures the ParaSBOLv library is properly found.
"""
import sys
import os

# Get the parent directory of the current script's directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add it to the Python path if it's not already there
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
