""" File containing classes related to texts"""

import flet as ft

class StandardText(ft.Text):
    """ Custom flet.Divider class for divider"""
    def __init__(self, value):
        super().__init__(value=value)
        self.color = ft.Colors.GREEN

        self.size=16
        self.color=ft.colors.BLACK