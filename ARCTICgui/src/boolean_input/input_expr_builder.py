"""File responsible for building the boolean expression textfield and the info button"""
import flet as ft
from data.data_storage import storage
from custom_controls.text import StandardText


def input_expr_builder(page: ft.Page) -> ft.TextField:
    """
    Builds a text field where users can enter a Boolean expression. This text field updates the global storage
    with the user's input every time a change is made, ensuring that the latest expression is always stored and accessible.

    Args:
        page (ft.Page): The current Flet page object where the text field will be displayed. This object provides
                        context and methods for handling user inputs and updating the UI.

    Returns:
        ft.TextField: A Flet text field component configured to accept and process Boolean expression inputs.
                      It features a label with instructions, centered text alignment, and an event handler that updates
                      storage with the content of the text field whenever the user makes changes.

    This text field for collecting the Boolean expression will be used by other components of the application,
    such as generating truth tables or selecting input sensors based on the Boolean logic defined by the user.
    """
    def textbox_changed(e:ft.ControlEvent) -> None:
        storage.bool_func = e.control.value.strip()

    input_expr = ft.TextField(
        label=storage.dictionary["Enter_Boolean_Function"],
        width=200, text_align=ft.TextAlign.CENTER, on_change=textbox_changed
        )

    return input_expr


def info_input_builder(page: ft.Page) -> ft.IconButton:
    """
    Creates an information button that, when clicked, opens a modal dialog window containing detailed information
    about how to enter a Boolean expression. This includes explanations of allowable operators, operand formats, and
    general guidelines that help users format their expressions correctly.

    Args:
        page (ft.Page): The current Flet page object where the information button will be displayed. This object provides
                        context and methods for managing UI elements like dialogs and buttons.

    Returns:
        ft.IconButton: A Flet icon button configured to display an info icon. When clicked, it opens a modal dialog
                       with details on constructing a Boolean expression correctly, including operator list and operand formats.
    """
    def handle_close(e:ft.ControlEvent) -> None:
        page.close(bool_info_window)

    bool_info_window = ft.AlertDialog(
        modal=True,
        title=StandardText(storage.dictionary["Information"]),
        content = StandardText(storage.dictionary["Enter_bool"] + "\n" 
                          + storage.dictionary["operant_list"]  + ". \n" 
                          +  storage.dictionary["operands_written_format"]),
        actions=[
            ft.TextButton(storage.dictionary["Close"], on_click=handle_close),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    return ft.IconButton(icon=ft.Icons.INFO_OUTLINE_ROUNDED, on_click=lambda e: page.open(bool_info_window))
