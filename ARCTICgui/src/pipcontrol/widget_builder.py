import flet as ft
from custom_controls import container


def widget_builder(page: ft.Page) -> ft.Stack:
    """Generates the widgets making up the pipeline

    Args:
        page (ft.Page): 

    Returns:
        ft.Stack: Stack with Elements
    """

    widget1 = container.PipelineContainer(page, "Context Specification", 20, 100)
    widget2 = container.PipelineContainer(page, "Logic Synthesis", 170, 100)
    widget3 = container.PipelineContainer(page, "Technology Mapping", 320, 20)

    widget4 = container.PipelineContainer(page, "Simulation", 320, 170)
    widget5 = container.PipelineContainer(page, "Plasmid Creation", 470, 20)
    widget6 = container.PipelineContainer(page, "Visualization", 470, 170)

    stack = ft.Stack()
    stack.controls = [widget1, widget2, widget3, widget4, widget5, widget6]
    return stack