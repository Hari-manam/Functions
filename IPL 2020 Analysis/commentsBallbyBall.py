import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Chrome setup
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Fetch match URLs (excluding the final)
base_url = "https://www.cricbuzz.com/cricket-series/3130/indian-premier-league-2020/matches"
driver.get(base_url)
time.sleep(5)

match_elements = driver.find_elements(By.CSS_SELECTOR, "a.text-hvr-underline")
match_urls = [
    elem.get_attribute("href").replace("scorecard", "commentary")
    for elem in match_elements
    if "live-cricket-scorecard" in elem.get_attribute("href")
]

# Exclude the last match (final)
match_urls = match_urls[:-1]

print(f"Found {len(match_urls)} matches.")

# Function to scrape single match commentary
def scrape_match(url):
    driver.get(url)
    time.sleep(5)

    # Scroll until all comments loaded
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.cb-com-ln"))
        )
    except:
        print("Commentary elements did not load.")
        return []

    match_title = driver.find_element(By.CSS_SELECTOR, "h1.cb-nav-hdr").text
    commentary_blocks = driver.find_elements(By.CSS_SELECTOR, "div.cb-com-ln")

    commentary_data = []
    for block in commentary_blocks:
        try:
            ball = block.find_element(By.CSS_SELECTOR, "span.cb-col-8.text-bold").text
            comment = block.find_element(By.CSS_SELECTOR, "span.cb-col-90").text
            commentary_data.append({"Match": match_title, "Ball": ball, "Commentary": comment})
        except:
            continue

    return commentary_data

# Scrape all matches
all_comments = []
for idx, match_url in enumerate(match_urls):
    print(f"Scraping ({idx+1}/{len(match_urls)}): {match_url}")
    comments = scrape_match(match_url)
    all_comments.extend(comments)

driver.quit()

# Save to CSV
df = pd.DataFrame(all_comments)
df.to_csv("IPL_2020_Full_Commentary.csv", index=False)
print("Scraping complete! Data saved to IPL_2020_Full_Commentary.csv.")
