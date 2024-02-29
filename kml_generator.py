import networkx as nx
import simplekml


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

        kml.save(path=kml_file_path)
