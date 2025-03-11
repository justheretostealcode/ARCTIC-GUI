"""program entry point"""

import os
import sys
import flet as ft

from pipcontrol import syn
from gui.design_goal import DesignGoal
from gui.design_view import DesignView
from gui.pipeline_view import GDAPipeline
from gui.analysis_visualizer import AnalysisVisualizer
from data.data_storage import storage, config_manager
from custom_controls.container import PageContainer


PYTHON_PATH = sys.executable

if sys.platform == "win32":
    PYTHON_PATH = PYTHON_PATH.replace("\\", "\\\\")

if not os.path.isabs(config_manager.get_config('sim', 'PYTHON_BINARY')):
    config_manager.update_config('sim', 'PYTHON_BINARY', PYTHON_PATH)


def main(page: ft.Page) -> None:
    """Entry point for the Flet program

    Args:
        page (ft.Page): standard
    """

    #General flet.page settings
    page.title = storage.dictionary["PAGE_TITLE"]
    page.window.frameless = False
    page.theme_mode = ft.ThemeMode.LIGHT

    page.window.width = config_manager.get_config("gui", "START_WIDTH")
    page.window.height = config_manager.get_config("gui", "START_HEIGHT")

    upper_row = ft.Row()
    lower_row = ft.Row()

    upper_row.expand = True
    lower_row.expand = True

    design_goal = DesignGoal(page)
    design_view = DesignView()
    gda_pipeline = GDAPipeline(page)
    analysis_visualizer =AnalysisVisualizer()

    container_top_left = PageContainer()
    container_top_right = PageContainer()
    container_bottom_left = PageContainer()
    container_bottom_right = PageContainer()

    container_top_left.expand = 50
    container_top_right.expand = 50
    container_bottom_left.expand = 70
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
    syn.kill()
