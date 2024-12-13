import flet as ft

class GUIAppBar(ft.AppBar):
    def __init__(self):
        super().__init__()
        self.title = ft.Text("ARCTIC-GUI")
