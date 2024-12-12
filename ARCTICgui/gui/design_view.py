
import flet as ft

class CombinedDesignView(ft.Tab):
    def __init__(self):
        super().__init__()
        self.text='Combined View'
        self.content=ft.Column(
            spacing=1,
            controls=[
                # TODO: add elements here
            ]
        )

class PlasmidView(ft.Tab):
    def __init__(self):
        super().__init__()
        self.text='Plasid View'
        self.content=ft.Column(
            spacing=1,
            controls=[
                ft.TextField('No Functionality in tab Manual Design')
            ]
        )

class SequenceView(ft.Tab):
    def __init__(self):
        super().__init__()
        self.text='Sequence View'
        self.content=ft.Column(
            spacing=1,
            controls=[
                ft.TextField('No Functionality in tab Analysis')
            ]
        )

class DesignView(ft.Tabs):
    def __init__(self):
        super().__init__()
        self.selected_index = 0
        self.animation_duration = 250
        self.tabs = [
            CombinedDesignView(),
            PlasmidView(),
            SequenceView(),
        ]
