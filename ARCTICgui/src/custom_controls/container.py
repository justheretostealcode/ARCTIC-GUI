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
        self.width = 170
        self.height = 240
        self.border_radius = 10
        
        self.bgcolor = ft.Colors.GREY_500
        self.order = order
        self.inactive_border_color = ft.Colors.GREY_800
        self.active_border_color = "#34608D"

        self.border = ft.border.all(3, self.active_border_color)

    def activate(self, is_active):
        
        if is_active:
            self.border = ft.border.all(3, self.active_border_color)
        
        else:
            self.border = ft.border.all(3, self.inactive_border_color)
