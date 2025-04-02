import sys
import os
import csv
from flask import Flask, jsonify, request, render_template 

try:
    from indexer import Indexer
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from indexer import Indexer

try:
    from crawler.eol_scraper import EOLScraper
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from crawler.eol_scraper import EOLScraper

app = Flask(__name__, template_folder="templates", static_folder="static")

indexer = Indexer()
scraper = EOLScraper()

# Path to the CSV file where data is stored
CSV_FILE = 'index.csv'

def read_csv_data():
    """Reads the index.csv file and returns it as a dictionary."""
    data = {}
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            for row in reader:
                software_name, eol_data = row[0], row[1]
                data[software_name.lower()] = eol_data
    return data

def save_to_csv(software_name, eol_info):
    """Saves EOL info to the index.csv file."""
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write software name and EOL data
        writer.writerow([software_name, eol_info])

@app.route("/")
def home():
    """Serve the front-end page."""
    return render_template("index.html")

@app.route("/api/eol_info", methods=["GET"])
def get_eol_info():
    """Fetch EOL info for the given software name and return the most relevant status."""
    software_name = request.args.get("name")
    if not software_name:
        return jsonify({"error": "Please provide a software name"}), 400

    # Check if the software name exists in the CSV first
    data = read_csv_data()
    software_name_lower = software_name.lower()

    # If data is in CSV, return it
    if software_name_lower in data:
        return jsonify(eval(data[software_name_lower]))  # Convert string back to list of dicts

    # scrape the data
    eol_info = indexer.get_eol_info(software_name)
    if not eol_info:
        eol_info = scraper.fetch_eol_info(software_name)

    if eol_info:
        # Save the data to CSV
        save_to_csv(software_name, str(eol_info))
        
        # Prioritize different levels of support
        priority_order = ["Support", "Active Support", "Critical Support", "Security Support"]
        sorted_info = sorted(
            [item for item in eol_info if isinstance(item, dict)],  # Filter out non-dictionaries
            key=lambda x: priority_order.index(x.get("support_status", "Security Support"))
            if x.get("support_status") in priority_order else len(priority_order)
        )
        return jsonify(sorted_info)

    return jsonify({"error": "No EOL information found"}), 404

if __name__ == "__main__":
    print("Starting API server...")
    app.run(debug=True, port=5001)
