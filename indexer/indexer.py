import pandas as pd

class Indexer:
    def __init__(self):
        self.data = []

    def add_to_index(self, url, eol_info):
        self.data.append({'URL': url, 'End of Life Info': eol_info})

    def save_index(self, filename='index.csv'):
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)

    def get_eol_info(self, software_name):
        """Retrieve EOL info for a given software name."""
        for entry in self.data:
            if software_name.lower() in entry['End of Life Info'].lower():
                return entry
        return None

    def add_eol_info(self, software_name, eol_info, url):
        """Add new EOL info to the indexer."""
        self.add_to_index(url, f"{software_name}: {eol_info}")