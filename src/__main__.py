from GenerateDataFromRealData import *


def main():
    sessions = extract_session_from_data()
    app_map = read_map_from_path_file()
    groups, label_lookup = grouping_by_re()
    routes = find_real_route_from_path(label_lookup, sessions, app_map)

    paths_data = dict()
    for route_idx in range(len(routes)):

        for session_id, start_idx in routes[route_idx]:
            paths_data[route_idx] = sessions[session_id][start_idx:start_idx+len(app_map.paths[route_idx].edges_list)+1]
    for idx, path in enumerate(app_map.paths):
        mapping_data_to_variables(paths_data, idx)





if __name__ == "__main__" :
    main()