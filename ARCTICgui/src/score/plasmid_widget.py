

import flet as ft
from data.data_storage import storage
from data.data_storage import storage
from image_generator.plasmid.paraSBOLv.scripts.plasmid_diagram import create_diagram_from_strings
import os

img_width=600,
img_height=150

image = ft.Image(width=img_width, height=img_height)




def plasmid_widget_builder(turn_off:bool = False) -> ft.Column:
    """Builds the plasmid widget"""
    # Get absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    empty_img_path = os.path.join(project_root, 'empty.png')
    
    # Check if empty.png exists
    if not os.path.exists(empty_img_path):
        print(f"Warning: Empty image not found at {empty_img_path}")
        empty_img_path = os.path.join(os.path.dirname(project_root), 'empty.png')
    
    # Use absolute path
    image.src = empty_img_path
    
    if storage.plasmid_json_path != "" and not turn_off:
        # Save plasmid diagram to project root using absolute path
        store_path = os.path.join(project_root, "plasmid_diagram.png")
        create_diagram_from_strings(storage.plasmid_json_path, show=False, output_path=store_path, plasmid_input_type='json')
    
        image.src = store_path

    return image


def plasmid_widget_update(turn_off:bool = False) -> None:
    """Updates the plasmid widget"""
    plasmid_widget_builder(turn_off)
    image.update()