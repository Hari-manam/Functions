import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

# --------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------

# Adjust this path to your actual ChromeDriver executable location
driver_path = r"C:\WebDrivers\chromedriver.exe"

chrome_options = Options()
chrome_options.add_argument("--headless")   # Headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

service = Service(driver_path)

# The page listing all matches in IPL 2020
ipl2020_matches_url = "https://www.cricbuzz.com/cricket-series/3130/indian-premier-league-2020/matches"

# Output CSV file
output_csv = "ipl2020_data.csv"

# --------------------------------------------------------------------
# Helper Functions
# --------------------------------------------------------------------

def get_all_match_urls(driver, main_url):
    """
    Go to the 'matches' page for IPL 2020,
    parse out each match's link, and return them in a list.
    """
    driver.get(main_url)
    time.sleep(5)  # Wait for the page to load, adjust as needed

    soup = BeautifulSoup(driver.page_source, "html.parser")

    match_links = []
    # The CSS class 'cb-col-75 cb-col' holds the match info blocks
    # The anchor tags for each match usually have "text-hvr-underline"
    for tag in soup.select("a.text-hvr-underline"):
        href = tag.get("href", "")
        if "/live-cricket-scores/" in href or "/cricket-scores/" in href:
            full_link = "https://www.cricbuzz.com" + href
            if full_link not in match_links:
                match_links.append(full_link)

    return match_links


def scrape_match_details(driver, match_url):
    """
    Scrape summary details, results, and commentary from a match page.
    Returns a dictionary with the scraped data.
    """
    driver.get(match_url)
    time.sleep(4)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    data = {}
    data["match_url"] = match_url

    # Match Title
    match_title_tag = soup.find("h1", class_="cb-nav-hdr")
    data["match_title"] = match_title_tag.get_text(strip=True) if match_title_tag else ""

    # Sub-header (Series, Venue, Date & Time, etc.)
    sub_hdr = soup.find("div", class_="cb-nav-subhdr")
    data["match_subhdr"] = sub_hdr.get_text(" ", strip=True) if sub_hdr else ""

    # Try to get short 'status' or 'result' from known places
    # For instance, the status might be in a <div> with "cb-text-complete" or similar
    status_tag = soup.find("div", class_="cb-text-complete")
    if not status_tag:
        # Sometimes it's "cb-text-live" or "cb-text-inprogress"
        status_tag = soup.find("div", class_="cb-text-live") or soup.find("div", class_="cb-text-inprogress")
    data["match_status"] = status_tag.get_text(strip=True) if status_tag else ""

    # Full commentary is sometimes on a separate link "/cricket-full-commentary/xxxx"
    # But we'll attempt to parse the partial commentary from the main page
    # OR you can navigate to "full commentary" link:
    # We'll do a quick approach: gather paragraph tags from commentary area
    commentary_texts = []
    commentary_section = soup.find_all("p", class_="cb-com-ln")
    for comm_item in commentary_section:
        text = comm_item.get_text(strip=True)
        if text:
            commentary_texts.append(text)
    data["commentary"] = "\n".join(commentary_texts)

    return data


def main():
    driver = webdriver.Chrome(service=service, options=chrome_options)

    print("Fetching all match URLs for IPL 2020 ...")
    match_urls = get_all_match_urls(driver, ipl2020_matches_url)
    print(f"Total match URLs found: {len(match_urls)}")

    if not match_urls:
        print("No matches found. Please verify the CSS selectors or the page structure.")
        driver.quit()
        return

    # Open one CSV for all data
    with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
        fieldnames = ["match_url", "match_title", "match_subhdr", "match_status", "commentary"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for idx, url in enumerate(match_urls, start=1):
            print(f"Scraping {idx}/{len(match_urls)} => {url}")
            try:
                match_data = scrape_match_details(driver, url)
                writer.writerow(match_data)
            except Exception as exc:
                print(f"Error scraping {url} => {exc}")

    driver.quit()
    print("Scraping completed.")
    print(f"Data saved in: {output_csv}")


if __name__ == "__main__":
    main()
