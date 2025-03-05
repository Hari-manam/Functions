import time
import re
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def scrape_schedule(url):
    """
    Scrapes schedule and results data from the provided Cricbuzz matches page.
    Returns a list of rows: [Date, Match Title, Venue, Result, Time, Match URL].
    """
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    schedule_data = []
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        # Wait for the container that holds match info
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.cb-series-matches")))
        time.sleep(2)  # extra delay for content to load fully

        # Each match entry is typically in "div.cb-srs-mtchs-tm"
        match_entries = driver.find_elements(By.CSS_SELECTOR, "div.cb-srs-mtchs-tm")

        for match in match_entries:
            # Find the date from the preceding sibling 'schedule-date' container
            try:
                date_elem = match.find_element(
                    By.XPATH,
                    "./ancestor::div[contains(@class,'cb-series-matches')]"
                    "/preceding-sibling::div[contains(@class, 'schedule-date')]"
                )
                date_text = date_elem.text.strip()
            except:
                date_text = ""

            # Extract match title and link
            try:
                match_link_elem = match.find_element(By.TAG_NAME, "a")
                match_title = match_link_elem.text.strip()
                match_url = match_link_elem.get_attribute("href")  # e.g. /cricket-scores/89654/csk-vs-rcb-1st-match...
            except:
                match_title = ""
                match_url = ""

            # Venue (div with class 'text-gray')
            try:
                venue_elem = match.find_element(By.CSS_SELECTOR, "div.text-gray")
                venue = venue_elem.text.strip()
            except:
                venue = ""

            # Result (anchor with class 'cb-text-complete')
            try:
                result_elem = match.find_element(By.CSS_SELECTOR, "a.cb-text-complete")
                result = result_elem.text.strip()
            except:
                result = ""

            # Time (span with attribute format='h:mm a')
            try:
                time_elem = match.find_element(By.XPATH, ".//span[@format='h:mm a']")
                match_time = time_elem.text.strip()
            except:
                match_time = ""

            schedule_data.append([date_text, match_title, venue, result, match_time, match_url])

    except Exception as e:
        print("Error scraping schedule:", e)
    finally:
        driver.quit()

    return schedule_data


def scrape_stats(url):
    """
    1) Navigates to the Stats page (IPL 2024).
    2) Clicks on "Most Runs" under Batting, scrapes table.
    3) Clicks on "Most Wickets" under Bowling, scrapes table.
    Returns a dict with two lists:
        {
          "most_runs": [ [col1, col2, ...], [row2], ... ],
          "most_wickets": [ [col1, col2, ...], ... ]
        }
    """
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    data = {"most_runs": [], "most_wickets": []}

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)
        time.sleep(2)

        # Wait until the left nav for stats is present
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.cb-stats-nav-sidebar")))

        ## 1) Click "Most Runs" under Batting
        try:
            most_runs_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Most Runs')]")
            most_runs_link.click()
            time.sleep(2)  # let the table load
        except Exception as e:
            print("Could not click 'Most Runs' link:", e)

        # Wait for the table
        try:
            table_elem = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.cb-series-stats"))
            )
            rows = table_elem.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if cols:
                    data["most_runs"].append([c.text.strip() for c in cols])
        except Exception as e:
            print("Error scraping 'Most Runs' table:", e)

        ## 2) Click "Most Wickets" under Bowling
        try:
            most_wickets_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Most Wickets')]")
            most_wickets_link.click()
            time.sleep(2)
        except Exception as e:
            print("Could not click 'Most Wickets' link:", e)

        # Wait for the new table
        try:
            table_elem = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.cb-series-stats"))
            )
            rows = table_elem.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if cols:
                    data["most_wickets"].append([c.text.strip() for c in cols])
        except Exception as e:
            print("Error scraping 'Most Wickets' table:", e)

    except Exception as e:
        print("Error scraping stats:", e)
    finally:
        driver.quit()

    return data


def scrape_commentary(match_url):
    """
    1) Convert a match URL (e.g. /cricket-scores/89654/...) to the commentary URL
       ( /cricket-full-commentary/89654/... )
    2) Scrape all paragraphs with class 'cb-com-ln' (the main commentary lines).
    Returns a list of commentary lines (strings).
    """
    # Example match_url:
    #   https://www.cricbuzz.com/cricket-scores/89654/csk-vs-rcb-1st-match-indian-premier-league-2024
    # We transform it to:
    #   https://www.cricbuzz.com/cricket-full-commentary/89654/csk-vs-rcb-1st-match-indian-premier-league-2024
    commentary_url = match_url.replace("/cricket-scores/", "/cricket-full-commentary/")

    commentary_lines = []
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        driver.get(commentary_url)
        wait = WebDriverWait(driver, 15)
        # Wait for commentary container
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.cb-ful-comm")))
        time.sleep(2)

        # Grab all <p class="cb-com-ln">
        paragraphs = driver.find_elements(By.CSS_SELECTOR, "p.cb-com-ln")
        for p in paragraphs:
            text = p.text.strip()
            if text:
                commentary_lines.append(text)

    except Exception as e:
        print(f"Error scraping commentary for {commentary_url}:", e)
    finally:
        driver.quit()

    return commentary_lines


def write_to_csv(schedule_data, stats_data, filename="ipl2024_data.csv"):
    """
    Writes the schedule/results, 'Most Runs'/'Most Wickets' data,
    and commentary lines for each match to a single CSV.
    """
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Section 1: Schedule & Results
        writer.writerow(["=== SCHEDULE & RESULTS ==="])
        writer.writerow(["Date", "Match Title", "Venue", "Result", "Time", "Match URL"])
        writer.writerows(schedule_data)
        writer.writerow([])  # blank line

        # Section 2: Batting - Most Runs
        writer.writerow(["=== MOST RUNS (BATTING) ==="])
        if stats_data["most_runs"]:
            writer.writerows(stats_data["most_runs"])
        writer.writerow([])

        # Section 3: Bowling - Most Wickets
        writer.writerow(["=== MOST WICKETS (BOWLING) ==="])
        if stats_data["most_wickets"]:
            writer.writerows(stats_data["most_wickets"])
        writer.writerow([])

        # Section 4: Commentary for each match
        writer.writerow(["=== COMMENTARY for each match ==="])
        # We'll do a loop over schedule_data, re-scrape commentary for each
        # This can be time-consuming if many matches
        for i, row in enumerate(schedule_data, start=1):
            match_date, match_title, venue, result, match_time, match_url = row
            # Build commentary
            lines = scrape_commentary(match_url)

            writer.writerow([f"--- MATCH #{i}: {match_title} ---"])
            # Dump commentary lines
            if lines:
                for line in lines:
                    writer.writerow([line])
            else:
                writer.writerow(["No commentary found or match hasn't started."])
            writer.writerow([])  # blank line after each match

    print(f"Data saved to {filename}")


if __name__ == "__main__":
    schedule_url = "https://www.cricbuzz.com/cricket-series/7607/indian-premier-league-2024/matches"
    stats_url = "https://www.cricbuzz.com/cricket-series/7607/indian-premier-league-2024/stats"

    print("Scraping Schedule & Results ...")
    schedule_data = scrape_schedule(schedule_url)

    print("Scraping Stats (Most Runs & Most Wickets) ...")
    stats_data = scrape_stats(stats_url)

    print("Writing combined data (Schedule, Stats, Commentary) to CSV ...")
    write_to_csv(schedule_data, stats_data, filename="ipl2024_data.csv")
    print("Done.")
