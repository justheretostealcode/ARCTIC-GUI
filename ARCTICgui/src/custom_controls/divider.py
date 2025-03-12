""" File containing classes related to custom Divider"""
import flet as ft

class StandardDivider(ft.Divider):
    """ Custom flet.Divider class for divider"""
    def __init__(self):
        super().__init__()
        self.height = 9
        self.thickness = 2
        self.color = ft.Colors.BLACK
        self.leading_indent = 7
        self.trailing_indent = 7