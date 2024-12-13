import flet as ft
from custom_controls.tab import PageTab
from custom_controls.tabs import PageTabs

class TransientBehaviour(PageTab):
    def __init__(self):
        super().__init__()

        self.text = "Transient Behaviour"
        self.content = self._contentBuilder()
    
    def _contentBuilder(self) -> ft.Container:
        return ft.Placeholder(color=ft.Colors.random())


class SteadyStateBehaviour(PageTab):
    def __init__(self):
        super().__init__()

        self.text = "Steady State Behaviour"
        self.content = self._contentBuilder()
    
    def _contentBuilder(self) -> ft.Container:
        return ft.Placeholder(color=ft.Colors.random())


class HazardAnalysis(PageTab):
    def __init__(self):
        super().__init__()

        self.text = "Hazard Analysis"
        self.content = self._contentBuilder()
    
    def _contentBuilder(self) -> ft.Container:
        return ft.Placeholder()


class AnalysisVisualizer(PageTabs):
    def __init__(self):
        super().__init__()

        self.tabs = [
            TransientBehaviour(),
            SteadyStateBehaviour(),
            HazardAnalysis()
        ]
