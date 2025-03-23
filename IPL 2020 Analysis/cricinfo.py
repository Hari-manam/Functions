import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Dictionary of URLs for each stat you want to scrape
records_urls = {
    "most_runs": "https://www.espncricinfo.com/records/trophy/batting-most-runs-career/indian-premier-league-117",
    "most_wickets": "https://www.espncricinfo.com/records/trophy/bowling-most-wickets-career/indian-premier-league-117",
    "best_bowling": "https://www.espncricinfo.com/records/trophy/bowling-best-figures-innings/indian-premier-league-117",
    "highest_team_totals": "https://www.espncricinfo.com/records/trophy/team-highest-innings-totals/indian-premier-league-117",
    "most_catches": "https://www.espncricinfo.com/records/trophy/fielding-most-catches-career/indian-premier-league-117",
    "result_summary": "https://www.espncricinfo.com/records/trophy/team-results-summary/indian-premier-league-117"
}

def scrape_and_combine(url_dict):
    """
    For each record type in url_dict:
      1. Open the page in Selenium.
      2. Wait for the page to load.
      3. Parse the HTML content with pandas.read_html().
      4. Add a 'record_type' column.
      5. Clean column names.
    Finally, combine all DataFrames into a single DataFrame.
    """
    # Set up the Selenium ChromeDriver service
    # Update the path to your chromedriver if necessary
    service = Service("C:\\WebDrivers\\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    
    combined_dfs = []  # List to store DataFrames from each page
    
    try:
        for stat_name, url in url_dict.items():
            print(f"Scraping {stat_name} from {url} ...")
            driver.get(url)
            # Wait for the page to fully load (adjust time if needed or use explicit waits)
            time.sleep(5)
            
            html_content = driver.page_source
            try:
                tables = pd.read_html(html_content)
                if tables:
                    df = tables[0]  # usually the main data table is the first one
                    # Add a column for record type
                    df['record_type'] = stat_name
                    # Standardize column names: strip whitespace, lowercase, replace spaces with underscores
                    df.rename(columns=lambda x: x.strip().lower().replace(" ", "_"), inplace=True)
                    combined_dfs.append(df)
                    print(f"Scraped {stat_name} successfully with {len(df)} rows.")
                else:
                    print(f"No tables found for {stat_name}.\n")
            except Exception as e:
                print(f"Error parsing table from {url}: {e}\n")
    finally:
        # Close the browser once done
        driver.quit()
        
    # Combine all DataFrames if any were scraped
    if combined_dfs:
        combined_df = pd.concat(combined_dfs, ignore_index=True)
        # Optional: further cleaning steps can be added here
        return combined_df
    else:
        return pd.DataFrame()  # return an empty DataFrame if nothing was scraped

if __name__ == "__main__":
    combined_df = scrape_and_combine(records_urls)
    if not combined_df.empty:
        output_filename = "ipl_records_combined.csv"
        combined_df.to_csv(output_filename, index=False)
        print(f"\nCombined data saved to '{output_filename}'.")
    else:
        print("No data was scraped.")
