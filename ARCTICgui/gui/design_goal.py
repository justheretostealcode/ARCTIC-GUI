""" File containing classes related to the design_goal tabs"""
import flet as ft
from custom_controls.tab import PageTab
from custom_controls.tabs import PageTabs

import pipcontrol.boolean_function as bf
import pipcontrol.syn as syn


class LogicCircuitSynth(PageTab):
    """Class representing the flet.tab related to the LogicCircuitSynth"""
    def __init__(self, page: ft.Page) -> None:
        super().__init__()

        self.page = page
        self.text="Logic Circuit Synthesis"
        self.content_builder()

    def content_builder(self) -> ft.Column:
        """Generic method to build the content of the LogicCircuitSynth class

        Returns:
            ft.Container: Column with LogicCircuitSynth controls
        """
        # Create a text field for user input --> in desgin_goal mit strip fct zum rausziehen
        input_expr = ft.TextField(label="Enter Boolean Function", width=200, text_align=ft.TextAlign.CENTER)

        def show_truth_table(e):
            # Parse and evaluate the user input
            expr = input_expr.value.strip()
            if expr:
                try:
                    #parse the user expression into a truth table
                    truth_table = bf.generate_truth_table_from_expr(expr)
                    table_content = []
                    for row in truth_table:
                        table_content.append(ft.Text(f"{' | '.join(map(str, row))}"))
                    truth_table_container.content = ft.Column(table_content)
                    self.page.update()
                except Exception as ex:
                    truth_table_container.content = ft.Text(f"Error: {str(ex)}")
                    self.page.update()
            else:
                truth_table_container.content = ft.Text("Please enter a valid boolean expression.")
                self.page.update()

        generate_table_btn = ft.ElevatedButton("Generate Truth Table", on_click=show_truth_table)
        truth_table_container = ft.Container()  # here truth table is displayed


        def start_synth(e:ft.ControlEvent):
            if not isinstance((button:=e.control), ft.TextButton):
                return
            if button.text != 'Synthesis':
                return
            button.text = 'Running syn&tm'
            button.update()
            syn.start(f=input_expr.value.strip())
            button.text = 'Synthesis'
            button.update()
        
        self.content = ft.Column([
            input_expr, #input for boolean function
            generate_table_btn,  #button to generate truth table based on input
            truth_table_container, #the container for the generated truth table
            ft.TextButton('Synthesis', on_click=start_synth), 
        ])

class ManualDesign(PageTab):
    """Class representing the flet.tab related to the ManualDesign"""
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.text="Manual Design"
        self.content = self.content_builder()

    def content_builder(self) -> ft.Column:
        """Generic method to build the content of the ManualDesign class
        Returns:
            ft.Column: Column with ManualDesign controls
        """
        return ft.Placeholder(color=ft.Colors.random())


class Analysis(PageTab):
    """Class representing the flet.tab related to the Analysis"""
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.text="Analysis"
        self.content = self.content_builder()

    def content_builder(self) -> ft.Column:
        """Generic method to build the content of the Analysis class

        Returns:
            ft.Column: Column with Analysis controls
        """
        return ft.Placeholder(color=ft.Colors.random())


class DesignGoal(PageTabs):
    """Class representing the flet.tabs related to the DesignGoal"""
    def __init__(self, page: ft.Page):
        super().__init__()

        self.tabs = [
            LogicCircuitSynth(page),
            ManualDesign(page),
            Analysis(page),
        ]
