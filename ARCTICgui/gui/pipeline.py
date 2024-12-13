import flet as ft

class GDAPipeline(ft.Container):
    def __init__(self):
        super().__init__()

        self.content = self._contentBuilder()
    
    def _contentBuilder(self) -> ft.Container:
        return ft.Placeholder()
