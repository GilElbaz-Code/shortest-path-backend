import os
from collections import namedtuple

from graph_builder import GraphBuilder
from graph_processor import GraphProcessor
from kml_generator import KMLGenerator

class GraphManager:
    """
    A class that manages the graph-related operations, including building, processing, and generating KML files.
    """

    # Default path to the JSON file containing graph data
    GRAPH_DATA = os.getenv(key='GRAPH_DATA', default='./data/graph_example.json')

    def __init__(self):
        """
        Initialize the GraphManager with instances of GraphBuilder, GraphProcessor, and KMLGenerator.
        """
        # Create a GraphBuilder instance to build the graph from the JSON file
        self.graph_builder = GraphBuilder(json_file_path=self.GRAPH_DATA)

        # Create a GraphProcessor instance for processing graph-related operations
        self.graph_processor = GraphProcessor(graph=self.graph_builder.graph)

        # Create a KMLGenerator instance for generating KML files from the graph
        self.kml_generator = KMLGenerator(graph=self.graph_builder.graph)

    def calculate_shortest_path(self, start: dict, end: dict, kml_requested: bool):
        """
        Calculate the shortest path between two points on the graph.

        Parameters:
        - start (dict): Dictionary containing 'x' and 'y' keys representing the starting coordinates.
        - end (dict): Dictionary containing 'x' and 'y' keys representing the ending coordinates.
        - kml_requested (bool): Flag indicating whether a KML file is requested.

        Returns:
        - str or list: If kml_requested is True, returns the path to the generated KML file.
                      Otherwise, returns a list representing the shortest path.
        """
        # Define a named tuple for coordinates
        Coordinates = namedtuple('Coordinates', ['latitude', 'longitude'])

        # Parse start and end coordinates
        start = Coordinates(latitude=float(start.get('x')), longitude=float(start.get('y')))
        end = Coordinates(latitude=float(end.get('x')), longitude=float(end.get('y')))

        # Find the closest points on the graph to the given coordinates
        closest_point_start = self.graph_processor.find_closest_point(coord=start)
        closest_point_end = self.graph_processor.find_closest_point(coord=end)

        # Calculate the shortest path between the closest points
        shortest_path = self.graph_processor.compute_shortest_path(start=closest_point_start, end=closest_point_end)

        # If a KML file is requested, generate and return the KML file path
        if kml_requested:
            kml_shortest_path = self.kml_generator.generate_kml_file(shortest_path=shortest_path)
            return kml_shortest_path

        # Otherwise, return the list representing the shortest path
        return shortest_path
