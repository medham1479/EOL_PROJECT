from bs4 import BeautifulSoup
import requests


def scrape_eol_info(self, software_name):
    """Scrape end-of-life information for the given software name from endoflife.date."""
    try:
        # Construct the software-specific URL
        url = f"{self.base_url}/{software_name.lower().replace(' ', '-')}"
        print(f"Constructed URL: {url}") # Debugging: Log the URL being scraped
        
        # Send a request to the URL
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the EOL table
        eol_table = soup.find("table", class_="table-auto")
        if not eol_table:
            return f"No EOL information found for {software_name}."

        # Extract EOL data from the table
        eol_data = []
        for row in eol_table.find_all("tr")[1:]:  # Skip the header row
            columns = row.find_all("td")
            if len(columns) >= 3:
                version = columns[0].text.strip()
                release_date = columns[1].text.strip()
                eol_date = columns[2].text.strip()
                eol_data.append({
                    "Version": version,
                    "Release Date": release_date,
                    "End of Life Date": eol_date
                })

        return eol_data if eol_data else f"No EOL data available for {software_name}."
    except Exception as e:
        return f"Error scraping data for {software_name}: {str(e)}"