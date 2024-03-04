from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from constants import Constants
from graph_manager import GraphManager

# Create a Flask application instance
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for the application
CORS(app, expose_headers=["Content-Disposition"])

# Create an instance of the GraphManager class for managing graphs
graph_manager = GraphManager()

# Define a route for handling POST requests to calculate the shortest path
@app.route('/calculate_shortest_path', methods=['POST'])
def calculate_shortest_path():
    try:
        # Retrieve JSON input from the POST request
        request_input = request.get_json()

        # Extract start, end, and kml_requested from the input
        start = request_input.get('start')
        end = request_input.get('end')
        kml_requested = request_input.get('kml', False)

        # Calculate the shortest path using the GraphManager
        shortest_path = graph_manager.calculate_shortest_path(start=start, end=end, kml_requested=kml_requested)

        # If the result is a string, assume it's a file path and return it as a downloadable KML file
        if isinstance(shortest_path, str):
            return send_file(shortest_path,
                             mimetype=Constants.KML_MIMETYPE,
                             as_attachment=True,
                             download_name='shortest_path.kml'), 200

        # If the result is not a string, assume it's a list of nodes representing the shortest path and return it as JSON
        return jsonify({'path': shortest_path}), 200

    except Exception as e:
        # Handle unexpected errors and return a 500 Internal Server Error response with an error message
        error_message = f"An unexpected error occurred: {str(e)}"
        return jsonify({'error': error_message}), 500

# Run the Flask application if this script is executed directly
if __name__ == '__main__':
    app.run()
