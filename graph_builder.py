import json
import networkx as nx


class GraphBuilder:
    """
    Class responsible for building a graph from a JSON file using NetworkX.
    """

    def __init__(self, json_file_path: str):
        """
        Initialize the GraphBuilder with the given JSON file path and build the graph.

        Parameters:
        - json_file_path (str): Path to the JSON file containing graph data.
        """
        self.graph = self.build_graph(json_file_path=json_file_path)

    @staticmethod
    def _parse_source_node(source_str: str):
        """
        Parse the source node from a string representation.

        Parameters:
        - source_str (str): String representation of the source node.

        Returns:
        - tuple: Parsed tuple representing the source node coordinates.
        """
        return tuple(map(float, source_str.strip('()').split(',')))

    def build_graph(self, json_file_path: str) -> nx.Graph:
        """
        Build a graph from the provided JSON file.

        Parameters:
        - json_file_path (str): Path to the JSON file containing graph data.

        Returns:
        - nx.Graph: Constructed graph using NetworkX.
        """
        with open(json_file_path) as f:
            graph_data = json.load(f)

        graph = nx.Graph()

        for source, targets in graph_data.items():
            # Parse source node coordinates
            source_node = self._parse_source_node(source_str=source)

            # Add source node to the graph with coordinates attribute
            graph.add_node(node_for_adding=source_node, coordinates=source_node)

            for target in targets:
                # Parse target node coordinates
                target_node = tuple(target)

                # Add target node to the graph with coordinates attribute
                graph.add_node(node_for_adding=target_node, coordinates=target_node)

                # Add edge between source and target nodes
                graph.add_edge(u_of_edge=source_node, v_of_edge=target_node)

        return graph
