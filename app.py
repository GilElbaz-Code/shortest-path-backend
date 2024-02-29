from flask import Flask, request, jsonify

from graph_builder import GraphBuilder
from kml_generator import KMLGenerator
from graph_processor import GraphProcessor

app = Flask(__name__)

# Initialize graph components
graph_builder = GraphBuilder(json_file_path="./data/graph_example.json")
graph_processor = GraphProcessor(graph=graph_builder.graph)
kml_generator = KMLGenerator(graph=graph_builder.graph)


@app.route('/calculate_shortest_path', methods=['POST'])
def calculate_shortest_path():
    """
    Calculate the shortest path between two points and optionally generate a KML file.

    Expected JSON format:
    {
        "start_point": [latitude, longitude],
        "end_point": [latitude, longitude],
        "include_kml": true/false
    }

    Returns:
    - JSON response with the shortest path or KML file download link.
    """
    try:
        request_input = request.get_json()

        start = request_input.get('start_point')
        end = request_input.get('end_point')
        include_kml = request_input.get('include_kml')

        if not (start and end):
            return jsonify({'error': 'Invalid input format. Expected "start_point" and "end_point" coordinates.'}), 400

        # Find the closest points and compute the shortest path
        closest_point_start = graph_processor.find_closest_point(coord=tuple(start))
        closest_point_end = graph_processor.find_closest_point(coord=tuple(end))
        shortest_path = graph_processor.compute_shortest_path(start=closest_point_start, end=closest_point_end)

        if include_kml:
            # Generate KML file and return download link
            kml_shortest_path = kml_generator.generate_shortest_path_kml(shortest_path=shortest_path,
                                                                         kml_file_path="shortest_path.kml")
            return kml_shortest_path, 200

        return jsonify({'path': shortest_path}), 200
    except (ValueError, TypeError) as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 500


if __name__ == '__main__':
    app.run()
