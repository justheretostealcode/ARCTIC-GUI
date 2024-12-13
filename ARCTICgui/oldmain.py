"""program entry point"""

import flet as ft
import os
from itertools import product
import pipcontrol.syn as syn
import pipcontrol.boolean_function as bf

def main(page: ft.Page) -> None:
    """defines the FLET mainpage

    Args:
        page (ft.Page): standard
    """
    page.title ="ARCTIC"
    page.window.frameless = False

    def open_settings(e):
        print("open settings")

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
                page.update()
            except Exception as ex:
                truth_table_container.content = ft.Text(f"Error: {str(ex)}")
                page.update()
        else:
            truth_table_container.content = ft.Text("Please enter a valid boolean expression.")
            page.update()

    settings_btn = ft.IconButton(ft.Icons.SETTINGS, on_click=open_settings)
    generate_table_btn = ft.ElevatedButton("Generate Truth Table", on_click=show_truth_table)
    truth_table_container = ft.Container()  # here truth table is displayed

    settings_container = ft.Container(content=settings_btn)
    settings_container.alignment = ft.alignment.top_right

    page.add(
        settings_container
    )

    page.add(
        ft.Row(
            [
                ft.TextButton('Synthesis', on_click=lambda e: syn.start(f='a|(b&~c)')), # TODO: Replace argument with input_expr.value.strip()
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


    # Add the input field and button to the page
    page.add(
        ft.Column([
            input_expr,
            generate_table_btn,
            truth_table_container
        ])
    )

if __name__ == "__main__":
    print("Start GUI")
    ft.app(main)
    syn.kill()