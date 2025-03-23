import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def parse_points_table(soup):
    """
    Parses the HTML of the IPL points table (plus expansions)
    and returns a list of dictionaries, one row per match.
    Each row includes team summary columns plus Opponent/Result details.
    """
    # Find the main table by class
    main_table = soup.find("table", class_="table cb-srs-pnts")
    if not main_table:
        print("Points table not found in HTML!")
        return []

    tbody = main_table.find("tbody")
    all_rows = tbody.find_all("tr", recursive=False)

    data_rows = []
    i = 0
    while i < len(all_rows):
        row = all_rows[i]

        # 1) Parse the main (team) row
        team_name_td = row.find("td", class_="cb-srs-pnts-name")
        summary_tds = row.find_all("td", class_="cb-srs-pnts-td")

        if not team_name_td or not summary_tds:
            i += 1
            continue

        team_name = team_name_td.get_text(strip=True)

        # Typically 7 summary columns: Mat, Won, Lost, Tied, NR, Pts, NRR
        mat  = summary_tds[0].get_text(strip=True)
        won  = summary_tds[1].get_text(strip=True)
        lost = summary_tds[2].get_text(strip=True)
        tied = summary_tds[3].get_text(strip=True)
        nr   = summary_tds[4].get_text(strip=True)
        pts  = summary_tds[5].get_text(strip=True)
        nrr  = summary_tds[6].get_text(strip=True)

        # 2) The next row often has the sub-table with match details
        i += 1
        if i < len(all_rows):
            detail_row = all_rows[i]
            detail_td = detail_row.find("td", class_="cb-srs-pnts-dwn")
            if detail_td:
                sub_table = detail_td.find("table", class_="table cb-srs-pnts-dwn-tbl")
                if sub_table:
                    sub_tbody = sub_table.find("tbody")
                    sub_rows = sub_tbody.find_all("tr", recursive=False)
                    # sub_rows[0] is the header: Opponent, Description, Date, Result
                    for match_row in sub_rows[1:]:
                        match_cols = match_row.find_all("td")
                        if len(match_cols) == 4:
                            opponent    = match_cols[0].get_text(strip=True)
                            description = match_cols[1].get_text(strip=True)
                            date        = match_cols[2].get_text(strip=True)
                            result      = match_cols[3].get_text(strip=True)

                            data_rows.append({
                                "Team"       : team_name,
                                "Mat"        : mat,
                                "Won"        : won,
                                "Lost"       : lost,
                                "Tied"       : tied,
                                "NR"         : nr,
                                "Points"     : pts,
                                "NRR"        : nrr,
                                "Opponent"   : opponent,
                                "Description": description,
                                "Date"       : date,
                                "Result"     : result
                            })

        i += 1  # Move to the next team row
    return data_rows

def main():
    # ----------------------------------------------------------------
    # 1) Configure Selenium / Chrome
    # ----------------------------------------------------------------
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # optional: run Chrome in background
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver_path = r"C:\WebDrivers\chromedriver.exe"  # Update this!
    service = Service(driver_path)

    driver = webdriver.Chrome(service=service, options=chrome_options)

    # ----------------------------------------------------------------
    # 2) Load the IPL 2020 Points Table page
    # ----------------------------------------------------------------
    url = "https://www.cricbuzz.com/cricket-series/3130/indian-premier-league-2020/points-table"
    driver.get(url)
    time.sleep(3)  # wait for dynamic content

    # Grab HTML
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # ----------------------------------------------------------------
    # 3) Parse the points table
    # ----------------------------------------------------------------
    parsed_data = parse_points_table(soup)
    if not parsed_data:
        print("No data found or table structure not recognized.")
        return

    # ----------------------------------------------------------------
    # 4) Write data to CSV
    # ----------------------------------------------------------------
    csv_filename = "ipl2020_points_table_details.csv"
    fieldnames = [
        "Team", "Mat", "Won", "Lost", "Tied", "NR",
        "Points", "NRR", "Opponent", "Description", "Date", "Result"
    ]
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in parsed_data:
            writer.writerow(row)

    print(f"Scraping complete. Data saved to {csv_filename}")

if __name__ == "__main__":
    main()
