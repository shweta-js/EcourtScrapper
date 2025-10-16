# eCourts Cause List Scraper

A Python-based web scraper to extract **cause lists for judges** from the [eCourts portal](https://services.ecourts.gov.in/ecourtindia_v6/?p=cause_list/).  
The scraper automates browser actions using **Selenium**, parses HTML tables with **BeautifulSoup**, and saves the extracted data as **CSV files**.

---

## Features

- Extracts the list of judges for a selected court complex.
- Allows you to specify a **cause list date**.
- Saves each judge’s cause list in a separate CSV file.
- Handles popups automatically (e.g., “Select Establishment” validation modal).
- Skips **disabled judges** automatically.
- Supports **manual CAPTCHA entry** to comply with website security.
- Efficiently iterates over all judges in the dropdown.

---

## Inputs Required

Before running the scraper, the following inputs must be provided:

- **State** (e.g., `"Karnataka"`)
- **District** (e.g., `"BAGALKOT"`)
- **Court Complex** (e.g., `"District Court Complex Bagalkot"`)
- **Court Establishment** (e.g., `"VACATION COURT,BAGALKOT"`)
- **Cause List Date** (e.g., `"18-10-2025"`)

---

## How to Run

1. Open the script `ecourt_scrapper.py`.
2. Update the predefined inputs (State, District, Court Complex, Court Establishment, and Date) if required.
3. Run the script:

   ```bash
   python ecourt_scrapper.py

The script will pause for manual CAPTCHA entry.

Enter the CAPTCHA displayed on the website.

Click the Civil button.

Press Enter in the console to continue.

Cause lists will be saved in the same directory:

judges_<YYYY-MM-DD>.csv → List of judges.

CauseList_<Judge_Name>_<Date>.csv → Cause list for each judge.

## Limitations

Civil Button Only:

- Currently, only the Civil section is scraped.
- The Criminal section is not implemented, but can be added with a similar workflow.

Manual CAPTCHA Entry:

- CAPTCHAs cannot be automated for legal and ethical reasons.
- Each judge requires a new manual CAPTCHA input before fetching the cause list.

Hardcoded Inputs:

- State, District, Court Complex, Court Establishment, and Date are hardcoded.
- To scrape different courts or dates, the script must be updated manually.

Validation Popups:

- Validation modals are automatically closed by the script. Unexpected popups may require manual intervention.

Disabled Judges:
- Disabled judges in the dropdown are skipped automatically.

Dynamic Website Changes:
- If the eCourts portal changes its layout or element IDs, the scraper may fail and require    updates.

Output

- judges_<YYYY-MM-DD>.csv → List of all judges for the selected court complex.

- CauseList_<Judge_Name>_<Date>.csv → Cause list for each judge individually.

Notes

- time.sleep(2) is intentionally kept between steps to allow users to visually track progress.
- Ensure ChromeDriver matches the Chrome browser version installed on your system.
- Manual CAPTCHA entry is mandatory to comply with website rules.

License

- This project is for educational and academic purposes only. Do not use this script to violate website terms of service.
 

