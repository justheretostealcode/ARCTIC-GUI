""" File containing classes related to the pipeline tabs"""
import flet as ft
from pipcontrol import widget_builder

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

        stack = widget_builder.widget_builder(self.page)
        return stack
