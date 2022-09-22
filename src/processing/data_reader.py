import csv
import json
from classes.traffic_data_row import TrafficData
from classes.session import Session
from collections import defaultdict
from psql.connector import PSQLconnector
from classes.map import ApplicationMapData
from classes.DataEntrypoint import PathDataEntryPoint

from psql.commands import *
from processing.filepaths import *
from classes.json_keys import *



def extract_session_from_data():
    sessions = defaultdict(list)
    connector = PSQLconnector()
    def add_sessions(row):
        row_data = TrafficData(row)
        sessions[row_data.session].append(row_data)
    connector.connect()
    connector.execute(GET_ALL_COMMANDS, add_sessions)
    connector.disconnect()
    return sessions


def read_map_from_path_file(filepath=PATH_FILE):
    with open(filepath) as f:
        path = json.load(f)
        app_map = ApplicationMapData(path)
        return app_map


def get_unique_url():
    url = []
    def add_url(row):
        url.append(row)
    connector = PSQLconnector()
    connector.connect()
    connector.execute(GET_URL_COMMAND, add_url)
    connector.disconnect()
    return url


def get_data_entry_point(path_idx):
    with open(DATA_ENTRY_POINT_PATH, 'r') as f:
        data_entrypoint_dict = json.load(f)
        data_entrypoint = PathDataEntryPoint()
        data_entrypoint.from_dict(data_entrypoint_dict[path_idx])
        return data_entrypoint


def get_var_lookup():
    with open(VAR_LOOKUP_PATH) as f:
        return json.load(f)