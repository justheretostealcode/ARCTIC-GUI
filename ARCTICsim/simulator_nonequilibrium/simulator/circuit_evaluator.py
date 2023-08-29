"""
Author: Erik Kubaczka
"""
import numpy as np
from simulator.circuit import Circuit
from simulator.scores import FunctionalScore, EnergyScore
from simulator.circuit_utils import CircuitAssignment, CircuitStructure


# ToDos
# 1. Implement Interface    ✓
#   - Load Stucture             ✓
#   - Load Gate Lib             ✓
#   - Interpret Assignment      ✓
#
# 2. Implement Function         ✓
#   - Construct assigned circuit                                        ✓
#   - Implement simulation (based on samples from distributions)        ✓
#   - Propagate values through circuit                                  ✓
#
# 3. Perform scoring
#   - Functional Scoring based on Wasserstein
#   - Energy Scoring (either Average or Maximum)
#
# 4. Return scores
#   - Pass scores in JSON Format to optimizer

class CircuitEvaluator:

    def __init__(self, gate_lib, settings, structure: CircuitStructure):
        self.gate_lib = gate_lib
        self.settings = settings
        self.set_structure(structure)

        self.update_settings(settings)
        pass

    def set_structure(self, structure: CircuitStructure):
        if structure is None:
            return

        self.structure = structure
        self.circuit = Circuit(structure)

        # Generate Truthtable

    def update_settings(self, settings: dict):
        self.settings = settings

        self.functional_score = FunctionalScore(settings)
        self.energy_score = EnergyScore(settings)

        self.DEBUG_LEVEL = settings["verbosity"]

    def score_assignment(self, assignment: CircuitAssignment, sim_settings: dict):
        if self.DEBUG_LEVEL >= 1:
            print("sim_settings are currently ignored")

        circuit = self.circuit

        circuit.set_assignment(assignment)

        # ToDo
        # Iterate over truthtable entries
        # Evaluate Circuit
        # Extract relevant Values from circuit vals
        # Extract Energy Level
        mode = sim_settings["mode"]
        n_samples = sim_settings["n_samples"] if mode == "samp" else 1

        structure = circuit.structure
        truthtable = structure.truthtable

        circuit_output_vals_dict = {out_id: [[] for _ in range(2)] for out_id in structure.outputs}
        circuit_output_vals = []
        circuit_energy_rates = []

        input_ids = list(structure.inputs)
        input_ids.sort()
        node_order = structure.combinational_order()

        for input_vals, output_val in truthtable.input_output_truthtable():
            input_vals_dict = dict(zip(input_ids, input_vals))
            gate_output_vals = {id: np.empty(shape=(n_samples)) for id in node_order}
            energy_rates = np.empty(shape=(n_samples))
            for iN in range(n_samples):

                cur_gate_output_vals = circuit(input_vals_dict=input_vals_dict, sim_settings=sim_settings)
                cur_energy_rate = circuit.energy_rate

                for id in cur_gate_output_vals:
                    gate_output_vals[id][iN] = cur_gate_output_vals[id]
                energy_rates[iN] = cur_energy_rate

            cur_out_vals = []
            for out_id in structure.outputs:
                circuit_output_vals_dict[out_id][output_val].append(gate_output_vals[out_id])
                cur_out_vals.append(gate_output_vals[out_id])

            circuit_output_vals.append(cur_out_vals)
            circuit_energy_rates.append(energy_rates)

            # print(gate_output_vals)
            pass

        circuit_output_vals = np.array(circuit_output_vals)
        circuit_energy_rates = np.array(circuit_energy_rates)

        functional_scores = {}
        for out_id in circuit_output_vals_dict:
            cur_entry = circuit_output_vals_dict[out_id]
            functional_score = np.infty
            for dataON in cur_entry[1]:
                for dataOFF in cur_entry[0]:
                    cur_score = self.functional_score(dataON=dataON, dataOFF=dataOFF)
                    if cur_score < functional_score:
                        functional_score = cur_score

            functional_scores[out_id] = functional_score

        energy_score = self.energy_score(circuit_energy_rates)

        scores = {"functional_score": functional_scores,
                  "energy_score": energy_score}
        # ToDo
        # Apply functional score
        # Apply energy score

        return scores
