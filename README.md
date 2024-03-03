# Shortest Path Calculator

This Flask application calculates the shortest path between two points on a graph.
Optionally, it can generate a KML file representing the shortest path.
I developed it using Python 3.11.

## Setup

1. **Install dependencies:**
   pip install -r requirements.txt

2. **Run the server:**
   python app.py
   note: The application will be running at http://127.0.0.1:5000/.


## Usage

1. **Calculate Shortest Path:**
   Send a POST request to http://127.0.0.1:5000/calculate_shortest_path with the following JSON payload:
```yaml
POST /calculate_shortest_path

{
  "start": {"x": "x_value", "y": "y_value"},
  "end": {"x": "x_value", "y": "y_value"},
  "include_kml": true/false
}
```

   start_point: Coordinates of the starting point.
   
   end_point: Coordinates of the ending point.
   
   include_kml: Boolean indicating whether to include a KML file in the response.

2. **Response:**
   The response will contain either the shortest path or a download link for the KML file.
   If include_kml is set to true, the response will include the KML file.
   If include_kml is set to false, the response will contain the shortest path.


## Example

curl -X POST -H "Content-Type: application/json" -d '{"start": {"x": "30.1", "y": "34.3"},"end": {"x": "29.2", "y": "28.3"}, "kml": true}' http://127.0.0.1:5000/calculate_shortest_path

This example sends a POST request to calculate the shortest path between two points, including a KML file in the response.




