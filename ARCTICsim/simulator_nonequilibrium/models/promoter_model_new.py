"""
Author: Erik Kubaczka
E-Mail: erik.kubaczka@tu-darmstadt.de
"""

import numpy as np

from models.steady_state_ctmc_new import SteadyStateCTMC


class PromoterModel(SteadyStateCTMC):

    def __init__(self,
                 num_states,
                 num_trainable_parameters,
                 input_scaling_factor,
                 infinitesimal_generator_function,
                 per_state_promoter_activity):
        super().__init__(num_states, infinitesimal_generator_function, n_params=num_trainable_parameters - 2)

        self.num_trainable_parameters = num_trainable_parameters
        self.input_scaling_factor = input_scaling_factor

        self.promoter_state_class = np.array(per_state_promoter_activity)
        self.promoter_activity = np.array(per_state_promoter_activity)

        self.c_val = 10 ** (-6) #  A choice of 10**(-4) would be numerically more stable

    def __call__(self, in_val_dict: dict, sim_settings: dict, *args, **kwargs) -> dict:
        """
        :param in_val:
        :param args:
        :param kwargs:
        :return:
        """

        propagation_val_dict = {} # {key: in_val_dict[key] * self.input_scaling_factor for key in in_val_dict}

        for key in in_val_dict:
            new_vals = in_val_dict[key] * self.input_scaling_factor
            new_vals[new_vals < self.c_val] = self.c_val
            propagation_val_dict[key] = new_vals

        statistics = super().__call__(in_val_dict=propagation_val_dict, sim_settings=sim_settings)
        results = dict(statistics)

        average_promoter_activity_per_state = self.promoter_activity * statistics["distribution"]
        results["average_promoter_activity_per_state"] = average_promoter_activity_per_state
        results["average_promoter_activity"] = np.sum(average_promoter_activity_per_state, axis=-1)
        results["energy_dissipation_rate"] = statistics["entropy_production_rate"]
        results["energy_p"] = statistics["entropy_production_rate"]
        results["promoter_activity_per_state"] = self.promoter_activity

        return results

    def insert_params(self, new_params):
        if len(new_params) != self.num_trainable_parameters:
            raise Exception(
                f"The number of provided parameters does not match the number of available parameters ({len(new_params)} provided vs. {(self.num_trainable_parameters)} available)")

        y_on, y_off = new_params[:2]
        self.insert_rates(new_rates=new_params[2:])

        # Update Promoter Activity
        # (During parameter estimation, self.promoter_state_class is expected do consist of zeros and ones only)
        self.promoter_activity = y_off + (y_on - y_off) * self.promoter_state_class
