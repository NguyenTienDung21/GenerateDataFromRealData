import csv
import json
from classes.transition import Transition
from classes.json_keys import *
from classes.variable import Variable, VariableData
from functools import reduce
from processing.filepaths import *


def join_list(list_):
    return reduce(lambda x, y: x+ str(y), list_, '')

def get_variables(variable_dict_list):
    variable_list = [Variable(variable_dict[VAR_NAME], variable_dict[VAR_TYPE]) for variable_dict in variable_dict_list]
    return variable_list


def get_transition_from_dict(transition_dict):
    id = transition_dict[TRAN_ID]
    variable_dict_list = transition_dict[TRAN_VAR]
    return Transition(id, get_variables(variable_dict_list))


class PathDataEntryPoint:

            def from_dict(self, path_dict ):
                self.id = path_dict[PATH_DATA_ID]
                path_data = path_dict[PATH_DATA]
                self.get_transitions_data_from_dict(path_data)

            def get_transitions_data_from_dict(self, transition_dict_list):
                self.data = [get_transition_from_dict(transition_dict) for transition_dict in transition_dict_list]


            def map_data_for_path(self, path_data, var_lookup):
                vars =dict()
                for traffic_data, transition in zip(path_data, self.data):
                    print(traffic_data)
                    if transition.variables is not None and len(transition.variables) > 0:
                        for variable in transition.variables:

                            action_data = json.loads(traffic_data.action_data)

                            if action_data != None:

                                xpath_key = var_lookup[variable.name]
                                if xpath_key in action_data:
                                    value = action_data[xpath_key]['value']
                                    vars[variable.name] = value
                                else:
                                    print(f'Key not found : {xpath_key}')
                return vars



            def write_to_csv(self, filename):
                with open(filename, 'w') as f:
                    data_writer = csv.writer(f)
                    column_names = self.data_gen[0].keys()
                    data_writer.writerow(column_names)
                    for data in self.data_gen:
                        data_writer.writerow(data.values())
