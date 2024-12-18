""" File containing classes related to custom tabs controls"""
import flet as ft

class PageTabs(ft.Tabs):
    """ Custom flet.tabs class for the 4 general GUI sections"""
    def __init__(self) -> None:
        super().__init__()

        self.selected_index = 0
        self.animation_duration = 250
