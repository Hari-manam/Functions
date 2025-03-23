from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Setup Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Runs in background
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Cricbuzz IPL 2020 match list URL (excluding final)
ipl_url = "https://www.cricbuzz.com/cricket-series/3130/indian-premier-league-2020/matches"
driver.get(ipl_url)
time.sleep(5)  # Allow page to load

# Step 1: Get all match URLs
match_links = []
all_matches = driver.find_elements(By.CSS_SELECTOR, "a.text-hvr-underline")
for match in all_matches:
    link = match.get_attribute("href")
    if link and "match" in link and "final" not in link.lower():
        match_links.append(link.replace("scorecard", "commentary"))

print(f"Total matches found: {len(match_links)}")

# Step 2: Scrape ball-by-ball commentary
all_commentary = []

def scrape_commentary(match_url):
    driver.get(match_url)
    time.sleep(5)  # Allow full page load
    
    # Scroll to load full commentary
    body = driver.find_element(By.TAG_NAME, "body")
    for _ in range(20):  # Increase scroll count to load more content
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

    # Extract match title
    try:
        match_title = driver.find_element(By.CLASS_NAME, "cb-nav-hdr").text
    except:
        match_title = "Unknown Match"

    print(f"Scraping: {match_title}")

    # Extract ball-by-ball commentary
    overs = driver.find_elements(By.CSS_SELECTOR, "div.cb-col.cb-col-8.text-bold")
    comments = driver.find_elements(By.CSS_SELECTOR, "div.cb-col.cb-col-90.cb-com-ln")

    if not overs or not comments:
        print(f"⚠ No commentary found for {match_url}. Adjusting scroll behavior.")

    for over, comment in zip(overs, comments):
        all_commentary.append({"Match": match_title, "Over": over.text, "Commentary": comment.text})

# Step 3: Loop through each match and extract commentary
for idx, match_url in enumerate(match_links):
    print(f"Scraping Match {idx + 1} of {len(match_links)}: {match_url}")
    scrape_commentary(match_url)
    time.sleep(2)  # Prevent IP blocking

# Step 4: Save to CSV
df = pd.DataFrame(all_commentary)
df.to_csv("IPL_2020_Commentary.csv", index=False)

# Close WebDriver
driver.quit()

print("✅ Scraping complete! Commentary saved to 'IPL_2020_Commentary.csv'.")
