from flask import Flask, render_template, jsonify, send_from_directory, request
from pathlib import Path
import json
import csv
import numpy as np
from shapely.geometry import shape, Point
from pyproj import Transformer


app = Flask(__name__)

# Project locations
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"
MAP_DIR = OUTPUT_DIR / "maps"
CSV_FILE = OUTPUT_DIR / "district_statistics.csv"
DATA_FILE = BASE_DIR / "outputs" / "data" / "agri_pulse_data.npz"
GEOJSON_FILE = BASE_DIR /"data"/"reference"/ "faisalabad_district.geojson"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/statistics")
def statistics():

    records = []

    if CSV_FILE.exists():
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                records.append(row)

    return jsonify(records)


@app.route("/maps/<filename>")
def show_map(filename):

    allowed_maps = {
        "HH_30_Oct.png",
        "HH_11_Nov.png",
        "HH_change.png",
        "HV_30_Oct.png",
        "HV_11_Nov.png",
        "HV_change.png"
    }

    if filename not in allowed_maps:
        return "Map not found", 404

    return send_from_directory(MAP_DIR, filename)
@app.route("/api/study-area")
def study_area():
    if not GEOJSON_FILE.exists():
        return jsonify({"error": "Study area boundary not found"}), 404

    with open(GEOJSON_FILE, "r", encoding="utf-8") as file:
        boundary = json.load(file)

    return jsonify(boundary)

@app.route("/api/location-values")
def location_values():

    # Read selected geographic coordinates
    try:
        latitude = float(request.args.get("lat"))
        longitude = float(request.args.get("lon"))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid coordinates"}), 400

    if not np.isfinite(latitude) or not np.isfinite(longitude):
        return jsonify({"error": "Invalid coordinates"}), 400

    if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
        return jsonify({"error": "Coordinates out of range"}), 400

    if not DATA_FILE.exists() or not GEOJSON_FILE.exists():
        return jsonify({"error": "Required data files not found"}), 404

    # Verify the selected point is inside Faisalabad
    with open(GEOJSON_FILE, "r", encoding="utf-8") as file:
        boundary_data = json.load(file)

    district = shape(boundary_data["features"][0]["geometry"])
    selected_point = Point(longitude, latitude)

    if not district.covers(selected_point):
        return jsonify({
            "error": "Selected location is outside Faisalabad District"
        }), 400

    # Convert geographic coordinates to the radar grid CRS
    transformer = Transformer.from_crs(
        "EPSG:4326",
        "EPSG:32643",
        always_xy=True
    )

    x, y = transformer.transform(longitude, latitude)

    try:
        with np.load(DATA_FILE, allow_pickle=False) as data:

            x_coordinates = data["x_coordinates"]
            y_coordinates = data["y_coordinates"]

            # Find nearest grid cell
            column = int(np.argmin(np.abs(x_coordinates - x)))
            row = int(np.argmin(np.abs(y_coordinates - y)))

            # Confirm the selected point falls within the grid cell
            x_distance = abs(x_coordinates[column] - x)
            y_distance = abs(y_coordinates[row] - y)

            if x_distance > 50.1 or y_distance > 50.1:
                return jsonify({
                    "error": "No radar coverage at this location"
                }), 404

            # Retrieve all six radar measurements
            keys = [
                "hh_30_oct",
                "hh_11_nov",
                "hh_change",
                "hv_30_oct",
                "hv_11_nov",
                "hv_change"
            ]

            values = {}

            for key in keys:
                value = float(data[key][row, column])

                values[key] = (
                    round(value, 4)
                    if np.isfinite(value)
                    else None
                )

            valid_count = sum(
                value is not None for value in values.values()
            )

            if valid_count == 0:
                status = "No valid radar observations"
            elif valid_count == len(keys):
                status = "All six observations available"
            else:
                status = "Partial radar observations available"

            pixel_longitude, pixel_latitude = transformer.transform(
                float(x_coordinates[column]),
                float(y_coordinates[row]),
                direction="INVERSE"
            )

            return jsonify({
                "status": status,
                "selected_location": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "grid_cell": {
                    "row": row,
                    "column": column,
                    "latitude": pixel_latitude,
                    "longitude": pixel_longitude,
                    "resolution": "100 m"
                },
                "measurements": values
            })

    except (KeyError, ValueError, OSError) as error:
        return jsonify({
            "error": "Unable to retrieve radar measurements",
            "details": str(error)
        }), 500
    
@app.route("/api/status")
def status():

    return jsonify({
        "project": "AgriPulse",
        "study_area": "Faisalabad District",
        "data_available": CSV_FILE.exists(),
        "maps_available": MAP_DIR.exists()
    })


if __name__ == "__main__":
    print("Starting AgriPulse dashboard...")
    print("Project directory:", BASE_DIR)

    app.run(debug=True, port=5000)