"""File responsible for building the boolean expression textfield and the info button"""
import flet as ft
from data.data_storage import storage


def input_expr_builder(page: ft.Page) -> ft.TextField:
    """Method to build the input textfield

    Args:
        page (ft.Page): current page
    """

    def textbox_changed(e:ft.ControlEvent) -> None:
        storage.bool_func = e.control.value.strip()

    input_expr = ft.TextField(
        label=storage.dictionary["Enter_Boolean_Function"],
        width=200, text_align=ft.TextAlign.CENTER, on_change=textbox_changed
        )

    return input_expr


def info_input_builder(page: ft.Page) -> ft.IconButton:
    """_summary_

    Args:
        page (ft.Page): _description_
    """
    def handle_close(e:ft.ControlEvent) -> None:
        page.close(bool_info_window)

    bool_info_window = ft.AlertDialog(
        modal=True,
        title=ft.Text(storage.dictionary["Information"]),
        content = ft.Text(storage.dictionary["Enter_bool"] + "\n" 
                          + storage.dictionary["operant_list"]  + ". \n" 
                          +  storage.dictionary["operands_written_format"]),
        actions=[
            ft.TextButton(storage.dictionary["Close"], on_click=handle_close),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    return ft.IconButton(icon=ft.Icons.INFO_OUTLINE_ROUNDED, on_click=lambda e: page.open(bool_info_window))
