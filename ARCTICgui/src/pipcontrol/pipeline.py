"""File to handle the logic for the pipeline"""
from threading import Thread
from sys import maxsize
from data.data_storage import DataStorage, storage, config_manager, images
import flet as ft
import pipcontrol.syn as syn
from pipcontrol.steps import SimulatorStep, SynthesisStep, TechnologyMappingStep, PlasmidCreationStep
from pipcontrol import sim
from score.score_widget import score_widget_update
from score.plasmid_widget import plasmid_widget_update
from custom_controls.texts import StandardText, ErrorText, WarningText
from custom_controls.snackbars import ErrorSnackBar, InfoSnackBar, WarningSnackBar


class Pipeline():
    """Class to execute the Pipeline logic"""

    def __init__(self, data_storage: DataStorage):
        self.data_storage = data_storage
        self.data_storage.pipeline_is_running = False


    def _start_synth(self) -> None:
        """Method to start the synthesis
        """
        syn.start_synth()


    def _start_technology_mapping(self, circuit_structure_path: str) -> None:
        #Currently not implemented to execute the technology mapping alone
        raise NotImplementedError(storage.dictionary["Technology_mapping"])

    def _start_simulation(self, circuit_structure_path: str, circuit_structure_assignment_path: str) -> list[str]:
        """Method to start the simulation alone

        Args:
            circuit_structure_path (str): path to the simulated structure
            circuit_structure_assignment_path (str): path to the simulated structure-assignment
        """
            
        result = sim.start(circuit_structure_path, circuit_structure_assignment_path)
        storage.score_json_path = result[0]
        storage.plasmid_json_path = result[1]
        score_widget_update()
        return result


    def _start_plasmidCreation(self, circuit_structure_path: str = None, circuit_structure_assignment_path: str = None) -> None:
        """Method to start the plasmid creation alone

        Args:
            circuit_structure_path (str): path to the simulated structure
            circuit_structure_assignment_path (str): path to the simulated structure-assignment
        """

        result = None
        if not circuit_structure_path or not circuit_structure_assignment_path:
            for id in images.ids():
                if id.startswith("result"):
                    anotherpath = images[id]
                    structure = anotherpath.replace(".png", ".json")
                    assignemnt = anotherpath.replace(".png", "_assignment.json")
                    result = self._start_simulation(structure, assignemnt)
        
        else:
            result = self._start_simulation(circuit_structure_path, circuit_structure_assignment_path)

        plasmid_widget_update()

        


    def _start_pipeline_thread(self, e:ft.ControlEvent) -> None:
        """Method to start a seperate thread for the pipeline to avoid stalling the primary thread with the UI"""

        #Warning if not 3 input vars
        if storage.number_of_input_variables != 3:
            e.page.show_snack_bar(
                    WarningSnackBar(content=WarningText(f"{storage.dictionary['Warning_not_3_inputs']}")),
                )

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

                if storage.bool_func == '':
                    raise FileNotFoundError
                
                config_manager.update_config("syn", "SYNTHESIS_PROCEED_WITH_TM", "true")
                syn.start_synth()

                if plasmid_creation_is_active and plasmid_simulator_step:
                    self._start_plasmidCreation()
                    
            except FileNotFoundError:
                e.page.show_snack_bar(
                    ErrorSnackBar(content=ErrorText(f"{storage.dictionary['No_input_provided']}")),
                )

            except Exception as err:
                print(err)
            

        #Case not every step is active
        else:

            try:
                config_manager.update_config("syn", "SYNTHESIS_PROCEED_WITH_TM", "False")
                
                for step in sorted_pipeline_steps:

                    if step.is_active:

                        if isinstance(step, SynthesisStep):
                            self._start_synth()


                        if isinstance(step, TechnologyMappingStep):
                            self._start_technology_mapping(step.path_to_circuit_structure)
                            
                        if isinstance(step, SimulatorStep):
                            self._start_simulation(step.path_to_circuit_structure, step.path_to_circuit_assignment)

                        if isinstance(step, PlasmidCreationStep):
                            self._start_plasmidCreation(step.path_to_circuit_structure, step.path_to_circuit_assignment)

                        else:
                            pass

            except NotImplementedError as err:
                e.page.show_snack_bar(
                    ErrorSnackBar(content=ErrorText(f"{storage.dictionary['Feature_not_implented']}: {err}. {storage.dictionary['turn_all_on']}")),
                )

            except FileNotFoundError as err:
                e.page.show_snack_bar(
                    ErrorSnackBar(content=ErrorText(f"{err}"))
                )


        

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
                    InfoSnackBar(content=StandardText("Pipeline already started."))
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
                    ErrorSnackBar(content=StandardText("Error During pipeline execution."))
                )


arctic_pipeline = Pipeline(storage)
del Pipeline