"""File to build the widgets for the pipeline"""
import flet as ft
from custom_controls import container


def widget_builder(page: ft.Page) -> ft.Stack:
    """Generates the widgets making up the pipeline

    Args:
        page (ft.Page): 

    Returns:
        ft.Stack: Stack with Elements
    """

    widget1 = container.PipelineContainer(page, "Context", 10, 90, 1)
    widget2 = container.PipelineContainer(page, "Logic Synthesis", 160, 90, 2)
    widget3 = container.PipelineContainer(page, "Tech. Mapping", 310, 10, 3)

    widget4 = container.PipelineContainer(page, "Simulation", 310, 160, 4)
    widget5 = container.PipelineContainer(page, "Plasmid Creation", 460, 10, 5)
    widget6 = container.PipelineContainer(page, "Visualization", 460, 160, 6)

    stack = ft.Stack()
    stack.controls = [widget1, widget2, widget3, widget4, widget5, widget6]
    return stack