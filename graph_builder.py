import json
import networkx as nx
import matplotlib.pyplot as plt


class GraphBuilder:
    def __init__(self, json_file_path: str):
        self.graph = self.build_graph(json_file_path=json_file_path)

    @staticmethod
    def _parse_source_node(source_str: str):
        return tuple(map(float, source_str.strip('()').split(',')))

    def build_graph(self, json_file_path):
        with open(json_file_path) as f:
            graph_data = json.load(f)

        graph = nx.Graph()

        for source, targets in graph_data.items():
            source_node = self._parse_source_node(source_str=source)
            graph.add_node(node_for_adding=source_node, coordinates=source_node)
            for target in targets:
                target_node = tuple(target)
                graph.add_node(node_for_adding=target_node, coordinates=target_node)
                graph.add_edge(u_of_edge=source_node, v_of_edge=target_node)
        # plt.figure()
        # nx.draw(graph)
        # plt.show()
        return graph
