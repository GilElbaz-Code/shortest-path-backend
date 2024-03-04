import os
from collections import namedtuple

from objects.graph_builder import GraphBuilder
from objects.graph_processor import GraphProcessor
from objects.kml_generator import KMLGenerator
from objects.results.result_classes import FilePathResult, JsonPathResult


class GraphManager:
    """
    A class that manages the graph-related operations, including building, processing, and generating KML files.
    """

    GRAPH_DATA = os.getenv(key='GRAPH_DATA', default='./data/graph_example.json')

    def __init__(self):
        self.graph_builder = GraphBuilder(json_file_path=self.GRAPH_DATA)
        self.graph_processor = GraphProcessor(graph=self.graph_builder.graph)
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
        Coordinates = namedtuple('Coordinates', ['latitude', 'longitude'])

        start = Coordinates(latitude=float(start.get('x')), longitude=float(start.get('y')))
        end = Coordinates(latitude=float(end.get('x')), longitude=float(end.get('y')))

        closest_point_start = self.graph_processor.find_closest_point(coord=start)
        closest_point_end = self.graph_processor.find_closest_point(coord=end)

        shortest_path = self.graph_processor.compute_shortest_path(start=closest_point_start, end=closest_point_end)

        if kml_requested:
            return FilePathResult(file_path=self.kml_generator.generate_kml_file(shortest_path=shortest_path))
        else:
            return JsonPathResult(path=shortest_path)
