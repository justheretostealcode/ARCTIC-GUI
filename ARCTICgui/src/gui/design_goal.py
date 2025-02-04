""" File containing classes related to the design_goal tabs"""
import flet as ft
import sympy    
import os

from custom_controls.tab import PageTab
from custom_controls.tabs import PageTabs
from data.data_storage import storage as st
from data.json_parser import update_storage_with_devices
import pipcontrol.boolean_function as bf
import pipcontrol.syn as syn

from data import data_storage

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
            # First parse the current library
            current_lib = genetic_gate_libraries_dropdown.value
            if not current_lib:
                self.page.show_snack_bar(
                    ft.SnackBar(content=ft.Text("Please select a gate library first"))
                )
                return
                
            json_path = os.path.join("ARCTICsim", "simulator_nonequilibrium", "data", "gate_libs", current_lib)
            
            try:
                update_storage_with_devices(json_path)
                
                if len(st.input_devices) == 0:
                    self.page.show_snack_bar(
                        ft.SnackBar(content=ft.Text("No input devices found in the library"))
                    )
                    return
                
                # Show success message with device count
                self.page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text(f"Successfully found {len(st.input_devices)} input devices"),
                        bgcolor=ft.colors.GREEN_700,
                    )
                )
                    
            except Exception as ex:
                print(f"Error parsing library: {str(ex)}") # Only errors go to terminal
                def close_dialog(e):
                    self.page.dialog.open = False
                    self.page.update()
                
                error_dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Error"),
                    content=ft.Text(f"Error parsing library: {str(ex)}"),
                    actions=[
                        ft.TextButton("OK", on_click=close_dialog),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
                self.page.dialog = error_dialog
                error_dialog.open = True
                self.page.update()
                return

            # Parse and evaluate the user input
            expr = input_expr.value.strip()
            if expr:
                try:
                    expression = sympy.sympify(expr)
                    variables = sorted(expression.atoms(sympy.Symbol), key=lambda x: str(x))
                    dropdowns = []
                    for var in variables:
                        # Create dropdown options from actual input devices
                        options = [
                            ft.dropdown.Option(
                                key=device_id,
                                text=f"{info['name']}" # uncomment if need more info in the dropdown but for short only the name ({device_id})"
                            )
                            for device_id, info in st.input_devices.items()
                        ]
                        
                        dropdown = ft.Dropdown(
                            width=70,
                            height=35,
                            label=str(var),
                            options=options,
                            text_size=14,
                            content_padding=ft.padding.only(left=10, right=20),
                            border_radius=5,
                        )
                        dropdowns.append(dropdown)
                    
                    input_sensor_container.content = ft.Row(
                        controls=dropdowns,
                        spacing=15,
                        alignment=ft.MainAxisAlignment.START,
                    )
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
        
        path_to_gen_lib = os.path.join("ARCTICsim", "simulator_nonequilibrium", "data", "gate_libs")

        def on_dropdown_change(e):
            selected_library = e.control.value
            if selected_library:
                try:
                    # Use os.path.join and then convert to forward slashes
                    library_path = '../' + os.path.join(path_to_gen_lib, selected_library).replace('\\', '/')
                    data_storage.config_manager.update_config('map', 'LIBRARY', library_path)
                    selected_file_display.value = f"Selected library: {selected_library}"
                    self.page.update()
                except ValueError as err:
                    print(f"Error setting library path: {err}")

        # genetic gate library dropdown
        genetic_gate_libraries_dropdown = ft.Dropdown(
            width=300,
            height=35,
            text_size=13,
            content_padding=ft.padding.only(top=2, left=5, right=5, bottom=2),
            border_color=ft.colors.BLUE_400,
            focused_border_color=ft.colors.BLUE_ACCENT,
            focused_border_width=2,
            options=[
                ft.dropdown.Option(
                    genetic_gate_library,
                    text_style=ft.TextStyle(
                        size=13,
                        weight=ft.FontWeight.W_500, 
                    )
                ) 
                for genetic_gate_library in os.listdir(path_to_gen_lib)
            ],
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
        placeholder_path = os.path.join("ARCTICsim", "simulator_nonequilibrium", "data", "gate_libs", "figures_eight-state_det-var_2024-04-04_Monotonicity")

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
            data_storage.images.clear()
            for path in syn.start(f=st.bool_func):
                imgid = '.'.join(os.path.basename(path).split('.')[:-1])
                data_storage.images[imgid] = path
            data_storage.images.update()
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
            ft.Row([ft.TextButton('Synthesis', on_click=start_synth), ft.IconButton(icon=ft.Icons.STOP, on_click=syn.kill_stop)]),
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
