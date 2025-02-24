
from data.data_storage import config_manager, storage
from masks import IOType
import flet as ft
from custom_controls.divider import StandardDivider

class Step():
    def __init__(self, order:int = -1, settings: dict = {},
        mask: dict = {}, input_type:IOType = IOType.NOTHING, output_type: IOType = IOType.NOTHING):
        self.settings = settings
        self.order = order
        self.mask = mask
        self.input_type = input_type
        self.output_type = output_type
        self.is_active = True
        self.input_column = ft.Column()


    def is_ready(self):
        pass

    def on_setting_changed(self):
        pass

    def get_alternative_textfield(self):
        return self.input_column
    
    def update_alternative_textfield(self):
        pass

class SynthesisStep(Step):
    def __init__(self, order:int = -1, settings: dict = {},
        mask: dict = {}, input_type:IOType = IOType.NOTHING, output_type: IOType = IOType.NOTHING):
        super().__init__(order, settings, mask, input_type, output_type)


    def on_setting_changed(self,e: ft.ControlEvent):
        for key, value in storage.dictionary.items():
            if value == e.control.label:
                config_manager.update_config("syn", key, e.control.value.strip())


class TechnologyMappingStep(Step):
    def __init__(self, order:int = -1, settings: dict = {},
        mask: dict = {}, input_type:IOType = IOType.NOTHING, output_type: IOType = IOType.NOTHING):
        super().__init__(order, settings, mask, input_type, output_type)
        self.input_column = ft.Column()
        self.path_to_circuit_structure = config_manager.get_config('simulator_settings', 'required.structure')

    def is_ready(self):
        return True

    def on_setting_changed(self,e: ft.ControlEvent):
        for key, value in storage.dictionary.items():
            if value == e.control.label:
                config_manager.update_config("map", key, e.control.value.strip())

    def get_alternative_textfield(self):
        return self.input_column
    
    def update_alternative_textfield(self) -> bool:
        self.input_column.controls.clear()
        prev_step_active = False

        for prev_step in storage.pipeline_steps:
            if  self.order - prev_step.order == 1 and prev_step.is_active: 
                prev_step_active = True

        def on_path_to_circuit_structure_change(e):
            self.path_to_circuit_structure = e.control.value
        
        if not prev_step_active and not isinstance(self, SynthesisStep):
            self.input_column.controls.append( ft.Column(controls=[ft.TextField(label=storage.dictionary["path_to_circuit_structure"],
                             value=self.path_to_circuit_structure, on_change=on_path_to_circuit_structure_change),
                StandardDivider()
                ]))
        
        self.input_column.update()

class SimulatorStep(Step):
    def __init__(self, order:int = -1, settings: dict = {},
        mask: dict = {}, input_type:IOType = IOType.NOTHING, output_type: IOType = IOType.NOTHING):
        super().__init__(order, settings, mask, input_type, output_type)
        self.path_to_circuit_structure = config_manager.get_config('simulator_settings', 'required.structure')
        self.path_to_circuit_assignment = config_manager.get_config('simulator_settings', 'required.assignment')
        self.simulator_path = ""


    def on_setting_changed(self,e: ft.ControlEvent, sim_specific: bool = False):

        if not sim_specific:
            for key, value in storage.dictionary.items():
                if value == e.control.label:
                    config_manager.update_config("sim", key, e.control.value.strip())
            return
        
        config_manager.update_config('simulator_settings', e.control.label, e.control.value)
    
    def is_ready(self):
        return True

    def get_alternative_textfield(self):
        return self.input_column
    
    def update_alternative_textfield(self) -> bool:
        self.input_column.controls.clear()
        prev_step_active = False

        for prev_step in storage.pipeline_steps:
            if  self.order - prev_step.order == 1 and prev_step.is_active: 
                prev_step_active = True
        
        def on_path_to_circuit_structure_change(e):
            self.path_to_circuit_structure = e.control.value
        
        def on_path_to_circuit_assignment_change(e):
            self.path_to_circuit_assignment = e.control.value


        if not prev_step_active and not isinstance(self, SynthesisStep):
            self.input_column.controls.append( ft.Column(controls=[
                ft.TextField(label=storage.dictionary["path_to_circuit_structure"], 
                             value=self.path_to_circuit_structure, on_change=on_path_to_circuit_structure_change),

                ft.TextField(label=storage.dictionary["path_to_circuit_assignment"], 
                             value=self.path_to_circuit_assignment, on_change=on_path_to_circuit_assignment_change),

                StandardDivider()
                ]
                ))
        
        self.input_column.update()
