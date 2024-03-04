import os
import tempfile
import networkx as nx
import simplekml


class KMLGenerator:
    """
        Class responsible for generating KML files for shortest path.
    """

    # Default values for line width and color obtained from environment variables
    LINE_WIDTH = int(os.getenv('LINE_WIDTH', default=3))
    LINE_COLOR = os.getenv('LINE_COLOR', default='ff008cff')

    def __init__(self, graph: nx.Graph):
        """
        Initialize the KMLGenerator with a graph.

        Parameters:
        - graph (nx.Graph): The graph for which the KML will be generated.
        """
        self.graph = graph

    def _generate_kml_content(self, path: list) -> simplekml.Kml:
        """
        Generate KML content for the given shortest path.

        Parameters:
        - shortest_path (list): List of nodes representing the shortest path.

        Returns:
        - simplekml.Kml: The generated KML object.
        """
        kml = simplekml.Kml()

        # Add points for each node in the graph
        for node, data in self.graph.nodes(data=True):
            coordinates = data['coordinates']
            kml.newpoint(name=str(node), coords=[coordinates])

        # Add a line for the shortest path
        line = kml.newlinestring(name='Shortest Path', coords=[self.graph.nodes[node]['coordinates'] for node in path])
        line.style.linestyle.width = self.LINE_WIDTH
        line.style.linestyle.color = self.LINE_COLOR

        return kml

    def generate_kml_file(self, shortest_path: list) -> str:
        """
        Generate a KML file for the given shortest path and return the file path.

        Parameters:
        - shortest_path (list): List of nodes representing the shortest path.

        Returns:
        - str: The file path of the generated KML file.
        """
        try:
            with tempfile.NamedTemporaryFile(suffix='.kml', mode='w', delete=False) as temp_kml:
                kml_content = self._generate_kml_content(path=shortest_path)
                temp_kml.write(kml_content.kml())
            return temp_kml.name
        except (IOError, OSError) as e:
            error_message = str(e)
            raise RuntimeError(f"Failed to create temporary KML file: {error_message}")
