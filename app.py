from flask import Flask, request, jsonify

from graph_builder import GraphBuilder
from kml_generator import KMLGenerator
from path_finder import PathFinder

app = Flask(__name__)

graph_builder = GraphBuilder(json_file_path="./data/graph_example.json")

path_finder = PathFinder(graph=graph_builder.graph)

kml_generator = KMLGenerator().generate_kml(graph=graph_builder.graph, kml_file_path='example')

@app.route('/calculate_shortest_path', methods=['POST'])
def calculate_shortest_path():
    # maybe need to convert input to float?
    try:
        coordinates_input = request.get_json()
        start = tuple(coordinates_input.get('start_point'))
        end = tuple(coordinates_input.get('end_point'))
        closest_point_start = path_finder.find_closest_point(coord=start)
        closest_point_end = path_finder.find_closest_point(coord=end)
        shortest_path = path_finder.compute_shortest_path(start=closest_point_start, end=closest_point_end)
        return jsonify({'path': shortest_path}), 200
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return jsonify({'error': error_message}), 500


if __name__ == '__main__':
    app.run()
