""" File containing classes related to Snackbars"""
import flet as ft

class ErrorSnackBar(ft.SnackBar):
    """ Custom flet.Divider class for Snackbars, representing errors"""
    def __init__(self, content = ""):
        super().__init__(content=content)

class InfoSnackBar(ft.SnackBar):
    """ Custom flet.Divider class for Snackbars, representing Infos"""
    def __init__(self, content = ""):
        super().__init__(content=content)

class WarningSnackBar(ft.SnackBar):
    """ Custom flet.Divider class for Snackbars, representing Warnings"""
    def __init__(self, content = ""):
        super().__init__(content=content)

