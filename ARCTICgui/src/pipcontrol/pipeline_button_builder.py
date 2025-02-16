"""File to build the Pipeline button"""
from pipcontrol.pipeline import arctic_pipeline
from data.data_storage import storage
import flet as ft


def pipeline_button_builder(page: ft.Page) -> ft.Button:
    """Method to build the UI Elements for the Pipeline start button

    Args:
        page (ft.Page): the current flet page

    Returns:
        ft.Button: The Pipeline Button
    """

    return ft.Row(controls=[ft.TextButton(storage.dictionary["Start_pipeline"], on_click=arctic_pipeline.start_pipeline),
                             ft.IconButton(icon=ft.Icons.STOP, on_click=arctic_pipeline.stop_pipeline)
                             ], alignment=ft.MainAxisAlignment.CENTER,)
