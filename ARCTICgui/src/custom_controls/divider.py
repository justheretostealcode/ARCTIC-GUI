""" File containing classes related to custom Divider"""
import flet as ft

class StandardDivider(ft.Divider):
    """ Custom flet.Divider class for divider"""
    def __init__(self):
        super().__init__()
        self.height = 9
        self.thickness = 3
        self.color = ft.Colors.BLACK