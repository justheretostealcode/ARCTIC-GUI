"""program entry point"""

import flet as ft

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

if __name__ == "__main__":
    print("Start GUI")
    ft.app(main)