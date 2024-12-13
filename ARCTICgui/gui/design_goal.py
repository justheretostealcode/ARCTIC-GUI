import flet as ft
from custom_controls.tab import PageTab
from custom_controls.tabs import PageTabs


class LogicCircuitSynth(PageTab):
    def __init__(self):
        super().__init__()

        self.text="Logic Circuit Synthesis"
        self.content = self._contentBuilder()
    
    def _contentBuilder(self) -> ft.Container:
        return ft.Placeholder(color=ft.Colors.random())


class ManualDesign(PageTab):
    def __init__(self):
        super().__init__()
        self.text="Manual Design"
        self.content = self._contentBuilder()
    
    def _contentBuilder(self) -> ft.Container:
        return ft.Placeholder(color=ft.Colors.random())


class Analysis(PageTab):
    def __init__(self):
        super().__init__()
        self.text="Analysis"
        self.content = self._contentBuilder()
    
    def _contentBuilder(self) -> ft.Container:
        return ft.Placeholder(color=ft.Colors.random())


class DesignGoal(PageTabs):
    def __init__(self):
        super().__init__()

        self.tabs = [
            LogicCircuitSynth(),
            ManualDesign(),
            Analysis(),
        ]
