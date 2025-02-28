""" File containing classes related to custom container controls"""
import flet as ft
from data.data_storage import storage

class PageContainer(ft.Container):
    """ Custom flet.Container class for the 4 general GUI sections"""
    def __init__(self) -> None:
        super().__init__()

        self.expand = True
        self.border = ft.border.all(4, ft.Colors.BLACK38)

class PipelineContainer(ft.Container):
    """Custom flet.Container class for the tiles making up the pipeline"""
    def __init__(self, page:ft.Page, title:str, left:int, top:int, order:int = -1) -> None:
        super().__init__()
        self.page = page
        self.left = left
        self.top = top
        self.border_radius=10
        self.title = title
        self.width = int(page.width / 7)
        self.height = int(page.height /3)
        self.border_radius = 10
        self.border = ft.border.all(4, ft.Colors.BLACK)
        self.bgcolor = ft.Colors.BLUE
        self.order = order
