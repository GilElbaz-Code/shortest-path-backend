from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from constants import Constants
from graph_builder import GraphBuilder
from kml_generator import KMLGenerator
from graph_processor import GraphProcessor
from collections import namedtuple

app = Flask(__name__)
CORS(app, expose_headers=["Content-Disposition"])

# Initialize graph components
graph_builder = GraphBuilder(json_file_path="./data/graph_example.json")
graph_processor = GraphProcessor(graph=graph_builder.graph)
kml_generator = KMLGenerator(graph=graph_builder.graph)

Coordinates = namedtuple('Coordinates', ['latitude', 'longitude'])


@app.route('/calculate_shortest_path', methods=['POST'])
def calculate_shortest_path():
    """
    Calculate the shortest path between two points and optionally generate a KML file.

    Expected JSON format:
    {
        "start": {"x": latitude, "y": longitude},
        "end": {"x": latitude, "y": longitude},
        "kml": true/false
    }

    Returns:
    - JSON response with the shortest path or KML file download link.
    """
    try:
        request_input = request.get_json()

        start = request_input.get('start')
        end = request_input.get('end')
        kml_requested = request_input.get('kml', False)

        if not (start and end):
            return jsonify({'error': 'Invalid input format. Expected start and end coordinates.'}), 400

        start = Coordinates(latitude=float(start.get('x')), longitude=float(start.get('y')))
        end = Coordinates(latitude=float(end.get('x')), longitude=float(end.get('y')))

        # Find the closest points and compute the shortest path
        closest_point_start = graph_processor.find_closest_point(coord=start)
        closest_point_end = graph_processor.find_closest_point(coord=end)
        shortest_path = graph_processor.compute_shortest_path(start=closest_point_start, end=closest_point_end)

        if kml_requested:
            # Generate KML file and return download link
            kml_shortest_path = kml_generator.generate_kml_file(shortest_path=shortest_path)
            return send_file(kml_shortest_path,
                             mimetype=Constants.KML_MIMETYPE,
                             as_attachment=True,
                             download_name='shortest_path.kml')

        return jsonify({'path': shortest_path}), 200
    except (ValueError, TypeError) as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 500


if __name__ == '__main__':
    app.run()
