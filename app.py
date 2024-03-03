# Import necessary modules from Flask and custom components
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from constants import Constants
from graph_builder import GraphBuilder
from kml_generator import KMLGenerator
from graph_processor import GraphProcessor
from collections import namedtuple

# Create a Flask web application instance
app = Flask(__name__)

# Enable CORS and expose "Content-Disposition" headers for handling cross-origin requests
CORS(app, expose_headers=["Content-Disposition"])

# Initialize graph components using custom modules
graph_builder = GraphBuilder(json_file_path="./data/graph_example.json")
graph_processor = GraphProcessor(graph=graph_builder.graph)
kml_generator = KMLGenerator(graph=graph_builder.graph)

# Define a namedtuple for coordinates with 'latitude' and 'longitude' fields
Coordinates = namedtuple('Coordinates', ['latitude', 'longitude'])


# Define a Flask route for handling POST requests to calculate the shortest path
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
        # Retrieve JSON input from the POST request
        request_input = request.get_json()

        # Extract start, end, and kml_requested from the input
        start = request_input.get('start')
        end = request_input.get('end')
        kml_requested = request_input.get('kml', False)

        # Convert start and end coordinates to namedtuples
        start = Coordinates(latitude=float(start.get('x')), longitude=float(start.get('y')))
        end = Coordinates(latitude=float(end.get('x')), longitude=float(end.get('y')))

        # Find the closest points and compute the shortest path
        closest_point_start = graph_processor.find_closest_point(coord=start)
        closest_point_end = graph_processor.find_closest_point(coord=end)
        shortest_path = graph_processor.compute_shortest_path(start=closest_point_start, end=closest_point_end)

        # If KML is requested, generate the KML file and return as a downloadable attachment
        if kml_requested:
            kml_shortest_path = kml_generator.generate_kml_file(shortest_path=shortest_path)
            return send_file(kml_shortest_path,
                             mimetype=Constants.KML_MIMETYPE,
                             as_attachment=True,
                             download_name='shortest_path.kml'), 200

        # If KML is not requested, return the JSON response with the shortest path
        return jsonify({'path': shortest_path}), 200

    # Handle potential errors such as invalid input or computation failure
    except (ValueError, TypeError) as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 500


# Run the Flask application if the script is executed directly
if __name__ == '__main__':
    app.run()
