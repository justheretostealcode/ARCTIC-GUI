
import flet as ft
#  “Logic Circuit Synthesis”, “Manual Design” und “Analysis” und ertelle eine function die sie in eine flet.Tabs classe einfügt. 
class LogicCircuitSynth(ft.Tab):
    def __init__(self):
        super().__init__()
        self.text='Logic Circuit Synthesis'
        self.content=ft.Column(
            spacing=1,
            controls=[
                # TODO: add elements here
            ]
        )

class ManualDesign(ft.Tab):
    def __init__(self):
        super().__init__()
        self.text='Manual Design'
        self.content=ft.Column(
            spacing=1,
            controls=[
                ft.TextField('No Functionality in tab Manual Design')
            ]
        )

class Analysis(ft.Tab):
    def __init__(self):
        super().__init__()
        self.text='Analysis'
        self.content=ft.Column(
            spacing=1,
            controls=[
                ft.TextField('No Functionality in tab Analysis')
            ]
        )

class DesignGoal(ft.Tabs):
    def __init__(self):
        super().__init__()
        self.selected_index = 1
        self.animation_duration = 250
        self.tabs = [
            LogicCircuitSynth(),
            ManualDesign(),
            Analysis(),
        ]
