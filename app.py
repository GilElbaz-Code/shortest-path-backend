from flask import Flask, request, jsonify, send_file

from graph_builder import GraphBuilder
from kml_generator import KMLGenerator
from graph_processor import GraphProcessor

app = Flask(__name__)

graph_builder = GraphBuilder(json_file_path="./data/graph_example.json")
graph_processor = GraphProcessor(graph=graph_builder.graph)
kml_generator = KMLGenerator(graph=graph_builder.graph)


@app.route('/calculate_shortest_path', methods=['POST'])
def calculate_shortest_path():
    try:
        request_input = request.get_json()

        start = tuple(request_input.get('start_point'))
        end = tuple(request_input.get('end_point'))
        include_kml = request_input.get('include_kml')

        if not (start and end):
            return jsonify({'error': 'Invalid input format. Expected "start_point" and "end_point" coordinates.'}), 400

        closest_point_start = graph_processor.find_closest_point(coord=start)
        closest_point_end = graph_processor.find_closest_point(coord=end)

        shortest_path = graph_processor.compute_shortest_path(start=closest_point_start, end=closest_point_end)

        if include_kml:
            kml_shortest_path = kml_generator.generate_shortest_path_kml(shortest_path=shortest_path,
                                                                         kml_file_path="shortest_path.kml")
            return kml_shortest_path, 200
        return jsonify({'path': shortest_path}), 200
    except (ValueError, TypeError) as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 500


if __name__ == '__main__':
    app.run()
