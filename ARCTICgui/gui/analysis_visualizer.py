""" File containing classes related to the analysis_visualizer tabs"""
import flet as ft
from custom_controls.tab import PageTab
from custom_controls.tabs import PageTabs

class TransientBehaviour(PageTab):
    """Class representing the Container related to the TransientBehaviour"""
    def __init__(self) -> None:
        super().__init__()

        self.text = "Transient Behaviour"
        self.content = self.content_builder()

    def content_builder(self) -> ft.Column:
        """Generic method to build the Content of the TransientBehaviour class

        Returns:
            ft.Column: Column with TransientBehaviour controls
        """
        return ft.Placeholder(color=ft.Colors.random())


class SteadyStateBehaviour(PageTab):
    """Class representing the Container related to the SteadyStateBehaviour"""
    def __init__(self) -> None:
        super().__init__()

        self.text = "Steady State Behaviour"
        self.content = self.content_builder()

    def content_builder(self) -> ft.Column:
        """Generic method to build the Content of the SteadyStateBehaviour class

        Returns:
            ft.Column: Column with SteadyStateBehaviour controls
        """
        return ft.Placeholder(color=ft.Colors.random())


class HazardAnalysis(PageTab):
    """Class representing the Container related to the HazardAnalysis"""
    def __init__(self) -> None:
        super().__init__()

        self.text = "Hazard Analysis"
        self.content = self.content_builder()

    def content_builder(self) -> ft.Column:
        """Generic method to build the Content of the HazardAnalysis class

        Returns:
            ft.Column: Column with HazardAnalysis controls
        """
        return ft.Placeholder()


class AnalysisVisualizer(PageTabs):
    """Class representing the Container related to the AnalysisVisualizer"""
    def __init__(self) -> None:
        super().__init__()

        self.tabs = [
            TransientBehaviour(),
            SteadyStateBehaviour(),
            HazardAnalysis()
        ]
