""" File containing classes related to custom appbar controls"""
import flet as ft
from custom_controls.text import StandardText
class GUIAppBar(ft.AppBar):
    """ Custom flet.AppBar class"""
    def __init__(self) -> None:
        super().__init__()
        self.title = StandardText("ARCTIC-GUI")
