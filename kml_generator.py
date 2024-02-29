import networkx as nx
import simplekml
from flask import send_file
from tempfile import NamedTemporaryFile


class KMLGenerator:
    def __init__(self, graph: nx.Graph):
        self.graph = graph

    def generate_shortest_path_kml(self, shortest_path: list, kml_file_path: str):
        kml = simplekml.Kml()

        for node, data in self.graph.nodes(data=True):
            coordinates = data['coordinates']
            kml.newpoint(name=str(node), coords=[coordinates])

        line = kml.newlinestring(name='Shortest Path',
                                 coords=[self.graph.nodes[node]['coordinates'] for node in shortest_path])
        line.style.linestyle.width = 3
        line.style.linestyle.color = simplekml.Color.blue

        with NamedTemporaryFile(suffix='.kml', delete=False) as temp_kml:
            kml.save(temp_kml.name)

        return send_file(temp_kml.name, as_attachment=True, download_name=kml_file_path)
