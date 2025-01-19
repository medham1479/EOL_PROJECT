from flask import Flask, jsonify, request
from indexer.indexer import Indexer  # Ensure this is the correct import path

app = Flask(__name__)
indexer = Indexer()

@app.route('/api/eol_info', methods=['GET'])
def get_eol_info():
    software_name = request.args.get('name')  # Get the software name from query parameters
    if software_name:
        eol_info = indexer.get_eol_info(software_name)  # Assume this method exists
        if eol_info:
            return jsonify(eol_info), 200
        else:
            return jsonify({"error": "No EOL information found"}), 404
    return jsonify({"error": "Please provide a software name"}), 400

if __name__ == '__main__':
    print("Starting API server...")
    app.run(debug=True, port=5001)