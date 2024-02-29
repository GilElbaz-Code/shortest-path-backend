import networkx as nx
import simplekml
from flask import send_file, make_response, jsonify, Response
import os
from tempfile import TemporaryDirectory


class KMLGenerator:
    def __init__(self, graph: nx.Graph):
        self.graph = graph

    def _generate_kml_content(self, shortest_path: list) -> bytes:
        kml = simplekml.Kml()

        for node, data in self.graph.nodes(data=True):
            coordinates = data['coordinates']
            kml.newpoint(name=str(node), coords=[coordinates])

        line = kml.newlinestring(name='Shortest Path',
                                 coords=[self.graph.nodes[node]['coordinates'] for node in shortest_path])
        line.style.linestyle.width = 3
        line.style.linestyle.color = simplekml.Color.blue

        kml_content = kml.kml()
        return kml_content.encode('utf-8')  # Convert string to bytes

    def generate_shortest_path_kml_response(self, shortest_path: list, kml_file_path: str) -> Response:
        try:
            kml_content = self._generate_kml_content(shortest_path)

            with TemporaryDirectory() as temp_dir:
                temp_kml_path = os.path.join(temp_dir, "shortest_path.kml")

                with open(temp_kml_path, 'wb') as kml_file:
                    kml_file.write(kml_content)

                kml_file.close()

                response = make_response(send_file(temp_kml_path,
                                                   as_attachment=True,
                                                   download_name=kml_file_path,
                                                   mimetype='application/vnd.google-earth.kml+xml'))
                return response

        except Exception as e:
            error_message = f'Error generating KML: {str(e)}'
            return make_response(jsonify({'error': error_message}), 500)
