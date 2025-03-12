

import flet as ft
from data.data_storage import storage
from data.data_storage import storage
from image_generator.plasmid.paraSBOLv.scripts.plasmid_diagram import create_diagram_from_strings
import os

img_width=600,
img_height=150

image = ft.Image(width=img_width, height=img_height)




def plasmid_widget_builder() -> ft.Column:
    """Builds the plasmid widget"""
    
    image.src=os.path.join('ARCTICgui', 'empty.png')
    
    if storage.plasmid_json_path != "":
        store_path = "plasmid_diagram.png"
        create_diagram_from_strings(storage.plasmid_json_path,show=False, output_path=store_path, plasmid_input_type = 'json')
    
        image.src = store_path

    return image


def plasmid_widget_update() -> None:
    """Updates the plasmid widget"""
    plasmid_widget_builder()
    image.update()