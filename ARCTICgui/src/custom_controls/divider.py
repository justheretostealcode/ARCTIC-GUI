import flet as ft

class StandardDivider(ft.Divider):

    def __init__(self):
        super().__init__()
        self.height = 9
        self.thickness = 3
        self.color = ft.Colors.BLACK