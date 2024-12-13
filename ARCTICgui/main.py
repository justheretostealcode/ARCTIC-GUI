"""program entry point"""

from gui.design_goal import DesignGoal
from gui.design_view import DesignView
from gui.pipeline import GDAPipeline
from gui.analysis_visualizer import AnalysisVisualizer

from Components.container import PageContainer
from Components.appbar import GUIAppBar

import flet as ft

def main(page: ft.Page) -> None:
    """defines the FLET mainpage

    Args:
        page (ft.Page): standard
    """

    page.title ="ARCTIC"
    page.window.frameless = False
    page.theme_mode = ft.ThemeMode.LIGHT

    page.appbar = GUIAppBar()

    upper_row = ft.Row()
    lower_row = ft.Row()

    upper_row.expand = True
    lower_row.expand = True

    design_goal = DesignGoal()
    design_view = DesignView()
    gda_pipeline = GDAPipeline()
    analysis_visualizer =AnalysisVisualizer()

    container_top_left = PageContainer()
    container_top_right = PageContainer()
    container_bottom_left = PageContainer()
    container_bottom_right = PageContainer()

    container_top_left.expand = 50
    container_top_right.expand = 50
    container_bottom_left.expand = 50
    container_bottom_right.expand = 50

    container_top_left.content = design_goal
    container_top_right.content = design_view
    container_bottom_left.content = gda_pipeline
    container_bottom_right.content = analysis_visualizer

    upper_row.controls = [container_top_left, container_top_right]
    lower_row.controls = [container_bottom_left, container_bottom_right]

    page.add(
        upper_row,
        lower_row
    )

    page.update()


if __name__ == "__main__":
    ft.app(main)
