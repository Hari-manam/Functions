from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import requests
from urllib.parse import urljoin

def setup_driver():
    try:
        print("\nSetting up Chrome driver...")
        options = Options()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--start-maximized')
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Error setting up driver: {e}")
        return None

def download_pdf(url, filename):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200 and response.headers.get('content-type', '').lower() == 'application/pdf':
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Successfully downloaded: {filename}")
            return True
        else:
            print(f"Failed to download {filename}: Not a valid PDF")
            return False
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
        return False

def create_download_folder():
    folder_name = "budget_pdfs"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

def main():
    driver = None
    try:
        # Create folder for PDFs
        download_folder = create_download_folder()
        
        driver = setup_driver()
        if not driver:
            return

        print("\nNavigating to AP Finance website...")
        base_url = "https://apfinance.gov.in/"
        driver.get(base_url)
        time.sleep(5)

        print("\nSearching for budget-related PDF links...")
        
        # Find all links
        links = driver.find_elements(By.TAG_NAME, "a")
        pdf_count = 0

        for link in links:
            try:
                href = link.get_attribute('href')
                text = link.text.lower()
                
                # Check if link is budget-related and points to a PDF
                if href and href.endswith('.pdf') and ('budget' in text or 'financial' in text):
                    pdf_url = urljoin(base_url, href)
                    filename = os.path.join(download_folder, f"budget_doc_{pdf_count + 1}.pdf")
                    
                    print(f"\nFound budget PDF: {text}")
                    print(f"Downloading from: {pdf_url}")
                    
                    if download_pdf(pdf_url, filename):
                        pdf_count += 1
                        
            except Exception as e:
                print(f"Error processing link: {e}")
                continue

        if pdf_count > 0:
            print(f"\nSuccessfully downloaded {pdf_count} budget-related PDFs to '{download_folder}' folder")
        else:
            print("\nNo budget-related PDFs found")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        if driver:
            print("\nClosing browser...")
            driver.quit()

if __name__ == "__main__":
    main()