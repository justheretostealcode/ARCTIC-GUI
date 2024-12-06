"""program entry point"""

import flet as ft
import os

import pipcontroll.syn as syn

def main(page: ft.Page) -> None:
    """defines the FLET mainpage

    Args:
        page (ft.Page): standard
    """
    page.title ="ARCTIC"
    page.window.frameless = False

    def open_settings(e):
        print("open settings")

    settings_btn = ft.IconButton(ft.Icons.SETTINGS, on_click=open_settings)

    settings_container = ft.Container(content=settings_btn)
    settings_container.alignment = ft.alignment.top_right
    
    page.add(
        settings_container
    )

    
    page.add(
        ft.Row(
            [
                ft.TextButton('Synthesis', on_click=lambda e: syn.start(f='a|(b&~c)')), # TODO: Replace argument
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

if __name__ == "__main__":
    print("Start GUI")
    ft.app(main)
    syn.kill()