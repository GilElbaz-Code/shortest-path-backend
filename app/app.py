from flask import Flask, request, jsonify
from flask_cors import CORS
from objects.graph_manager import GraphManager
from utils.validators import Validators

app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for React
CORS(app, expose_headers=["Content-Disposition"])

# Create an instance of the GraphManager class for managing graphs
graph_manager = GraphManager()


@app.route('/calculate_shortest_path', methods=['POST'])
def calculate_shortest_path():
    try:
        request_input = request.get_json()

        # Check for required fields and their existence
        if not all(key in request_input for key in ['start', 'end']):
            return jsonify({'error': 'Both "start" and "end" keys are required in the input'}), 400

        # Validate start and end dictionaries
        start = request_input.get('start')
        if not Validators.validate_node_dict(node_dict=start):
            return jsonify({'error': 'Invalid format or non-numeric values in the "start" dictionary'}), 400

        end = request_input.get('end')
        if not Validators.validate_node_dict(node_dict=end):
            return jsonify({'error': 'Invalid format or non-numeric values in the "end" dictionary'}), 400

        # Validate kml_requested (optional)
        kml_requested = request_input.get('kml', False)
        if not isinstance(kml_requested, bool):
            return jsonify({'error': 'Invalid value for "kml". It should be a boolean.'}), 400

        result = graph_manager.calculate_shortest_path(start=start, end=end, kml_requested=kml_requested)
        return result.process_result()

    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return jsonify({'error': error_message}), 500


if __name__ == '__main__':
    app.run()
