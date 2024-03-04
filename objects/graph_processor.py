import networkx as nx
from scipy.spatial.distance import euclidean

class GraphProcessor:
    """
    A class for processing operations on a network graph, such as finding the closest points and computing the shortest paths.
    """

    def __init__(self, graph: nx.Graph):
        self.graph = graph

    def find_closest_point(self, coord: tuple) -> tuple:
        """
        Find the closest point on the graph to the given coordinates.

        Parameters:
        - coord (tuple): A tuple representing the coordinates for which the closest point needs to be found.

        Returns:
        - tuple: The coordinates of the closest point on the graph.
        """
        closest_point = min(self.graph.nodes, key=lambda node: euclidean(coord, self.graph.nodes[node]['coordinates']))
        return closest_point

    def compute_shortest_path(self, start: tuple, end: tuple) -> list:
        """
        Compute the shortest path on the graph between two given nodes.

        Parameters:
        - start (tuple): The starting node coordinates.
        - end (tuple): The ending node coordinates.

        Returns:
        - list: A list representing the nodes in the shortest path.
        """
        shortest_path = nx.shortest_path(self.graph, source=start, target=end)
        return shortest_path
