import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the job site URL
job_url = "https://remoteok.io/remote-dev-jobs"

#  Set headers to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

#  Send a request to fetch the page content
response = requests.get(job_url, headers=headers)

#  Parse the HTML with BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

#  Extract job titles using correct selector
job_titles = soup.find_all("h2", itemprop="title")

#  Extract company names using correct selector
company_names = soup.select("td.company.position.company_and_position a")

#  Extract job locations (if available)
locations = soup.find_all("div", class_="location")

#  Store results
job_list = []
for i in range(min(len(job_titles), len(company_names), len(locations))):
    job_title = job_titles[i].text.strip() if job_titles[i].text else "N/A"
    company = company_names[i].text.strip() if company_names[i].text else "N/A"
    location = locations[i].text.strip() if locations[i].text else "Remote"

    job_list.append([job_title, company, location])

# Convert to DataFrame and Save to CSV
df = pd.DataFrame(job_list, columns=["Job Title", "Company", "Location"])
df.to_csv("remoteok_jobs_fixed.csv", index=False)

print(" Job listings scraped and saved successfully!")
