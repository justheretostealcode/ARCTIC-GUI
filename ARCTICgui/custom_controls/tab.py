""" File containing classes related to custom tab controls"""
import flet as ft

class PageTab(ft.Tab):
    """ Custom flet.tab class for the 4 general GUI sections"""
    def __init__(self) -> None:
        super().__init__()
