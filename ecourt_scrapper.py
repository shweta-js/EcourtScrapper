from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import csv
from datetime import datetime

driver = webdriver.Chrome()
driver.get("https://services.ecourts.gov.in/ecourtindia_v6/?p=cause_list/")

wait = WebDriverWait(driver, 20)  # Increased wait for slow page load

# Helper function to select dropdown reliably
def select_dropdown(by, locator, value):
    dropdown = wait.until(EC.element_to_be_clickable((by, locator)))
    select = Select(dropdown)
    select.select_by_visible_text(value)
    time.sleep(2)  # Wait for dependent dropdown to populate

# Step 1: Select State
select_dropdown(By.ID, "sess_state_code", "Karnataka")
time.sleep(2)
# Step 2: Select District
select_dropdown(By.ID, "sess_dist_code", "BAGALKOT")
time.sleep(2)
# Step 3: Select Court
select_dropdown(By.ID, "court_complex_code", "District Court Complex Bagalkot")
time.sleep(2)
# Step 3a: Handle "Select Establishment" popup
try:
    wait.until(EC.alert_is_present())
    alert = driver.switch_to.alert
    print("Popup text:", alert.text)
    alert.accept()
    print("Popup accepted")
except:
    print("No popup appeared")

time.sleep(2)
select_dropdown(By.ID, "court_est_code", "VACATION COURT,BAGALKOT")
time.sleep(2)

# Close validation modal if present
try:
    close_button = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#validateError .btn-close"))
    )
    close_button.click()
    print("Validation modal closed.")
    wait.until(EC.invisibility_of_element_located((By.ID, "validateError")))
except:
    print("No validation modal to close.")

# Extract judges
judge_dropdown = wait.until(EC.presence_of_element_located((By.ID, "CL_court_no")))
judge_select = Select(judge_dropdown)
judges = [opt.text.strip() for opt in judge_select.options if opt.text.strip() and "Select" not in opt.text]
print(f"Found {len(judges)} judges:")
for j in judges:
    print(j)

# Save judges to CSV
date_str = datetime.now().strftime("%Y-%m-%d")
csv_filename = f"judges_{date_str}.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Judge Name"])
    for j in judges:
        writer.writerow([j])
print(f"Judges list saved to {csv_filename}")

# Loop for all judges
for judge_name in judges:
    print(f"\nProcessing judge: {judge_name}")

    # 1️⃣ Select the judge in the dropdown
    judge_dropdown = wait.until(EC.presence_of_element_located((By.ID, "CL_court_no")))
    judge_select = Select(judge_dropdown)

    # Skip disabled judges
    option_to_select = None
    for opt in judge_select.options:
        if opt.text.strip() == judge_name:
            if not opt.is_enabled():
                print(f"Skipping disabled judge: {judge_name}")
                option_to_select = None
            else:
                option_to_select = opt
            break
    if option_to_select is None:
        time.sleep(2)
        continue

    judge_select.select_by_visible_text(judge_name)
    time.sleep(2)

    # 2️⃣ Enter the hardcoded cause list date
    date_input = driver.find_element(By.ID, "causelist_date")
    date_input.clear()
    date_input.send_keys("18-10-2025")
    time.sleep(2)

    # 3️⃣ Pause for manual CAPTCHA input and clicking Civil
    input(f"Please enter CAPTCHA on the webpage and click Civil for judge '{judge_name}', then press Enter here to continue...")
    time.sleep(2)

    # 4️⃣ Click Civil button
    civil_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Civil')]")
    civil_button.click()
    time.sleep(5)
    print("Civil button clicked successfully!")

    # 5️⃣ Locate the cause list table
    table_element = driver.find_element(By.ID, "dispTable")
    table_html = table_element.get_attribute("outerHTML")

    # 6️⃣ Parse table with BeautifulSoup
    soup = BeautifulSoup(table_html, "html.parser")
    table = soup.find("table")

    rows = table.find_all("tr")
    data = []
    for row in rows:
        cols = row.find_all(["td", "th"])
        cols_text = [c.get_text(strip=True) for c in cols]
        data.append(cols_text)

    # 7️⃣ Save to CSV with judge name in filename
    filename = f"CauseList_{judge_name.replace(' ', '_')}_18-10-2025.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)

    print(f"Cause list for judge '{judge_name}' saved to {filename}")

    time.sleep(2)
