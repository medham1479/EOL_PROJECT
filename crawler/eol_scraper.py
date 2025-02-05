import requests

class EOLScraper:
    def __init__(self):
        self.api_base_url = "https://endoflife.date/api"

    def fetch_software_list(self):
        """Fetches a list of software available in the API."""
        try:
            response = requests.get(f"{self.api_base_url}/all.json")
            response.raise_for_status()  # Raise an error for HTTP issues

            data = response.json()
            print("Fetched Software List:", data)  # Debugging log

            if isinstance(data, list):
                return [software["name"] for software in data]
            else:
                print("Unexpected API response format:", data)
                return []
        except requests.RequestException as e:
            print(f"Error fetching software list: {e}")
            return []

    def fetch_eol_info(self, software):
        """Fetches EOL information for a given software."""
        try:
            formatted_software = software.lower().replace(" ", "-")  # Format name for API
            response = requests.get(f"{self.api_base_url}/{formatted_software}.json")
            response.raise_for_status()

            data = response.json()
            print(f"Raw EOL Data for {software}:")
            print(data)  # Debugging log to inspect raw data

            # Check if the data is a list of dictionaries
            if isinstance(data, list):
                eol_info = []
                for entry in data:
                    # Print details for debugging
                    print(f"Processing version: {entry['cycle']}, Details: {entry}")
                    
                    version = entry['cycle']
                    release_date = entry.get('releaseDate', 'N/A')
                    eol_date = entry.get('eol', 'N/A')
                    latest_version = entry.get('latest', 'N/A')
                    latest_release_date = entry.get('latestReleaseDate', 'N/A')

                    # Determine the support status in the correct order
                    if eol_date != 'N/A' and eol_date != False:
                        support_status = eol_date  # If there is an EOL date, use it
                    elif entry.get('lts', False):
                        support_status = 'Active Support'  # If it’s an LTS version, use Active Support
                    elif eol_date == False:
                        support_status = 'Critical Support'  # If eol is False, it's critical support
                    else:
                        support_status = 'Security Support'  # Default fallback to Security Support
                    
                    eol_info.append({
                        "version": version,
                        "release_date": release_date,
                        "eol_date": eol_date,
                        "latest_version": latest_version,
                        "latest_release_date": latest_release_date,
                        "support_status": support_status
                    })

                return eol_info
            else:
                print("Unexpected API response format:", data)
                return []

        except requests.RequestException as e:
            print(f"Error fetching EOL info for {software}: {e}")
            return []

    def print_eol_info(self, software):
        """Prints EOL information for a given software."""
        eol_data = self.fetch_eol_info(software)
        if not eol_data:
            print(f"No EOL data found for {software}.")
            return

        print(f"\nEnd-of-Life Information for {software}:")
        for entry in eol_data:
            print(f"- Version: {entry['version']}")
            print(f"  - Release Date: {entry['release_date']}")
            print(f"  - Latest Version: {entry['latest_version']}")
            print(f"  - Latest Release Date: {entry['latest_release_date']}")
            print(f"  - EOL Date: {entry['eol_date']}")
            print(f"  - Support Status: {entry['support_status']}")

# Example Usage
scraper = EOLScraper()
scraper.print_eol_info("Apache APISIX")  # Fetch and print EOL info for Apache APISIX
