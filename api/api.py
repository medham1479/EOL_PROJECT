import sys
import os
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

    # Try fetching from the index first
    eol_info = indexer.get_eol_info(software_name)
    
    if not eol_info:
        # If not found in the index, scrape the data
        eol_info = scraper.fetch_eol_info(software_name)
        if eol_info:
            indexer.add_to_index(software_name, eol_info, f"https://endoflife.date/{software_name.lower().replace(' ', '-')}")
    
    if eol_info:
        # Prioritize different levels of support
        priority_order = ["Support", "Active Support", "Critical Support", "Security Support"]
        sorted_info = sorted(eol_info, key=lambda x: priority_order.index(x.get("support_status", "Security Support")) if x.get("support_status") in priority_order else len(priority_order))
        return jsonify(sorted_info)

    return jsonify({"error": "No EOL information found"}), 404

if __name__ == "__main__":
    print("Starting API server...")
    app.run(debug=True, port=5001)
