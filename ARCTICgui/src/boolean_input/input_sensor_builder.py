"""File for building"""
# import sys
# import os

# # Append the path of the project root to sys.path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.data_storage import storage, config_manager
from data.json_parser import update_storage_with_devices
import flet as ft
import sympy
import pipcontrol.boolean_function as bf
from custom_controls.text import StandardText


def truth_table_and_sensor_builder(page: ft.Page) -> tuple[ft.ElevatedButton, ft.ElevatedButton, ft.Container]:
    """
    Constructs the user interface components for selecting sensors and generating a truth table based on a Boolean function.
    This function creates two buttons (1st: initiating the display of the truth table, 2nd: selecting input sensors based on 
    the Bool expr provided by the user) and three containers. The function checks the validity of the Boolean expression 
    before any action is taken. If valid, on button click it updates either the truth table container (generate_table_btn) 
    or the input sensors container (enter_and_choose_input_btn). If not valid, a separate container is used to display 
    a respective error message.

    Args:
        page (ft.Page): The current Flet page object where the UI components will be displayed. This object provides
                        context and methods for updating the UI.

    Returns:
        tuple[ft.ElevatedButton, ft.ElevatedButton, ft.Container, ft.Container, ft.Container]: 
            - 1st ElevatedButton is for selecting input sensors.
            - 2nd ElevatedButton is for generating the truth table.
            - 1st Container holds the input sensor selection UI or related messages.
            - 2nd Container is dedicated to displaying the truth table.
            - 3rd Container is used for displaying messages about the validity of the Bool expr or other errors.

    The function ensures that any change in the Boolean expression's validity updates the message container immediately
    and clears out previous outputs from both the input sensor and truth table containers, to ensure no conflicting information.
    """

    #Both buttons and container are build in the same method, because all three elements are interdependent

    input_sensor_container = ft.Container()
    input_sensor_container = ft.Container()
    truth_table_container = ft.Container()  # Dedicated container for the truth table

    def validate_expression():
        expr = storage.bool_func
        if not expr:
            message_container.content = StandardText(storage.dictionary['Please_enter_valid_bool'])
            input_sensor_container.content = ft.Container()
            truth_table_container.content = ft.Container()
        else:
            message_container.content = ft.Container()  # Clear the error message if the expression is valid
        page.update()

        
    def show_truth_table(e:ft.ControlEvent) -> None:
        validate_expression()  # Validate the expression before attempting to display truth table
        expr = storage.bool_func
        if not expr:
            #page.update()
            return

        try:
            truth_table = bf.generate_truth_table_from_expr(expr)
            if not truth_table:
                return

            # Get variable names from first row
            headers = [str(col) for col in truth_table[0][:-1]]  # All but last column
            headers.append(storage.dictionary['Output'])  # Last column is output

            # Create DataTable
            table = ft.DataTable(
                column_spacing=15, 
                columns=[ft.DataColumn(StandardText(header, size=14, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)) for header in headers],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Container(
                                    StandardText(str(int(cell)), size=14, text_align=ft.TextAlign.CENTER),
                                    alignment=ft.alignment.center,
                                    bgcolor=ft.colors.SURFACE_VARIANT if i == len(row) - 1 else None  # Gray background for the last column (function result)
                                )
                            ) for i, cell in enumerate(row)
                        ]
                    ) for row in truth_table[1:]
                ],
            )

            truth_table_container.content = ft.Container(content=table, padding=5)
            page.update()

        except Exception as ex:
            truth_table_container.content = StandardText(f"{storage.dictionary['Error']}: {str(ex)}")
            page.update()
    
    def show_input_sensors_dropdown(e: ft.ControlEvent) -> None:
        # First parse the current library
        json_path = config_manager.get_config("map", "LIBRARY")
        if not json_path:
            page.show_snack_bar(
                ft.SnackBar(content=StandardText(storage.dictionary['Please_select_lib']))
            )
            return

        try:
            json_path = json_path[1:] #remove the first dot of the path

            update_storage_with_devices(json_path)
            
            if len(storage.input_devices) == 0:
                page.show_snack_bar(
                    ft.SnackBar(content=StandardText(storage.dictionary['No_input_dev']))
                )
                return
            
            page.show_snack_bar(
                ft.SnackBar(
                    content=StandardText(f"{storage.dictionary['Successfully_found']} {len(storage.input_devices)} {storage.dictionary['input_devices']}"),
                    bgcolor=ft.colors.GREEN_700,
                )
            )

        except Exception as ex:
            print(f"{storage.dictionary['Error_parsing_library']}: {str(ex)}")

            def close_dialog(e:ft.ControlEvent) -> None:
                page.dialog.open = False
                page.update()
            
            error_dialog = ft.AlertDialog(
                modal=True,
                title=StandardText(storage.dictionary['Error']),
                content=StandardText(f"{storage.dictionary['Error_parsing_library']}: {str(ex)}"),
                actions=[
                    ft.TextButton(storage.dictionary['OK'], on_click=close_dialog),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.dialog = error_dialog
            error_dialog.open = True
            page.update()
            return

        # Parse and evaluate the user input
        validate_expression()  # Validate the expression before showing the dropdowns
        expr = storage.bool_func
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
                            text=f"{info['name']}"
                        )
                        for device_id, info in storage.input_devices.items()
                    ]
                    
                    dropdown = ft.Dropdown(
                        width=65,
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
                page.update()
            except Exception as ex:
                input_sensor_container.content = StandardText(f"{storage.dictionary['Error']}: {str(ex)}")
                page.update()
        else:
            return

    message_container = ft.Container()

    enter_and_choose_input_btn = ft.ElevatedButton(storage.dictionary['Choose_Input_Sensors'], on_click=show_input_sensors_dropdown)
    generate_table_btn = ft.ElevatedButton(storage.dictionary['Truth_table'], on_click=show_truth_table)

    return (enter_and_choose_input_btn, generate_table_btn, input_sensor_container, truth_table_container, message_container)
