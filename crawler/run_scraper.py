from eol_scraper import scrape_eol_info  # Ensure this matches your EOLScraper file

def main():
    try:
        # Define the software name
        software_name = input("Enter the software name: ").strip()
        
        # Base URL for the endoflife.date site
        base_url = "https://endoflife.date"
        
        print(f"Scraping EOL information for: {software_name}")  # Debugging statement

        # Call the scrape_eol_info function
        eol_data = scrape_eol_info({"base_url": base_url}, software_name)

        # Check and print the 
        if isinstance(eol_data, list):
            print(f"EOL information for {software_name}:")
            for entry in eol_data:
                print(f"Version: {entry['Version']}, Release Date: {entry['Release Date']}, End of Life Date: {entry['End of Life Date']}")
        else:
            print(eol_data)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()