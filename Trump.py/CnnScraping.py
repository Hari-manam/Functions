import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

base_search_url = "https://edition.cnn.com/search?q=Trump+Politics+2024&size=10&sort=relevance&page={}"

articles_data = []

# Scrape clearly first two pages
for page_num in [1, 2]:
    search_url = base_search_url.format(page_num)
    driver.get(search_url)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.container__link"))
    )
    time.sleep(2)

    article_links = [a.get_attribute('href') for a in driver.find_elements(By.CSS_SELECTOR, "a.container__link")]
    print(f"✅ Page {page_num}: Found {len(article_links)} articles.")

    for link in article_links:
        driver.get(link)
        time.sleep(2)

        # Extract Headline robustly
        try:
            headline = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.headline_live-story__text.inline-placeholder.vossi-headline-text"))
            ).text
        except:
            try:
                headline = driver.find_element(By.TAG_NAME, "h1").text
            except:
                headline = "No headline found"

        # Extract Content robustly
        paragraphs = driver.find_elements(By.CSS_SELECTOR,
            "div.live-story-post__content p.paragraph.inline-placeholder.vossi-paragraph")

        if not paragraphs:  # Fallback for standard articles
            paragraphs = driver.find_elements(By.CSS_SELECTOR,
                "div.article__content p, div.l-container p, section#body-text p")

        content = "\n\n".join([para.text for para in paragraphs if para.text.strip()])

        if content.strip() == "":
            content = "No content found or content could not be extracted."

        articles_data.append({"URL": link, "Headline": headline, "Content": content})
        print(f"✅ Scraped: {headline}")

# Save clearly to CSV
csv_file = "CNN_Trump_Politics2024_FirstTwoPages.csv"
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["URL", "Headline", "Content"])
    writer.writeheader()
    writer.writerows(articles_data)

print("✅ Done! All detailed articles clearly saved to CNN_Trump_Politics2024_FirstTwoPages.csv")

driver.quit()
