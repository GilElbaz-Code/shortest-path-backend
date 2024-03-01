import networkx as nx
from scipy.spatial.distance import euclidean


class GraphProcessor:
    """
    Class responsible for processing a geographical network represented by a graph.
    """

    def __init__(self, graph: nx.Graph):
        """
        Initialize the GraphProcessor with the given graph.

        Parameters:
        - graph (nx.Graph): Graph object representing the geographical network.
        """
        self.graph = graph

    def find_closest_point(self, coord: tuple) -> tuple:
        """
        Find the closest point in the graph to the given coordinates.

        Parameters:
        - coord (tuple): Coordinates (latitude, longitude) to find the closest point to.

        Returns:
        - tuple: Coordinates of the closest point in the graph.
        """
        closest_point = min(self.graph.nodes, key=lambda node: euclidean(coord, self.graph.nodes[node]['coordinates']))
        return closest_point

    def compute_shortest_path(self, start: tuple, end: tuple) -> list:
        """
        Compute the shortest path between two points in the graph.

        Parameters:
        - start (tuple): Coordinates of the starting point.
        - end (tuple): Coordinates of the ending point.

        Returns:
        - list: List of nodes representing the shortest path.
        """
        shortest_path = nx.shortest_path(self.graph, source=start, target=end)
        return shortest_path
