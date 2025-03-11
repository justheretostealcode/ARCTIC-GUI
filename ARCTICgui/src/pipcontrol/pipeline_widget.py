
import flet as ft
from custom_controls.container import PipelineContainer
from custom_controls.divider import StandardDivider
from data.data_storage import storage, config_manager
from pipcontrol.steps import Step, SimulatorStep, SynthesisStep, TechnologyMappingStep, PlasmidCreationStep
from masks import IOType

class PipelineWidget(PipelineContainer):
    """Custom flet.Container class for the tiles making up the pipeline"""
    def __init__(self, page:ft.Page, step: Step, title:str = "",
                  left:int = 0, top:int = 0) -> None:
        super().__init__(page, title, left, top, step.order)

        self.step = step
        self.simulator_options_container = ft.Column()
        self.content = self.content_builder()
        

    def content_builder(self) -> ft.Container:
        """_summary_

        Returns:
            ft.Container: Single Widget containing all settings for a pipeline step
        """
        
        title_text = ft.Text(value=self.title)
        title_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[title_text])

        #Add on/off switch
        def on_switch_change(e: ft.ControlEvent) -> None:
            self.step.is_active = e.control.value

            #If switch gets switched check if alternative input fields are required by other steps
            for step in storage.pipeline_steps:
                step.update_alternative_textfield()
            
            e.page.update()

        switch_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
        

        on_off_switch_description = ft.Text(value=storage.dictionary["On_Off_switch_description"])
        switch = ft.Switch(
            value=True,
            on_change= on_switch_change
        )

        switch_row.controls = [on_off_switch_description,switch]

        #Control to hold additional settings if previous steps are inactive
        alternative_input = self.step.get_alternative_textfield()

       
        contents = [title_row,StandardDivider(), switch_row, StandardDivider(), alternative_input]

        #Add other step/specific option
        for setting, IOtype  in self.step.settings.items():

            if setting in self.step.mask and self.step.mask[setting]:
                continue

            match IOtype:

                case IOType.SIMULATOR: 
                    simulators = config_manager.get_available_simulators()
                    
                    selected_sim = None
                    for simulator in simulators:
                        if simulator in self.step.simulator_path:
                            selected_sim = simulator

                    def get_options():
                        options = []
                        for simulator in simulators:
                            options.append(
                                ft.dropdown.Option(
                                    key=simulator,
                                    content=ft.Text(
                                        value=simulator,
                                    ),
                                )
                            )
                        return options

                    def on_dropdown_change(e: ft.ControlEvent) -> None:

                        #set new path in arctic
                        newpath = f"../ARCTICsim/{e.control.value}"

                        config_manager.update_config("sim", "SIM_PATH", newpath)
                        self.step.simulator_path = newpath

                        #create new Settings for current simulator
                        self.simulator_options_container.controls.clear()
                        
                        sim_specific_settings = config_manager.reload_simulator_settings()

                        for setting, current_value in sim_specific_settings.items():
                            
                            self.simulator_options_container.controls.append(
                                ft.TextField(label=storage.dictionary[setting], on_change= lambda e:  self.step.on_setting_changed(e, True),
                                            value=current_value)
                                )
                        e.page.update()

                    dd = ft.Dropdown(
                        label=storage.dictionary["SIMULATOR"],
                        options=get_options(),
                        value=selected_sim,
                        on_change=on_dropdown_change
                    )
                    content = dd
                    contents.append(content)

                case _:

                    if isinstance(self.step, SimulatorStep):
                        content = ft.TextField(label=storage.dictionary[setting], on_change= self.step.on_setting_changed,
                                           value=config_manager.get_config('sim', setting))
                        contents.append(content)
                    
                    if isinstance(self.step, SynthesisStep):
                        content = ft.TextField(label=storage.dictionary[setting], on_change= self.step.on_setting_changed,
                                           value=config_manager.get_config('syn', setting))
                        contents.append(content)
                    
                    if isinstance(self.step, TechnologyMappingStep):
                        content = ft.TextField(label=storage.dictionary[setting], on_change= self.step.on_setting_changed,
                                           value=config_manager.get_config('map', setting))
                        contents.append(content)
                    
                    if isinstance(self.step, PlasmidCreationStep):
                        content = ft.TextField(label=storage.dictionary[setting], on_change= self.step.on_setting_changed,
                                           value=config_manager.get_config('map', setting))
                        contents.append(content)
                        
                    
        #special case for simulator Add simulator specific arguments
        if isinstance(self.step, SimulatorStep):
            contents.append(StandardDivider())
            contents.append(self.simulator_options_container)

        content_column = ft.Column(contents)
        content_column.scroll = True
        inner = ft.Container(content=content_column)

        return inner