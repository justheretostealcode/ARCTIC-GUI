""" File containing classes related to the pipeline tabs"""
import flet as ft
from pipcontrol.widget_builder import widget_builder
from pipcontrol.pipeline_button_builder import pipeline_button_builder

class GDAPipeline(ft.Container):
    """Class representing the Container related to the GDA Pipeline"""
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.page = page
        self.content = self.content_builder()


    def content_builder(self) -> ft.Column:
        """Generic method to build the Content of the GDAPipeline class

        Returns:
            ft.Column: Column with GDAPipeline controls
        """

        stack_widget = widget_builder(self.page)

        start_pipeline_button = pipeline_button_builder(self.page)
        stack_widget.expand = 15
        start_pipeline_button.expand = 2

        result = ft.Column(controls=[stack_widget, start_pipeline_button])

        return result
