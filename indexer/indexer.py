import pandas as pd
import os

class Indexer:
    def __init__(self, filename="index.csv"):
        self.filename = filename
        self.data = []
        self.load_index()

    def load_index(self):
        """Load existing EOL data from CSV file."""
        if os.path.exists(self.filename):
            self.data = pd.read_csv(self.filename).to_dict(orient="records")

    def add_to_index(self, software_name, eol_info, url):
        """Store new EOL info."""
        entry = {"Software": software_name, "EOL Info": eol_info, "URL": url}
        self.data.append(entry)
        self.save_index()

    def save_index(self):
        """Save data to CSV."""
        pd.DataFrame(self.data).to_csv(self.filename, index=False)

    def get_eol_info(self, software_name):
        """Retrieve EOL info for a given software name."""
        for entry in self.data:
            if software_name.lower() in entry["Software"].lower():
                return entry
        return None