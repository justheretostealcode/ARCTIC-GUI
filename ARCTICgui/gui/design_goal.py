""" File containing classes related to the design_goal tabs"""
import flet as ft
from custom_controls.tab import PageTab
from custom_controls.tabs import PageTabs
import os
from data.data_storage import storage as st

import pipcontrol.boolean_function as bf
import pipcontrol.syn as syn
import sympy    




class LogicCircuitSynth(PageTab):
    """Class representing the flet.tab related to the LogicCircuitSynth"""
    def __init__(self) -> None:
        super().__init__()

        self.page = ft.Page
        self.text="Logic Circuit Synthesis"
        self.content = self.content_builder()

    def content_builder(self) -> ft.Column:
        """Generic method to build the content of the LogicCircuitSynth class

        Returns:
            ft.Container: Column with LogicCircuitSynth controls
        """

        def textbox_changed(e):
            st.bool_func = e.control.value.strip()

        # Create a text field for user input --> in desgin_goal mit strip fct zum rausziehen
        input_expr = ft.TextField(label="Enter Boolean Function", width=200, text_align=ft.TextAlign.CENTER, on_change=textbox_changed)

        #trying out alert dialogue
        def handle_close(e):
            self.page.close(bool_info_window)
        
        bool_info_content_column = ft.Column([
            ft.Text("Enter the boolean function with any variables of up to three."),
            ft.Text("Use the common operands:"),
            ft.Text("- AND (&) - for logical conjunction"),
            ft.Text("- OR (|) - for logical disjunction"),
            ft.Text("- NOT (~) - for logical negation"),
            ft.Text("- XOR (^) - for exclusive disjunction"),
            ft.Text("- Implication (~a|b) - for logical implication")
        ])

        bool_info_window = ft.AlertDialog(
            modal=True,
            title=ft.Text("Information"),
            #content= bool_info_content_column, 
            content = ft.Text("Enter the boolean function with any variables of up to three and the common operands: AND (&), OR (|), NOT (~), XOR (^), Implication (~ a| b)."),
            actions=[
                ft.TextButton("Close", on_click=handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            #on_dismiss=lambda e: self.page.add(ft.Text("Modal dialog dismissed"),),
        )

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
                    input_sensor_container.content = ft.Column(table_content)
                    self.page.update()
                except Exception as ex:
                    input_sensor_container.content = ft.Text(f"Error: {str(ex)}")
                    self.page.update()
            else:
                input_sensor_container.content = ft.Text("Please enter a valid boolean expression.")
                self.page.update()
        
        def show_input_sensors_dropdown(e):
            # Parse and evaluate the user input
            expr = input_expr.value.strip()
            if expr:
                try:
                    expression = sympy.sympify(expr)
                    variables = sorted(expression.atoms(sympy.Symbol), key=lambda x: str(x))
                    dropdowns = []
                    for var in variables:
                        dropdown = ft.Dropdown(
                            width= 60, #TODO relative!!
                            #width=main_left_column.width*(1/len(variables)),
                            label=str(var),
                            options=[
                                ft.dropdown.Option("Lac"),
                                ft.dropdown.Option("Tet"),
                                ft.dropdown.Option("Tac"),
                                ft.dropdown.Option("Ph")
                            ],
                        )
                        dropdowns.append(dropdown)
                    input_sensor_container.content = ft.Row(dropdowns)
                    self.page.update()
                except Exception as ex:
                    input_sensor_container.content = ft.Text(f"Error: {str(ex)}")
                    self.page.update()
            else:
                input_sensor_container.content = ft.Text("Please enter a valid boolean expression.")
                self.page.update()

        enter_and_choose_input_btn = ft.ElevatedButton("Choose Input Sensors", on_click=show_input_sensors_dropdown)
        generate_table_btn = ft.ElevatedButton("Truth Table", on_click=show_truth_table)
        input_sensor_container = ft.Container()  # here input sensor dropdowns are is displayed
        truth_table_container = ft.Container()  # here truth table is displayed
        
        # CODE TO BE ADDED
        selected_file_display = ft.Text("Select a library:", size=14, color=ft.colors.BLUE_700)
        # Dropdown to select a file
        def on_dropdown_change(e):
            #Update the selected file display when an option is chosen.
            selected_file_display.value = f"Selected library: {e.control.value}"
            self.page.update()

        # genetic gate library dropdown
        path_to_gen_lib = os.path.join('ARCTICsim', 'thermo_libs', 'evaluation', 'dirichlet')
        genetic_gate_libraries_dropdown = ft.Dropdown(
            width=300,
            height=35,
            options=[ft.dropdown.Option(genetic_gate_library) for genetic_gate_library in os.listdir(path_to_gen_lib)],
            on_change=on_dropdown_change
        )

        #Generate Image in GUI for every activation curve


        gglibrary_container = ft.Container(
            content=ft.Column([
            genetic_gate_libraries_dropdown,
            selected_file_display  # Display the selected file
        ]),
        )

        #Todo: get Diagrams from valid path
        placeholder_path =  os.path.join('ARCTICsim', 'gate_libs', 'plots_id_cytometry_01')

        images = ft.GridView(
        expand=1,
        runs_count=5,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
    )
        
        for filename in os.listdir(placeholder_path):
            images.controls.append(
                ft.Image(
                    src=os.path.join(placeholder_path, filename),
                    width=200,
                    height=200
                )
            )


        def start_synth(e:ft.ControlEvent):
            if not isinstance((button:=e.control), ft.TextButton):
                return
            if button.text != 'Synthesis':
                return
            button.text = 'Running syn&tm'
            button.update()
            syn.start(f=st.bool_func)
            button.text = 'Synthesis'
            button.update()
        
        #left side
        main_left_column = ft.Column(
            [ft.Row([input_expr, #input for boolean function
            ft.IconButton(icon=ft.Icons.INFO_OUTLINE_ROUNDED, on_click=lambda e: self.page.open(bool_info_window))]),
            ft.Row([enter_and_choose_input_btn, #enter boolean expression and choose input sensors from dropdown
            generate_table_btn]),  #button to generate truth table based on input
            input_sensor_container,#the container for the input sensor selection
            truth_table_container, #the container for the generated truth table
            ft.TextButton('Synthesis', on_click=start_synth)
            ])
        

        #right side
        main_right_column = ft.Column([gglibrary_container, #ft.Text("Select a FILE: "),
            images]
        )

        #so that content doesn't overflow, but is scrollable
        main_left_column.scroll = ft.ScrollMode.ALWAYS #to hide scrollbar, exchange ALWAYS for AUTO
        main_right_column.scroll = ft.ScrollMode.ALWAYS

        main_left_column.expand = True
        main_right_column.expand = True

        return ft.Row([main_left_column, main_right_column])




class ManualDesign(PageTab):
    """Class representing the flet.tab related to the ManualDesign"""
    def __init__(self) -> None:
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
    def __init__(self) -> None:
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
    def __init__(self):
        super().__init__()

        self.tabs = [
            LogicCircuitSynth(),
            ManualDesign(),
            Analysis(),
        ]
