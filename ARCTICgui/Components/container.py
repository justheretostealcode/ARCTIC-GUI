import flet as ft

class PageContainer(ft.Container):
    def __init__(self):
        super().__init__()

        self.expand = True
        self.border = ft.border.all(4, ft.Colors.BLACK38)
