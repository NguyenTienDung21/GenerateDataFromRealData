from processing.data_reader import extract_session_from_data
from processing.data_reader import read_map_from_path_file, get_unique_url
from processing.data_reader import get_data_entry_point, get_var_lookup
import re
from collections import defaultdict
from processing.url_processing import extract_uri
import csv
import json


def get_labels_from_nodes(nodes):
    return [node.label for node in nodes]


def match_url(label_re, url):
    return label_re.fullmatch(str(extract_uri(url[0])))


def group_url_by_label(label, url_list, label_lookup, raw):
    label_re = re.compile(label)
    group = list(filter(lambda url: match_url(label_re, url) is not None, url_list))
    for url in group:
        label_lookup[extract_uri(url[0])] = raw
    return group


def label_process(label):
    label_escape = re.escape(label)
    label_pattern = label_escape.replace("\\[NUMBER\\]","\d*")

    return label_pattern


def grouping_by_re():
    app_map = read_map_from_path_file()
    labels = get_labels_from_nodes(app_map.nodes)
    url_list = get_unique_url()
    re_labels = [ label_process(label) for label in labels]
    label_lookup = defaultdict(str)
    groups = dict()
    for label, raw in zip(re_labels,labels):
        url_group = group_url_by_label(label, url_list, label_lookup, raw)
        groups[label] = url_group
    return groups, label_lookup


def compare_action_data(data1, data2):
    if data2 is None and data1 == "NaN":
        return False
    if data1 == "NaN":
        return True
    if data2 is None :
        return True
    data_dict_1 = json.loads(data1)
    data_dict_2 = json.loads(data2)
    data_dict_1_keys = set(data_dict_1.keys())
    data_dict_2_keys = set(data_dict_2.keys())
    print(data_dict_1_keys)
    print(data_dict_2_keys)
    print(data_dict_1_keys != data_dict_2_keys)
    return data_dict_1_keys != data_dict_2_keys

def match_path(session, start_idx, labels, label_lookup):
    num_of_node = len(labels)
    for idx in range(num_of_node):
        label = label_lookup[session[start_idx+idx].url]
        session_action = session[start_idx+idx].action
        session_action_data = session[start_idx+idx].action_data
        label_from_edge = labels[idx][0]
        label_action, label_action_data = labels[idx][1]
        compare_action = session_action != label_action if label_action != "end" else False
        # compare_data_result = compare_action_data(label_action_data,session_action_data)
        print(compare_action)
        print(label)
        print(label_from_edge)

        if label != label_from_edge or  compare_action :
            return False
    return True


def find_real_path(sessions, labels, label_lookup):
    real_paths = []
    num_of_node = len(labels)
    for id, session in sessions.items():
        sess_length = len(session)
        if sess_length >= num_of_node:
            for start_idx, node in zip(range(sess_length), session):
                if sess_length - start_idx >= num_of_node and match_path(session, start_idx, labels, label_lookup):
                        real_paths.append((id, start_idx))
    return real_paths


def find_real_route_from_path(label_lookup, sessions, app_map):
    routes = []
    for idx, path in enumerate(app_map.paths):
        label_list = app_map.convert_path_to_label_sequence_with_action(path)
        route = find_real_path(sessions, label_list, label_lookup)
        routes.append(route)
    return routes


def write_to_csv(routes ,filename):
    print(routes)
    if len(routes) == 0 :
        return
    with open(filename, 'w') as f:
            data_writer = csv.writer(f)
            column_names = routes[0].keys()
            data_writer.writerow(column_names)
            for data in routes:
                data_writer.writerow(data.values())


def mapping_data_to_variables(paths_data, path_idx):
    dataset = []
    print(path_idx)
    file_name = f'data/output/production_{path_idx}_.csv'
    for _, path_data in paths_data.items():
            dataEntryPoint = get_data_entry_point(path_idx)
            var_lookup = get_var_lookup()
            var_data = dataEntryPoint.map_data_for_path(path_data, var_lookup[str(path_idx)])
            dataset.append(var_data)

    write_to_csv(dataset, file_name)

