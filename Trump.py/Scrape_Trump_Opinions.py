# Imports
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# ---------- FOX NEWS OPINIONS SPECIFICALLY FOR "TRUMP 2024" ---------- #
fox_search_url = "https://www.foxnews.com/search-results/search?q=Trump%202024"
headers = {'User-Agent': 'Mozilla/5.0'}

fox_response = requests.get(fox_search_url, headers=headers)
fox_soup = BeautifulSoup(fox_response.content, 'html.parser')
fox_articles = []

for article in fox_soup.select("article.article"):
    headline_tag = article.select_one("h4.title")
    if not headline_tag:
        continue

    headline = headline_tag.get_text(strip=True)
    link_tag = article.select_one("a")
    if not link_tag or 'href' not in link_tag.attrs:
        continue

    link = link_tag['href']
    full_link = link if link.startswith('http') else f"https://www.foxnews.com{link}"

    article_resp = requests.get(full_link, headers=headers)
    article_soup = BeautifulSoup(article_resp.content, 'html.parser')
    paragraphs = article_soup.select("div.article-body p")

    content = " ".join(p.get_text(strip=True) for p in paragraphs)

    # ✅ Only include articles explicitly mentioning "Trump 2024"
    if "Trump 2024" in content or "Trump 2024" in headline:
        fox_articles.append({
            'Headline': headline,
            'URL': full_link,
            'Content': content
        })
        print(f"✅ Scraped Fox News article: {headline}")

# Save to CSV clearly
fox_csv = "FoxNews_Expert_Opinions_2024.csv"
pd.DataFrame(fox_articles).to_csv(fox_csv, index=False)
print(f"✅ Fox News 2024 opinions saved to {fox_csv}")

# ---------- QUORA PUBLIC OPINIONS CLEARLY FOR "DONALD TRUMP 2024" ---------- #
query = "Donald Trump 2024"
quora_url = f"https://www.quora.com/search?q={query.replace(' ', '%20')}"

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(quora_url)

WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.q-box'))
)
time.sleep(3)

# Scroll to load dynamic results clearly
for _ in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

questions = driver.find_elements(By.CSS_SELECTOR, "div.q-box.qu-mb--tiny a.q-box")
quora_data = []

# Collect question links & titles clearly
question_links = []
for question in questions[:10]:
    href = question.get_attribute('href')
    title = question.text.strip()
    if href and title:
        question_links.append((title, href))

for title, link in question_links:
    try:
        driver.get(link)
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.q-relative span.q-box span"))
        )
        time.sleep(2)

        answer_elements = driver.find_elements(By.CSS_SELECTOR, "div.q-relative span.q-box span")
        answers_text = [answer.text.strip() for answer in answer_elements if answer.text.strip()][:3]

        quora_data.append({
            'Question': title,
            'URL': link,
            'Top_Answers': " ||| ".join(answers_text)
        })
        print(f"✅ Scraped Quora question: {title}")

    except Exception as e:
        print(f"⚠️ Error scraping '{title}': {e}")

driver.quit()

# Save to CSV clearly
quora_csv = "Quora_Public_Opinions_2024.csv"
pd.DataFrame(quora_data).to_csv(quora_csv, index=False)
print(f"✅ Quora public opinions saved to {quora_csv}")
