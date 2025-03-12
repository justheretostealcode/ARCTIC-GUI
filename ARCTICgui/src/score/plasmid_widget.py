

import flet as ft
from data.data_storage import storage
from custom_controls.texts import StandardText
from data.data_storage import storage
from image_generator.plasmid.paraSBOLv.scripts.plasmid_diagram import create_diagram_from_strings

content_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
plasmid_column = ft.Column(controls= [content_row], alignment=ft.MainAxisAlignment.CENTER)

def plasmid_widget_builder() -> ft.Column:
    """Builds the plasmid widget"""
    
    placeholder_text = StandardText("")
    if storage.plasmid_json_path != "":
        store_path = "plasmid_diagram.png"
        create_diagram_from_strings(storage.plasmid_json_path,show=False, output_path=store_path, plasmid_input_type = 'json')
    
        placeholder_text = ft.Image(
                    src=store_path,
                    width=600,
                    height=200,
                    fit=ft.ImageFit.CONTAIN,
                )

    content_row.controls=[placeholder_text]

    return plasmid_column


def plasmid_widget_update() -> None:
    """Updates the plasmid widget"""
    plasmid_widget_builder()
    plasmid_column.update()