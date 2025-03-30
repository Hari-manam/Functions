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

