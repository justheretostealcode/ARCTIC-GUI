"""File to build the widgets for the pipeline"""
import flet as ft
from pipcontrol.widgets.pipeline_widget import PipelineWidget
import masks
from data.data_storage import storage
from pipcontrol.pipeline_steps.steps import TechnologyMappingStep, SimulatorStep, SynthesisStep


def widget_builder(page: ft.Page) -> ft.Stack:
    """Generates the widgets making up the pipeline

    Args:
        page (ft.Page): 

    Returns:
        ft.Stack: Stack with Elements
    """
    syn_step = SynthesisStep(1, masks.synthesis_settings, masks.synthesis_mask)
    tech_map_step = TechnologyMappingStep(2, masks.technology_mapping_settings, masks.technology_mapping_mask)
    sim_step = SimulatorStep(3, masks.default_simulator_settings, masks.default_simulator_mask)

    storage.pipeline_steps = [syn_step, tech_map_step, sim_step]

    widget1 = PipelineWidget(page, syn_step, storage.dictionary["Logic_Synthesis"], 10, 10)
    widget2 = PipelineWidget(page, tech_map_step, storage.dictionary["Technology_mapping"], 200, 10)
    widget3 = PipelineWidget(page, sim_step, storage.dictionary["Simulation"], 400, 10)

    stack = ft.Stack()
    stack.controls = [widget1, widget2, widget3]
    return stack