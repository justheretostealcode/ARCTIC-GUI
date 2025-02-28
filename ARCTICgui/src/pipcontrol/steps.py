
from data.data_storage import config_manager, storage
from masks import IOType
import flet as ft
from custom_controls.divider import StandardDivider

class Step():
    """Default class representing a step in a pipelin"""
    def __init__(self, order:int = -1, settings: dict = {},
        mask: dict = {}, input_type:IOType = IOType.NOTHING, output_type: IOType = IOType.NOTHING):
        self.settings = settings
        self.order = order
        self.mask = mask
        self.input_type = input_type
        self.output_type = output_type
        self.is_active = True
        self.input_column = ft.Column()


    def on_setting_changed(self, e: ft.ControlEvent) -> None:
        """Method to handle events when a setting for the step is changed

        Args:
            e (ft.ControlEvent): The event calling the method
        """
        pass

    def get_alternative_textfield(self) -> ft.Column:
        """Get container with settings relevant if Step is called in isolation

        Returns:
            ft.Column: Column containing all the settings
        """
        pass
    
    def update_alternative_textfield(self) -> None:
        """Method to update alternative if settings for isolated execution of the step should be updated"""
        pass

class SynthesisStep(Step):
    """Class representing a Synthesis Step"""
    def __init__(self, order:int = -1, settings: dict = {},
        mask: dict = {}, input_type:IOType = IOType.NOTHING, output_type: IOType = IOType.NOTHING):
        super().__init__(order, settings, mask, input_type, output_type)
        self.input_column = ft.Column()


    def on_setting_changed(self,e: ft.ControlEvent) -> None:
        for key, value in storage.dictionary.items():
            if value == e.control.label:
                config_manager.update_config("syn", key, e.control.value.strip())

    def get_alternative_textfield(self) -> ft.Column:
        return self.input_column
    


class TechnologyMappingStep(Step):
    """Class representing a Synthesis Step"""
    def __init__(self, order:int = -1, settings: dict = {},
        mask: dict = {}, input_type:IOType = IOType.NOTHING, output_type: IOType = IOType.NOTHING):
        super().__init__(order, settings, mask, input_type, output_type)
        self.input_column = ft.Column()
        self.path_to_circuit_structure = config_manager.get_config('simulator_settings', 'required.structure')


    def on_setting_changed(self,e: ft.ControlEvent) -> None:
        for key, value in storage.dictionary.items():
            if value == e.control.label:
                config_manager.update_config("map", key, e.control.value.strip())

    def get_alternative_textfield(self) -> ft.Column:
        return self.input_column
    
    def update_alternative_textfield(self) -> None:
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
    """Class representing a Simulator Step"""
    def __init__(self, order:int = -1, settings: dict = {},
        mask: dict = {}, input_type:IOType = IOType.NOTHING, output_type: IOType = IOType.NOTHING):
        super().__init__(order, settings, mask, input_type, output_type)
        self.path_to_circuit_structure = config_manager.get_config('simulator_settings', 'required.structure')
        self.path_to_circuit_assignment = config_manager.get_config('simulator_settings', 'required.assignment')
        self.simulator_path = ""


    def on_setting_changed(self,e: ft.ControlEvent, sim_specific: bool = False) -> None:
        if not sim_specific:
            for key, value in storage.dictionary.items():
                if value == e.control.label:
                    config_manager.update_config("sim", key, e.control.value.strip())
            return

        config_manager.update_config('simulator_settings', e.control.label, e.control.value)


    def get_alternative_textfield(self) -> ft.Column:
        return self.input_column
    
    def update_alternative_textfield(self) -> bool:
        self.input_column.controls.clear()
        prev_step_active = False

        for prev_step in storage.pipeline_steps:
            if  self.order - prev_step.order == 1 and prev_step.is_active: 
                prev_step_active = True
        
        def on_path_to_circuit_structure_change(e: ft.ControlEvent) -> None:
            self.path_to_circuit_structure = e.control.value
        
        def on_path_to_circuit_assignment_change(e: ft.ControlEvent) -> None:
            self.path_to_circuit_assignment = e.control.value


        if not prev_step_active and not isinstance(self, SynthesisStep):
            self.input_column.controls.append( ft.Column(controls=[
                ft.TextField(label=storage.dictionary["path_to_circuit_structure"], 
                             value=self.path_to_circuit_structure, on_change=on_path_to_circuit_structure_change),

                ft.TextField(label=storage.dictionary["path_to_circuit_assignment"], 
                             value=self.path_to_circuit_assignment, on_change=on_path_to_circuit_assignment_change),

                StandardDivider()
                ]))
        
        self.input_column.update()
