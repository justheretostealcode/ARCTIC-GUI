
import flet as ft
from Components.tabs import PageTabs
from Components.tab import PageTab

class CombinedDesignView(PageTab):
    def __init__(self):
        super().__init__()

        self.text="Combined View"
        self.content = self._contentBuilder()
    
    def _contentBuilder(self) -> ft.Container:
        return ft.Placeholder(color=ft.Colors.random())


class PlasmidView(PageTabs):
    def __init__(self):
        super().__init__()

        self.text="Plasid View"
        self.content = self._contentBuilder()
    
    def _contentBuilder(self) -> ft.Container:
        return ft.Placeholder(color=ft.Colors.random())


class SequenceView(PageTab):
    def __init__(self):
        super().__init__()

        self.text="Sequence View"
        self.content = self._contentBuilder()
    
    def _contentBuilder(self) -> ft.Container:
        return ft.Placeholder(color=ft.Colors.random())


class DesignView(PageTabs):
    def __init__(self):
        super().__init__()

        self.tabs = [
            CombinedDesignView(),
            PlasmidView(),
            SequenceView(),
        ]
