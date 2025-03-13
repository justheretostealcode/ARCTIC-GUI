"""file building the genetic library selection dropdown menu and the responding images"""
import os
import flet as ft
from data.data_storage import storage, config_manager
from custom_controls.texts import StandardText

def genetic_gate_library_builder(page: ft.Page) -> tuple[ft.GridView, ft.Container]:
    """Method to build the gate library dropdown menu and the 

    Args:
        page (ft.Page): _description_

    Returns:
        tuple[ft.GridView, ft.Container]: _description_
    """

    # Define project root path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    arctic_sim_dir = os.path.join(os.path.dirname(project_root), 'ARCTICsim')
    
    path_to_gen_lib = os.path.join(arctic_sim_dir, "simulator_nonequilibrium", "data", "gate_libs")

    selected_file_display = StandardText(storage.dictionary['Select_a_library'])

    def on_dropdown_change(e:ft.ControlEvent) -> None:
        selected_library = e.control.value
        if selected_library:
            try:
                # Use os.path.join and then convert to forward slashes
                library_path = '../' + os.path.join(path_to_gen_lib, selected_library).replace('\\', '/')
                config_manager.update_config('map', 'LIBRARY', library_path)
                selected_file_display.value = f"{storage.dictionary['Selected_library']}: {selected_library}"
                load_images()
                page.update()
            except ValueError as err:
                print(f"{storage.dictionary['Error_setting_library_path']}: {err}")

        # Get list of libraries if directory exists
    available_libraries = []
    if os.path.exists(path_to_gen_lib):
        available_libraries = os.listdir(path_to_gen_lib)
    else:
        print(f"Warning: Gate libraries directory not found at {path_to_gen_lib}")

    # genetic gate library dropdown
    genetic_gate_libraries_dropdown = ft.Dropdown(
        width=300,
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
        on_change=on_dropdown_change,
        value=os.path.basename(config_manager.get_config('map', 'LIBRARY')),
    )

    images = ft.GridView(
        expand=1,
        runs_count=5,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
        )

    def load_images() -> None:
        # Clear previous images
        images.controls.clear()
        
        ## A BIG TODO is to fix for the case where other simulateros are implied. Now the nonequilibrium simulator's path is hardcoded
        # We also didn't manage to come to the unified way to handle paths so that it would work with all operating systems so thats a big L
        # But i hope i'll get the chance to fix it before the joint meeting
        placeholder_path = os.path.join(arctic_sim_dir, "simulator_nonequilibrium", "data", "gate_libs", "figures_eight-state_det-var_2024-04-04_Monotonicity")
        
        if not os.path.exists(placeholder_path):
            print(f"Warning: Images directory not found at {placeholder_path}")
            return
        
        for filename in os.listdir(placeholder_path):
            # Get absolute path for image
            image_path = os.path.abspath(os.path.join(placeholder_path, filename))
            images.controls.append(
                ft.Image(
                    src=image_path,
                    width=200,
                    height=200
                )
            )
    load_images()

    return (ft.Container(
            content=ft.Column([
            genetic_gate_libraries_dropdown,
            selected_file_display
        ]),
        ),
        images)
