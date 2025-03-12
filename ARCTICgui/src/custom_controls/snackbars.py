""" File containing classes related to Snackbars"""
import flet as ft

class ErrorSnackBar(ft.SnackBar):
    """ Custom flet.Divider class for Snackbars, representing errors"""
    def __init__(self, content = ""):
        super().__init__(content=content)
        self.action_color = ft.Colors.RED

class InfoSnackBar(ft.SnackBar):
    """ Custom flet.Divider class for Snackbars, representing Infos"""
    def __init__(self, content = ""):
        super().__init__(content=content)
