import json
import networkx as nx

class GraphBuilder:
    """
    A class for building a network graph from a JSON file.
    """

    def __init__(self, json_file_path: str):
        """
        Initialize the GraphBuilder.

        Parameters:
        - json_file_path (str): The path to the JSON file containing graph data.
        """
        self.graph = self._build_graph(json_file_path=json_file_path)

    @staticmethod
    def _parse_source_node(source_str: str) -> tuple:
        """
        Parse the source node coordinates from a string.

        Parameters:
        - source_str (str): The string representation of the source node coordinates.

        Returns:
        - tuple: A tuple containing the parsed coordinates as floats.
        """
        return tuple(map(float, source_str.strip('()').split(',')))

    def _build_graph(self, json_file_path: str) -> nx.Graph:
        """
        Build a network graph from the data in a JSON file.

        Parameters:
        - json_file_path (str): The path to the JSON file containing graph data.

        Returns:
        - nx.Graph: A networkx Graph object representing the constructed graph.
        """
        # Load graph data from the JSON file
        with open(json_file_path) as f:
            graph_data = json.load(f)

        # Create an empty undirected graph
        graph = nx.Graph()

        # Iterate through the graph data and add nodes and edges to the graph
        for source, targets in graph_data.items():
            # Parse source node coordinates and add it to the graph
            source_node = self._parse_source_node(source_str=source)
            graph.add_node(node_for_adding=source_node, coordinates=source_node)

            # Add target nodes and edges to the graph
            for target in targets:
                target_node = tuple(target)

                # Add target node to the graph
                graph.add_node(node_for_adding=target_node, coordinates=target_node)

                # Add an edge between source and target nodes
                graph.add_edge(u_of_edge=source_node, v_of_edge=target_node)

        return graph
