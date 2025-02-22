from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-notifications')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

try:
    print("Starting the scraper...")
    driver = setup_driver()
    wait = WebDriverWait(driver, 30)  # Increased wait time

    # Navigate to website
    url = "https://www.remotejobs.io/search?searchkeyword=data+scientist&searchtype=basic"
    print(f"Navigating to {url}")
    driver.get(url)
    time.sleep(5)  # Wait for initial load

    # Scroll down to load more content
    print("Scrolling page to load content...")
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # Open and clear the file
    with open('job_listings.txt', 'w', encoding='utf-8') as file:
        file.write("")  # Clear the file

    print("Waiting for job listings to load...")
    # Wait for job cards and get them
    job_cards = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//div[contains(@class, 'sc-jv5lm6-0')]")
    ))
    print(f"Found {len(job_cards)} job listings")

    # Process each job card
    for index, job in enumerate(job_cards, 1):
        try:
            # Get job details with explicit waits
            title = wait.until(EC.presence_of_element_located(
                (By.XPATH, ".//h3[contains(@class, 'dPMOze')]//a")
            )).text.strip()

            # Only process if it's a data scientist position
            if not any(keyword in title.upper() for keyword in ["DATA SCIENTIST", "DATA SCIENCE"]):
                continue

            # Get other details
            location = job.find_element(By.XPATH, ".//span[contains(@class, 'ksCdkd')]").text.strip()
            
            try:
                posted_time = job.find_element(By.XPATH, ".//span[contains(@class, 'sc-jv5lm6-12')]").text.strip()
            except:
                posted_time = "Recently posted"

            try:
                job_type = job.find_element(By.XPATH, ".//span[contains(text(), 'Full-time') or contains(text(), 'Part-time')]").text.strip()
            except:
                job_type = "Full-time"

            try:
                pay_range = job.find_element(By.XPATH, ".//span[contains(text(), '$')]").text.strip()
            except:
                pay_range = "Salary not specified"

            # Print to console for debugging
            print(f"\nProcessing job {index}:")
            print(f"Title: {title}")
            print(f"Location: {location}")
            print(f"Posted: {posted_time}")
            print(f"Type: {job_type}")
            print(f"Pay: {pay_range}")

            # Append to file
            with open('job_listings.txt', 'a', encoding='utf-8') as file:
                file.write(f"Title: {title}\n")
                file.write(f"Location: {location}\n")
                file.write(f"Posted: {posted_time}\n")
                file.write(f"Type: {job_type}\n")
                file.write(f"Pay: {pay_range}\n")
                file.write("\n")  # Add blank line between entries

        except Exception as e:
            print(f"Error processing job {index}: {str(e)}")
            continue

    print("\nScript completed. Check job_listings.txt for results.")

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    print("Closing browser...")
    driver.quit()