import os
import tempfile
import networkx as nx
import simplekml


class KMLGenerator:
    """
    A class for generating Keyhole Markup Language (KML) files representing graph data.
    """

    LINE_WIDTH = int(os.getenv('LINE_WIDTH', default=3))
    LINE_COLOR = os.getenv('LINE_COLOR', default='ff008cff')

    def __init__(self, graph: nx.Graph):
        """
        Initialize the KMLGenerator with a network graph.

        Parameters:
        - graph (nx.Graph): The network graph used for generating KML files.
        """
        self.graph = graph

    def _generate_kml_content(self, path: list) -> simplekml.Kml:
        """
        Generate KML content for the given path on the graph.

        Parameters:
        - path (list): A list representing the nodes in the shortest path.

        Returns:
        - simplekml.Kml: A simplekml Kml object containing the generated KML content.
        """
        kml = simplekml.Kml()

        # Add points for each node in the graph
        for node, data in self.graph.nodes(data=True):
            coordinates = data['coordinates']
            kml.newpoint(name=str(node), coords=[coordinates])

        # Add a line representing the shortest path
        line = kml.newlinestring(name='Shortest Path', coords=[self.graph.nodes[node]['coordinates'] for node in path])
        line.style.linestyle.width = self.LINE_WIDTH
        line.style.linestyle.color = self.LINE_COLOR

        return kml

    def generate_kml_file(self, shortest_path: list) -> str:
        """
        Generate a temporary KML file for the given shortest path.

        Parameters:
        - shortest_path (list): A list representing the nodes in the shortest path.

        Returns:
        - str: The path to the generated temporary KML file.
        """
        try:
            # Create a named temporary KML file
            with tempfile.NamedTemporaryFile(suffix='.kml', mode='w', delete=False) as temp_kml:
                kml_content = self._generate_kml_content(path=shortest_path)
                temp_kml.write(kml_content.kml())
            return temp_kml.name
        except (IOError, OSError) as e:
            # Handle errors and raise a RuntimeError with an appropriate error message
            error_message = str(e)
            raise RuntimeError(f"Failed to create temporary KML file: {error_message}")
