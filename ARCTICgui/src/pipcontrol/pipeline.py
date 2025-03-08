"""File to handle the logic for the pipeline"""
from threading import Thread
import sys
from sys import maxsize
from data.data_storage import DataStorage, storage, config_manager
import flet as ft
import pipcontrol.syn as syn
from pipcontrol.steps import SimulatorStep, SynthesisStep, TechnologyMappingStep, PlasmidCreationStep
import os
from subprocess import call


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


    def _start_technology_mapping(self, circuit_structure_path: str) -> None:
        #Currently not implemented to execute the technology mapping alone
        pass

    def _start_simulation(self, circuit_structure_path: str, circuit_structure_assignment_path: str, path_to_simulator: str) -> None:
        """Method to start the simulation alone

        Args:
            circuit_structure_path (str): path to the simulated structure
            circuit_structure_assignment_path (str): path to the simulated structure-assignment
            path_to_simulator (str): path to the choosen simulator
        """

        old_structure = config_manager.get_config('simulator_settings', 'required.structure')
        old_assignment = config_manager.get_config('simulator_settings', 'required.assignment')

        try:
            config_manager.update_config('simulator_settings', 'required.structure', circuit_structure_path)
            config_manager.update_config('simulator_settings', 'required.assignment', circuit_structure_assignment_path)
            
            call([sys.executable, path_to_simulator])


        except Exception as err:
            print(err)

        config_manager.update_config('simulator_settings', 'required.structure', old_structure)
        config_manager.update_config('simulator_settings', 'required.assignment', old_assignment)


    def _start_plasmidCreation(self, circuit_structure_path: str, circuit_structure_assignment_path: str, path_to_simulator: str) -> None:
        """Method to start the plasmid creation alone

        Args:
            circuit_structure_path (str): path to the simulated structure
            circuit_structure_assignment_path (str): path to the simulated structure-assignment
            path_to_simulator (str): path to the choosen simulator
        """
        self._start_simulation(circuit_structure_path, circuit_structure_assignment_path, path_to_simulator)

        

    def _start_pipeline_thread(self, e:ft.ControlEvent) -> None:
        """Method to start a seperate thread for the pipeline to avoid stalling the primary thread with the UI"""

        #sort pipeline steps in order specified by the pipelinewidgets in widget_builder.py
        
        sorted_pipeline_steps = sorted(self.data_storage.pipeline_steps, key=lambda el: el.order if (el.order != -1) else maxsize)

        #Case every step (apart from plasmid creation step) is active
        every_step_is_active = True

        plasmid_creation_is_active = False
        plasmid_simulator_step = None

        for step in sorted_pipeline_steps:

            if not step.is_active and not isinstance(step, PlasmidCreationStep):
                every_step_is_active = False
            
            if isinstance(step, SimulatorStep):
                plasmid_simulator_step = step

            if isinstance(step, PlasmidCreationStep) and step.is_active:
                plasmid_creation_is_active = True


        if every_step_is_active:
            try:
                config_manager.update_config("syn", "SYNTHESIS_PROCEED_WITH_TM", "true")
                syn.start_synth()

                if plasmid_creation_is_active and plasmid_simulator_step:
                    print("Staraartast")
                    current_dir = os.path.dirname(os.path.dirname(__file__))
                    arctic_gui_dir = os.path.dirname(current_dir)
                    arctic_sim_dir = os.path.join(os.path.dirname(arctic_gui_dir), 'ARCTICsim', plasmid_simulator_step.simulator_path, 'main.py')
                    self._start_simulation(plasmid_simulator_step.path_to_circuit_structure, plasmid_simulator_step.path_to_circuit_assignment, arctic_sim_dir)

            except Exception as err:
                print("something went wrong")
            

        #Case not every step is active
        else:
            config_manager.update_config("syn", "SYNTHESIS_PROCEED_WITH_TM", "False")
            
            for step in sorted_pipeline_steps:

                if step.is_active:

                    if isinstance(step, SynthesisStep):
                        syn.start_synth()


                    if isinstance(step, TechnologyMappingStep):
                        self._start_technology_mapping(step.path_to_circuit_structure)
                        

                    if isinstance(step, SimulatorStep):
                        current_dir = os.path.dirname(os.path.dirname(__file__))
                        arctic_gui_dir = os.path.dirname(current_dir)
                        arctic_sim_dir = os.path.join(os.path.dirname(arctic_gui_dir), 'ARCTICsim', step.simulator_path, 'main.py')
                        self._start_simulation(step.path_to_circuit_structure, step.path_to_circuit_assignment, arctic_sim_dir)

                    if isinstance(step, PlasmidCreationStep):
                        current_dir = os.path.dirname(os.path.dirname(__file__))
                        arctic_gui_dir = os.path.dirname(current_dir)
                        arctic_sim_dir = os.path.join(os.path.dirname(arctic_gui_dir), 'ARCTICsim', plasmid_simulator_step.simulator_path, 'main.py')
                        self._start_simulation(step.path_to_circuit_structure, step.path_to_circuit_assignment, arctic_sim_dir)

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

        except Exception:
            e.page.show_snack_bar(
                    ft.SnackBar(content=ft.Text("Error During pipeline execution."))
                )


arctic_pipeline = Pipeline(storage)
del Pipeline