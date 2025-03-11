""" File containing classes related to the design_view tabs"""
import flet as ft
import os

from custom_controls.tabs import PageTabs
from custom_controls.tab import PageTab
from data import data_storage
from data.data_storage import storage


class CombinedDesignView(PageTab):
    """Class representing the flet.tab related to the CombinedDesignView"""
    def __init__(self) -> None:
        super().__init__()

        data_storage.images.register(self.dataUpdate)

        self.text= storage.dictionary["Hazard_Analysis"]
        self.content = self.content_builder()

    def content_builder(self) -> ft.Column:
        """Generic method to build the content of the CombinedDesignView class

        Returns:
            ft.Column: Column with CombinedDesignView controls
        """
        
        self.LogicCircuit = ft.Image(
            src=os.path.join('ARCTICgui', 'empty.png'),
            width=200,
            height=200,
        )
        self.Selections=ft.Dropdown(
            on_change=self.on_click
        )
        controls = [
            self.Selections,
            self.LogicCircuit,
        ]
        return ft.Column(controls=controls)
    def dataUpdate(self):
        self.Selections.options.clear()
        tmp=data_storage.images.ids()
        
        tmp = sorted(tmp, key=lambda k: (0, k)if k.startswith('result')else(1, k))
        self.Selections.options.extend([ft.dropdown.Option(item) for item in tmp])
        self.Selections.value = tmp[0] if len(tmp)>1 else ''
        
        self.Selections.update()
        self.on_click(None)
    def on_click(self, _):
        if self.Selections.value == '':
            self.LogicCircuit.src = os.path.join('ARCTICgui', 'empty.png')
        elif self.Selections.value not in data_storage.images.ids():
            raise Exception(f'{storage.dictionary["unknown_value"]}: "{self.Selections.value}"') # should be imposable
        else:
            ipf = data_storage.images[self.Selections.value]
            self.LogicCircuit.src = ipf
        self.LogicCircuit.update()

class PlasmidView(PageTab):
    """Class representing the flet.tab related to the PlasmidView"""
    def __init__(self) -> None:
        super().__init__()

        self.text = storage.dictionary["Plasmid_View"]
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

        self.text=storage.dictionary["Sequence_View"]
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

        self.text = storage.dictionary["Protocol_View"]
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
            #Not Implemented yet
            #PlasmidView(),
            #SequenceView(),
            #ProtocolView()
        ]
