import flet as ft

class PageTabs(ft.Tabs):
    def __init__(self):
        super().__init__()

        self.selected_index = 0
        self.animation_duration = 250
