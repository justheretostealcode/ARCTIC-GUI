""" File containing classes related to custom container controls"""
import flet as ft

class PageContainer(ft.Container):
    """ Custom flet.Page class for the 4 general GUI sections"""
    def __init__(self) -> None:
        super().__init__()

        self.expand = True
        self.border = ft.border.all(4, ft.Colors.BLACK38)
