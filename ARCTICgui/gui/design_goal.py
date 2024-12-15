import flet as ft
from custom_controls.tab import PageTab
from custom_controls.tabs import PageTabs

import pipcontrol.boolean_function as bf


class LogicCircuitSynth(PageTab):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.page = page
        self.text="Logic Circuit Synthesis"
        self.contentBuilder()
    
    def contentBuilder(self) -> ft.Container:
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


        self.content = ft.Column([
            input_expr,
            generate_table_btn,
            truth_table_container,
            ft.TextButton('Synthesis', on_click=lambda e: syn.start(f='a|(b&~c)')), # TODO: Replace argument with input_expr.value.strip()
        ])

class ManualDesign(PageTab):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.text="Manual Design"
        self.content = self._contentBuilder()
    
    def _contentBuilder(self) -> ft.Container:
        return ft.Placeholder(color=ft.Colors.random())


class Analysis(PageTab):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.text="Analysis"
        self.content = self._contentBuilder()
    
    def _contentBuilder(self) -> ft.Container:
        return ft.Placeholder(color=ft.Colors.random())


class DesignGoal(PageTabs):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.tabs = [
            LogicCircuitSynth(page),
            ManualDesign(page),
            Analysis(page),
        ]
