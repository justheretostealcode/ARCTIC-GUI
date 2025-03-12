""" File containing classes related to texts"""

import flet as ft

class StandardText(ft.Text):
    """ Custom ft.Text class for Text"""
    def __init__(self, value):
        super().__init__(value=value)
        self.size=16
        self.color=ft.colors.BLACK


class ErrorText(ft.Text):
    """ Custom ft.Text class for Text"""
    def __init__(self, value):
        super().__init__(value=value)
        self.size=16
        self.color=ft.colors.RED

class WarningText(ft.Text):
    """ Custom ft.Text class for Text"""
    def __init__(self, value):
        super().__init__(value=value)
        self.size=16
        self.color=ft.colors.YELLOW