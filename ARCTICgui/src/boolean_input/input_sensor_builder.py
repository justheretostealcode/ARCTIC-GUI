"""File for building"""
from data.data_storage import storage, config_manager
from data.json_parser import update_storage_with_devices
import flet as ft
import sympy
import pipcontrol.boolean_function as bf


def truth_table_and_sensor_builder(page: ft.Page) -> tuple[ft.ElevatedButton, ft.ElevatedButton, ft.Container]:
    """Method to build the truthtable or sensor selection, depending on which button is selected

    Args:
        page (ft.Page): current page

    Returns:
        tuple[ft.ElevatedButton, ft.ElevatedButton, ft.Container]: the inputsensor button, the truthtable button, the container, holding the value
    """

    #Both buttons and container are build in the same method, because all three elements are interdependent

    input_sensor_container = ft.Container()
    def show_truth_table(e:ft.ControlEvent) -> None:
        expr = storage.bool_func
        if not expr:
            input_sensor_container.content = ft.Text(storage.dictionary["Please_enter_valid_bool"])
            page.update()
            return

        try:
            truth_table = bf.generate_truth_table_from_expr(expr)
            if not truth_table:
                return

            # Get variable names from first row
            headers = [str(col) for col in truth_table[0][:-1]]  # All but last column
            headers.append(storage.dictionary["Output"])  # Last column is output

            # Create DataTable
            table = ft.DataTable(
                column_spacing=15, 
                columns=[ft.DataColumn(ft.Text(header, size=14, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)) for header in headers],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Container(
                                    ft.Text(str(int(cell)), size=14, text_align=ft.TextAlign.CENTER),
                                    alignment=ft.alignment.center,
                                    bgcolor=ft.colors.SURFACE_VARIANT if i == len(row) - 1 else None  # Gray background for the last column (function result)
                                )
                            ) for i, cell in enumerate(row)
                        ]
                    ) for row in truth_table[1:]
                ],
            )

            input_sensor_container.content = ft.Container(content=table, padding=5)
            page.update()

        except Exception as ex:
            input_sensor_container.content = ft.Text(f"{storage.dictionary["Error"]}: {str(ex)}")
            page.update()
    
    def show_input_sensors_dropdown(e: ft.ControlEvent) -> None:
        # First parse the current library
        json_path = config_manager.get_config("map", "LIBRARY")
        if not json_path:
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text(storage.dictionary["Please_select_lib"]))
            )
            return

        try:
            json_path = json_path[1:] #remove the first dot of the path

            update_storage_with_devices(json_path)
            
            if len(storage.input_devices) == 0:
                page.show_snack_bar(
                    ft.SnackBar(content=ft.Text(storage.dictionary["No_input_dev"]))
                )
                return
            
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(f"{storage.dictionary["Successfully_found"]} {len(storage.input_devices)} {storage.dictionary["input_devices"]}"),
                    bgcolor=ft.colors.GREEN_700,
                )
            )

        except Exception as ex:
            print(f"{storage.dictionary["Error_parsing_library"]}: {str(ex)}")

            def close_dialog(e:ft.ControlEvent) -> None:
                page.dialog.open = False
                page.update()
            
            error_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text(storage.dictionary["Error"]),
                content=ft.Text(f"{storage.dictionary["Error_parsing_library"]}: {str(ex)}"),
                actions=[
                    ft.TextButton(storage.dictionary["OK"], on_click=close_dialog),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.dialog = error_dialog
            error_dialog.open = True
            page.update()
            return

        # Parse and evaluate the user input
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
                input_sensor_container.content = ft.Text(f"{storage.dictionary["Error"]}: {str(ex)}")
                page.update()
        else:
            input_sensor_container.content = ft.Text(storage.dictionary["Please_enter_valid_bool"])
            page.update()

    enter_and_choose_input_btn = ft.ElevatedButton(storage.dictionary["Choose_Input_Sensors"], on_click=show_input_sensors_dropdown)
    generate_table_btn = ft.ElevatedButton(storage.dictionary["Truth_table"], on_click=show_truth_table)

    return (enter_and_choose_input_btn, generate_table_btn, input_sensor_container)