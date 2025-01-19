import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask, jsonify, request
from indexer.indexer import Indexer
from crawler.crawler import EOLScraper

app = Flask(__name__)
indexer = Indexer()
scraper = EOLScraper(indexer)  # Pass the indexer to the scraper

@app.route('/api/eol_info', methods=['GET'])
def get_eol_info():
    software_name = request.args.get('name')
    if software_name:
        eol_info = indexer.get_eol_info(software_name)
        
        if not eol_info:
            eol_info = scraper.search_and_scrape(software_name)

        if eol_info:
            return jsonify(eol_info), 200
        else:
            return jsonify({"error": "No EOL information found"}), 404
    return jsonify({"error": "Please provide a software name"}), 400

if __name__ == '__main__':
    print("Starting API server...")
    app.run(debug=True, port=5001)