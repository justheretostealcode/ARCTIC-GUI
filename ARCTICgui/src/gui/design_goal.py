""" File containing classes related to the design_goal tabs"""
import flet as ft

from custom_controls.tab import PageTab
from custom_controls.tabs import PageTabs
from data.data_storage import storage
from boolean_input import input_expr_builder
from boolean_input import input_sensor_builder
from gate_library_selection import genetic_gate_library_builder

class LogicCircuitSynth(PageTab):
    """Class representing the flet.tab related to the LogicCircuitSynth"""
    def __init__(self, page) -> None:
        super().__init__()

        self.page = page
        self.text= storage.dictionary["Logic_Circuit_Synthesis"]
        self.content = self.content_builder()

    def content_builder(self) -> ft.Column:
        """Generic method to build the content of the LogicCircuitSynth class

        Returns:
            ft.Container: Column with LogicCircuitSynth controls
        """
        


        input_expr = input_expr_builder.input_expr_builder(self.page)
        input_info_button = input_expr_builder.info_input_builder(self.page)
        #truth_table, sensor_dropdowns, input_sensor_container = input_sensor_builder.truth_table_and_sensor_builder(self.page)
        truth_table_btn, sensor_dropdowns_btn, input_sensor_container, truth_table_container, message_container = input_sensor_builder.truth_table_and_sensor_builder(self.page)

        #right side
        main_right_column = ft.Column(
            [ft.Row([input_expr, input_info_button]),
            ft.Row([truth_table_btn, sensor_dropdowns_btn]),
            message_container,
            input_sensor_container,
            truth_table_container,
            ])
        
        gglibrary_container, images = genetic_gate_library_builder.genetic_gate_library_builder(self.page)

        #left side
        main_left_column = ft.Column([gglibrary_container,
            images]
        )

        main_right_column.scroll = ft.ScrollMode.ALWAYS
        main_left_column.scroll = ft.ScrollMode.ALWAYS

        main_right_column.expand = True
        main_left_column.expand = True

        return ft.Row([main_left_column, main_right_column])


class ManualDesign(PageTab):
    """Class representing the flet.tab related to the ManualDesign"""
    def __init__(self) -> None:
        super().__init__()
        self.text= storage.dictionary["Manual_Design"]
        self.content = self.content_builder()

    def content_builder(self) -> ft.Column:
        """Generic method to build the content of the ManualDesign class
        Returns:
            ft.Column: Column with ManualDesign controls
        """
        return ft.Placeholder(color=ft.Colors.random())


class Analysis(PageTab):
    """Class representing the flet.tab related to the Analysis"""
    def __init__(self) -> None:
        super().__init__()
        self.text= storage.dictionary["Analysis"]
        self.content = self.content_builder()

    def content_builder(self) -> ft.Column:
        """Generic method to build the content of the Analysis class

        Returns:
            ft.Column: Column with Analysis controls
        """
        return ft.Placeholder(color=ft.Colors.random())


class DesignGoal(PageTabs):
    """Class representing the flet.tabs related to the DesignGoal"""
    def __init__(self, page):
        super().__init__()

        self.tabs = [
            LogicCircuitSynth(page),
            ManualDesign(),
            Analysis(),
        ]
