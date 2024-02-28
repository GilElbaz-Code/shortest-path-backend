import networkx as nx
import simplekml


class KMLGenerator:
    @staticmethod
    def generate_kml(graph: nx.Graph, kml_file_path: str):
        kml = simplekml.Kml()

        for node, data in graph.nodes(data=True):
            coordinates = data['coordinates']
            kml.newpoint(name=str(node), coords=[coordinates])

        kml.save(f'{kml_file_path}.kml')
