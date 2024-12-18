""" File containing classes related to the pipeline tabs"""
import flet as ft

class GDAPipeline(ft.Container):
    """Class representing the Container related to the GDA Pipeline"""
    def __init__(self) -> None:
        super().__init__()

        self.content = self.content_builder()

    def content_builder(self) -> ft.Column:
        """Generic method to build the Content of the GDAPipeline class

        Returns:
            ft.Column: Column with GDAPipeline controls
        """
        return ft.Placeholder()
