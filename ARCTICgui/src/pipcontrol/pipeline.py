"""File to handle the logic for the pipeline"""
from threading import Thread
from sys import maxsize
from data.data_storage import DataStorage, storage as st
import flet as ft
import pipcontrol.syn as syn


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

    def _start_pipeline_thread(self, e:ft.ControlEvent) -> None:
        """Method to start a seperate thread for the pipeline to avoid stalling the primary thread with the UI"""

        #sort pipeline steps in order specified by the pipelinewidgets in widget_builder.py
        sorted_pipeline_steps = sorted(self.data_storage.pipeline_steps_active.items(), key=lambda el: el[1][0] if (el[1][0] != -1) else maxsize)

        for step in sorted_pipeline_steps:
            step_name = step[0]
            step_is_active = step[1][1]

            if step_is_active:

                match step_name:

                    case "Context":
                        pass

                    case 'Logic Synthesis':

                        try:
                            syn.start_synth()

                        except Exception as err:
                            raise SynthesisError(err) from err

                    case 'Tech. Mapping':
                        pass

                    case 'Simulation':
                        pass

                    case 'Plasmid Creation':
                        pass

                    case 'Visualization':
                        pass

                    case _:
                        pass

        self.data_storage.pipeline_is_running = False

        e.control.text = st.dictionary["Start_pipeline"]
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
        e.control.text = st.dictionary["Pipeline_running"]
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

arctic_pipeline = Pipeline(st)
del Pipeline
