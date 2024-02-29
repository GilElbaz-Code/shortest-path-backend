import tempfile
import networkx as nx
import simplekml
import os


class KMLGenerator:
    LINE_WIDTH = int(os.getenv(key='LINE_WIDTH', default=3))
    LINE_COLOR = os.getenv(key='LINE_COLOR', default='ff008cff')

    def __init__(self, graph: nx.Graph):
        self.graph = graph

    def _generate_kml_content(self, shortest_path: list) -> str:
        kml = simplekml.Kml()

        for node, data in self.graph.nodes(data=True):
            coordinates = data['coordinates']
            kml.newpoint(name=str(node), coords=[coordinates])

        line = kml.newlinestring(name='Shortest Path',
                                 coords=[self.graph.nodes[node]['coordinates'] for node in shortest_path])
        line.style.linestyle.width = self.LINE_WIDTH
        line.style.linestyle.color = self.LINE_COLOR

        kml_content = kml.kml()
        return kml_content

    def generate_kml_file(self, shortest_path: list) -> str:
        try:
            with tempfile.NamedTemporaryFile(suffix='.kml', delete=False) as temp_kml:
                kml_content = self._generate_kml_content(shortest_path=shortest_path)
                temp_kml.write(kml_content.encode('utf-8'))
            return temp_kml.name
        except Exception as e:
            error_message = str(e)
            raise RuntimeError(f"Failed to create temporary KML file: {error_message}")
