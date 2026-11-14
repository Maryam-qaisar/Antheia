from flask import Flask, render_template, jsonify, send_from_directory
from pathlib import Path
import csv

app = Flask(__name__)

# Project locations
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"
MAP_DIR = OUTPUT_DIR / "maps"
CSV_FILE = OUTPUT_DIR / "district_statistics.csv"


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