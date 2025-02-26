from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os
import time
from urllib.parse import urljoin

def create_folders():
    """Create folders for storing images and videos"""
    # Create folders for images and videos
    folders = ['scraped_images', 'scraped_videos']
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
    return folders[0], folders[1]

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

def download_image(url, folder, index):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Save the image
            filename = os.path.join(folder, f'image_{index}.jpg')
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Saved image {index}")
            return True
    except Exception as e:
        print(f"Error downloading image {index}: {e}")
    return False

def main():
    driver = None
    try:
        # Create folders
        images_folder, videos_folder = create_folders()
        
        # Setup driver
        driver = setup_driver()
        if not driver:
            return

        # Use Pexels URL (more scraping-friendly)
        url = "https://www.pexels.com/search/nature/"
        print(f"\nNavigating to {url}")
        driver.get(url)
        time.sleep(5)  # Wait for page to load

        print("\nSearching for images...")
        # Find images with specific class names used by Pexels
        images = driver.find_elements(By.CSS_SELECTOR, "img.photo-item__img")
        image_count = 0
        
        for i, img in enumerate(images):
            try:
                src = img.get_attribute('src')
                if not src:  # Try data-src if src is not available
                    src = img.get_attribute('data-src')
                
                if src:
                    print(f"Found image: {src}")
                    full_url = urljoin(url, src)
                    if download_image(full_url, images_folder, i):
                        image_count += 1
                        print(f"Successfully downloaded image {i+1}")
                        
                        # Limit to 10 images for testing
                        if image_count >= 10:
                            break
            except Exception as e:
                print(f"Error processing image {i}: {e}")
                continue

        print(f"\nScraping completed!")
        print(f"Images downloaded: {image_count}")
        print(f"\nCheck '{images_folder}' for images")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        if driver:
            print("\nClosing browser...")
            driver.quit()

if __name__ == "__main__":
    main()