import networkx as nx
from scipy.spatial.distance import euclidean


class GraphProcessor:
    def __init__(self, graph: nx.Graph):
        self.graph = graph

    def find_closest_point(self, coord: tuple) -> tuple:
        closest_point = min(self.graph.nodes, key=lambda node: euclidean(coord, self.graph.nodes[node]['coordinates']))
        return closest_point

    def compute_shortest_path(self, start: tuple, end: tuple) -> list:
        shortest_path = nx.shortest_path(self.graph, source=start, target=end)
        return shortest_path
