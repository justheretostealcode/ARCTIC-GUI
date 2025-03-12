import flet as ft
import json
from data.data_storage import storage


content_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
score_column = ft.Column(controls= [content_row], alignment=ft.MainAxisAlignment.CENTER)

def score_widget_builder() -> ft.Column:    
    """Builds the score widget"""
    if storage.score_json_path != "":
        
        score_list = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

        with open(storage.score_json_path) as f:
            score_dict = json.load(f)
            for partial_score in score_dict:
                score_list.controls.append(
                    ft.Text(f"{storage.dictionary[partial_score]}: {score_dict[partial_score]}")
                )

        placeholder_text = score_list

    else:
        placeholder_text = ft.Text(storage.dictionary["Placeholder_score"])

    content_row.controls=[placeholder_text]

    return score_column

def score_widget_update() -> None:
    """Updates the score widget"""
    score_widget_builder()
    score_column.update()