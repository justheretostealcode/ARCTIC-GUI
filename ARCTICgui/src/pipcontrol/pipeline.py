"""File to handle the logic for the pipeline"""
from threading import Thread
from sys import maxsize
from data.data_storage import DataStorage, storage, config_manager
import flet as ft
import pipcontrol.syn as syn
from pipcontrol.pipeline_steps.steps import SimulatorStep, SynthesisStep, TechnologyMappingStep
import os


class Pipeline():
    """Class to execute the Pipeline logic"""


    def __init__(self, data_storage: DataStorage):
        self.data_storage = data_storage
        self.data_storage.pipeline_is_running = False


    def _start_synth(self, e:ft.ControlEvent) -> None:
        """Method to start the synthesis

        Args:
            e (ft.ControlEvent): Event that triggers the pipeline start
        """

        syn.start_synth()

    def _start_technology_mapping(self, circuit_structure_path):
        print(circuit_structure_path)

    def _start_simulation(self, circuit_structure_path, circuit_structure_assignment_path, path_to_simulator):

        old_structure = config_manager.get_config('simulator_settings', 'required.structure')
        old_assignment = config_manager.get_config('simulator_settings', 'required.assignment')

        try:
            config_manager.update_config('simulator_settings', 'required.structure', circuit_structure_path)
            config_manager.update_config('simulator_settings', 'required.assignment', circuit_structure_assignment_path)
            
            absolute_path = os.path.abspath(path_to_simulator)
            current_file_path =  os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

            absolute_path = os.path.join(current_file_path, "ARCTICsim", path_to_simulator.split("/")[2], "main.py")

            os.system(absolute_path)


            
        except Exception as err:
            pass

        config_manager.update_config('simulator_settings', 'required.structure', old_structure)
        config_manager.update_config('simulator_settings', 'required.assignment', old_assignment)

        

    def _start_pipeline_thread(self, e:ft.ControlEvent) -> None:
        """Method to start a seperate thread for the pipeline to avoid stalling the primary thread with the UI"""

        #sort pipeline steps in order specified by the pipelinewidgets in widget_builder.py
        
        sorted_pipeline_steps = sorted(self.data_storage.pipeline_steps, key=lambda el: el.order if (el.order != -1) else maxsize)

        #Case every step is active
        every_step_is_active = True

        for step in sorted_pipeline_steps:
            if not step.is_active:
                every_step_is_active = False

        if every_step_is_active:
            try:
                config_manager.update_config("syn", "SYNTHESIS_PROCEED_WITH_TM", "True")
                config_manager.update_config("map", "STATISTICS", "FALSE") #mit anton besprechen
                syn.start_synth()

            except Exception as err:
                raise SynthesisError(err) from err

        else:
            config_manager.update_config("syn", "SYNTHESIS_PROCEED_WITH_TM", "False")

            #Case not every step is active
            for step in sorted_pipeline_steps:

                if step.is_active:

                    if isinstance(step, SynthesisStep):
                        try:
                            syn.start_synth()

                        except Exception as err:
                            raise SynthesisError(err) from err

                    if isinstance(step, TechnologyMappingStep):
                        try:
                            self._start_technology_mapping(step.path_to_circuit_structure)
                        
                        except Exception as err:
                            raise SynthesisError(err) from err

                    if isinstance(step, SimulatorStep):
                        try:
                            self._start_simulation(step.path_to_circuit_structure, step.path_to_circuit_assignment, step.simulator_path)
                        
                        except Exception as err:
                            raise SynthesisError(err) from err

                    else:
                        pass

        self.data_storage.pipeline_is_running = False

        e.control.text = storage.dictionary["Start_pipeline"]
        e.page.update()


    def stop_pipeline(self, e: ft.ControlEvent) -> None:
        """Method to stop the execution for a pipeline

        Args:
            e (ft.core.control_event.ControlEvent): Event triggering the stop_pipeline method
        """
        syn.kill()


    def start_pipeline(self, e: ft.ControlEvent) -> None:
        """Method to start the Pipeline from a different thread

        Args:
            e (ft.ControlEvent): event starting the Pipeline
        """

        if self.data_storage.pipeline_is_running:
            e.page.show_snack_bar(
                    ft.SnackBar(content=ft.Text("Pipeline already started."))
                )
            return
        
        self.data_storage.pipeline_is_running = True    
        e.control.text = storage.dictionary["Pipeline_running"]
        e.page.update()

        pipline_thread = Thread(target=self._start_pipeline_thread, args=[e])

        try:
            pipline_thread.start()

        except SynthesisError:
            e.page.show_snack_bar(
                    ft.SnackBar(content=ft.Text("Error During pipeline execution."))
                )


class SynthesisError(Exception):
    """Error representing a failure during the synthesis pipeline-step"""
    def __init__(self, err):            
        super().__init__(str(err))
        self.error = err

arctic_pipeline = Pipeline(storage)
del Pipeline
