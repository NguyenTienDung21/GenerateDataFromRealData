from classes.json_keys import *
from classes.edge import Edge
from classes.node import Node
from classes.path import Path
from processing.url_processing import extract_uri


class ApplicationMapData:
    def __init__(self, json_data):
        self.nodes = []
        self.edges = []
        self.paths = []
        self.edges_hash_map = dict()
        self.nodes_hash_map = dict()
        self.set_node_from_data(json_data)
        self.set_edge_from_data(json_data)
        self.set_path_from_data(json_data)

    def set_node_from_data(self, json_data):
        nodes = json_data[NODES]
        nodes_id = range(len(nodes))
        for node_data, idx in zip(nodes, nodes_id):
            node_id = node_data[NODE_ID]
            label = extract_uri(node_data[NODE_LABEL])
            node = Node(node_id, label)
            self.append_node(node)
            self.update_node_hash_map(idx, node_id)

    def set_edge_from_data(self, json_data):
        edges = json_data[EDGES]
        edges_idx = range(len(edges))
        for edge_data, idx in zip(edges, edges_idx) :
            edge_id = edge_data[EDGE_ID]
            edge_src = edge_data[EDGE_SRC]
            edge_dest = edge_data[EDGE_DEST]
            edge_attribute = edge_data[EDGE_ATTRIBUTE]
            edge = Edge(edge_id, edge_src, edge_dest, edge_attribute)
            self.append_edge(edge)
            self.update_edge_hash_map(idx, edge_id)

    def set_path_from_data(self, json_data):
        for path in json_data[PATHS]:
            path_id = path[PATH_ID]
            path_edge_id_list = path[PATH_EDGES]
            path_edges_list = self.map_id_to_edge(path_edge_id_list)
            path = Path(path_id, path_edge_id_list, path_edges_list)
            self.append_path(path)

    def append_edge(self, edge):
        self.edges.append(edge)

    def update_edge_hash_map(self,idx, edge_id):
        self.edges_hash_map[edge_id] = idx

    def append_node(self, node):
        self.nodes.append(node)

    def update_node_hash_map(self, idx, node_id):
        self.nodes_hash_map[node_id] = idx

    def map_id_to_edge(self, edge_id_list):
        return list(map(lambda edge_id: self.edges[self.edges_hash_map[edge_id]], edge_id_list))

    def append_path(self, path):
        self.paths.append(path)

    def convert_path_to_label_sequence(self,path):
        dest_list = [edge.dest for edge in path.edges_list]
        first_edge, *tail = path.edges_list
        src = first_edge.src
        node_list = [src] + dest_list
        return [self.nodes[self.nodes_hash_map[node]].label for node in node_list]

    def convert_path_to_label_sequence_with_action(self,path):
        dest_list = [edge.dest for edge in path.edges_list]
        action_list = [(edge.attribute[0],edge.attribute[1]) for edge in path.edges_list] + [("end", None)]
        first_edge, *tail = path.edges_list
        src = first_edge.src
        node_list = [src] + dest_list
        return list(zip([self.nodes[self.nodes_hash_map[node]].label for node in node_list],
                   action_list))