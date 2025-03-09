
import pathlib
import json
import sys
import os

from data.data_storage import storage, config_manager
import flet as ft


def start(struct_path:str, assign_path:str)->list[str]:
    '''
    f:
        is a boolean function using the variables a, b & c and the operators ~, & and |
    tt:
        a truth table as string of 8 1's or 0's
        a  10101010
        b  11001100
        c  11110000
        tt 10011001
    mc:
        path to map.config for ARCTICsyn
    sync:
        path to syn.config for ARCTICsyn
    simc:
        path to sim.config for ARCTICsyn
    
    starts is a process that runs synthesis if no other process exists
    
    return:
        a list of paths in the output dictionary of new files
    '''
    
    sim_path = config_manager.get_config('sim', 'SIM_PATH')[1:]
    sim_scrips = config_manager.get_config('sim', 'SIM_SCRIPT')[:-3]
    
    struct_path = pathlib.Path(struct_path).absolute().as_posix()
    assign_path = pathlib.Path(assign_path).absolute().as_posix()

    with open(assign_path, 'r') as file:
        data = json.load(file)
    if data.get('valid', False):
        data = data['identifierMap']
        assign_path = assign_path[:-5]+'_sim'+assign_path[-5:]
        with open(assign_path, 'w+') as file:
            json.dump(data, file)
        
    
    root = os.path.abspath('./')
    sys.path.insert(0, sim_path)
    
    def sim_main(sim):

        # change working directory to here
        sim.os.chdir(sim.here)

        # load default settings first
        sim.settings, sim.types, sim.comments = sim.load_settings(sim.settings_config_path)

        # update settings through the command line
        sim.argp = sim.ArgumentParser(description='Thermodynamic Non-Equilibrium Steady State circuit simulator v.' + sim.version)
        for k, v in sim.settings.items():
            sim.argp.add_argument('-' + k[0], '--' + k, required=False, type=sim.type_dict[sim.types[k]], help=sim.comments[k])

        # The options are not supported
        # argp.add_argument('--autostart', required=False, action='store_true', default=False, help='if set, simulation starts immediately (no CLI beforehand)')
        # argp.add_argument('--autoexit', required=False, action='store_true', default=False, help='if set, termination immediately after first simulation (no CLI afterwards)')
        # argp.add_argument('--no_cli', required=False, action='store_true', default=False, help='if set, no CLI is called at all (immediate start, immediate exit)')
        sim.settings.update({k: v for k, v in vars(sim.argp.parse_args(['--structure', struct_path, '--assignment', assign_path])).items() if v is not None})

        # setup communication interface
        sim.cli_io = sim.communication_wrapper(None, None, prefix=':>')

        sim.path_to_library = sim.settings["library"]
        sim.json_lib = sim.JsonFile(path=sim.path_to_library)

        sim.gate_lib = sim.GateLibCollectionBased(json_file=sim.json_lib)

        sim.structure = None
        if "structure" in sim.settings:
            structure = sim.load_structure(sim.settings)

        # Interface to new simulator
        sim.evaluator = sim.CircuitEvaluator(gate_lib=sim.gate_lib, settings=sim.settings, structure=structure)

        sim.cli_io.writeline("ready")

    simulator = __import__(os.path.basename(sim_scrips))
    sim_main(simulator)
    os.chdir(root)
    
    newFiles = []
    newFiles.append('.'.join(struct_path.split('.')[:-1])+'_score.json')
    with open(newFiles[-1], '+w')as file:
        json.dump(simulator.sim_run([]), file)
    newFiles.append('.'.join(struct_path.split('.')[:-1])+'_plasmid.json')
    with open(newFiles[-1], '+w')as file:
        json.dump(simulator.sim_plasmid([]), file)
    
    sys.path.remove(sim_path)
    return newFiles
 
