""" File containing classes related to custom appbar controls"""
import flet as ft

class GUIAppBar(ft.AppBar):
    """ Custom flet.AppBar class"""
    def __init__(self) -> None:
        super().__init__()
        self.title = ft.Text("ARCTIC-GUI")
