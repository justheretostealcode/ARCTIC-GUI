"""File to build the Pipeline button"""
from pipcontrol.pipeline import arctic_pipeline
import flet as ft

def pipeline_button_builder(page: ft.Page) -> ft.Button:
    """Method to build the UI Elements for the Pipeline start button

    Args:
        page (ft.Page): the current flet page

    Returns:
        ft.Button: The Pipeline Button
    """

    return ft.Row(controls=[ft.TextButton('Pipeline', on_click=arctic_pipeline.start_pipeline),
                             ft.IconButton(icon=ft.Icons.STOP, on_click=arctic_pipeline.stop_pipeline)
                             ], alignment=ft.MainAxisAlignment.CENTER,)
