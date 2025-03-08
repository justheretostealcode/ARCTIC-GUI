"""File to build the widgets for the pipeline"""
import flet as ft

import masks
from pipcontrol.pipeline_widget import PipelineWidget
from data.data_storage import storage
from pipcontrol.steps import TechnologyMappingStep, SimulatorStep, SynthesisStep, PlasmidCreationStep


def widget_builder(page: ft.Page) -> ft.Stack:
    """Generates the widgets making up the pipeline

    Args:
        page (ft.Page): The page in which the pipeline steps are implemented

    Returns:
        ft.Stack: Stack with Elements
    """
    syn_step = SynthesisStep(1, masks.synthesis_settings, masks.synthesis_mask)
    tech_map_step = TechnologyMappingStep(2, masks.technology_mapping_settings, masks.technology_mapping_mask)
    sim_step = SimulatorStep(3, masks.default_simulator_settings, masks.default_simulator_mask)
    plasmid_step = PlasmidCreationStep(4, masks.plasmid_settings, masks.plasmid_mask)

    storage.pipeline_steps = [syn_step, tech_map_step, sim_step, plasmid_step]

    pipeline_spacing = 160
    start_spacing = 5
    widget1 = PipelineWidget(page, syn_step, storage.dictionary["Logic_Synthesis"], start_spacing, 10)
    widget2 = PipelineWidget(page, tech_map_step, storage.dictionary["Technology_mapping"], start_spacing + 1 *pipeline_spacing, 10)
    widget3 = PipelineWidget(page, sim_step, storage.dictionary["Simulation"], start_spacing + 2 *pipeline_spacing, 10)
    widget4 = PipelineWidget(page, plasmid_step, storage.dictionary["Plasmid_creation"], start_spacing + 3 *pipeline_spacing, 10)

    stack = ft.Stack()
    stack.controls = [widget1, widget2, widget3, widget4]
    return stack