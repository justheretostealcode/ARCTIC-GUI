""" File containing classes related to the design_view tabs"""
import flet as ft
from custom_controls.tabs import PageTabs
from custom_controls.tab import PageTab

class CombinedDesignView(PageTab):
    """Class representing the flet.tab related to the CombinedDesignView"""
    def __init__(self) -> None:
        super().__init__()

        self.text="Combined View"
        self.content = self.content_builder()

    def content_builder(self) -> ft.Column:
        """Generic method to build the content of the CombinedDesignView class

        Returns:
            ft.Column: Column with CombinedDesignView controls
        """
        return ft.Placeholder(color=ft.Colors.random())


class PlasmidView(PageTab):
    """Class representing the flet.tab related to the PlasmidView"""
    def __init__(self) -> None:
        super().__init__()

        self.text="Plasmid View"
        self.content = self.content_builder()

    def content_builder(self) -> ft.Column:
        """Generic method to build the content of the PlasmidView class

        Returns:
            ft.Column: Column with PlasmidView controls
        """
        return ft.Placeholder(color=ft.Colors.random())


class SequenceView(PageTab):
    """Class representing the flet.tab related to the SequenceView"""
    def __init__(self) -> None:
        super().__init__()

        self.text="Sequence View"
        self.content = self.content_builder()

    def content_builder(self) -> ft.Column:
        """Generic method to build the content of the SequenceView class

        Returns:
            ft.Column: Column with SequenceView controls
        """
        return ft.Placeholder(color=ft.Colors.random())


class ProtocolView(PageTab):
    """Class representing the flet.tab related to the ProtocolView"""
    def __init__(self) -> None:
        super().__init__()

        self.text = "Protocol View"
        self.content = self.content_builder()

    def content_builder(self) -> ft.Column:
        """Generic method to build the content of the ProtocolView class

        Returns:
            ft.Column: Column with ProtocolView controls
        """
        return ft.Placeholder(color=ft.Colors.random())


class DesignView(PageTabs):
    """Class representing the flet.tabs related to the DesignView"""
    def __init__(self) -> None:
        super().__init__()

        self.tabs = [
            CombinedDesignView(),
            PlasmidView(),
            SequenceView(),
            ProtocolView()
        ]
