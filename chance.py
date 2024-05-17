from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import json
import time
 
service = Service(executable_path="chromedriver.exe")
browser = uc.Chrome(service=service)
browser.get("https://www.chance.cz/kurzy/dnes?limit=225")

time.sleep(2)

# Accept cookies
try:
    browser.find_element(By.XPATH, '//*[@id="js-LayersReact"]/div[2]/div/div[3]/button[2]').click()
except: pass

time.sleep(2)

matches = browser.find_elements(By.XPATH, "//div[contains(@data-atid, 'content||MATCH||')]")

matchData = []

for match in matches:

    # Extract match date
    date = match.find_element(By.XPATH, "./div/div[2]/div[2]/div/span[1]")
 
    # Check if the date text contains "dnes" (case-insensitive)
    if "dnes" not in date.get_attribute("textContent").lower():
        continue  # Skip this iteration if "dnes" is not found in the date text

    # Extract match title
    title = match.find_element(By.XPATH, "./div/div[2]/div[1]/span")
    titleText = title.get_attribute("textContent").replace(" ", " ").strip()

    # Extract odds
    oddsElements = match.find_elements(By.XPATH, ".//div[contains(@data-atid, 'content||ODD||')]")
    odds = {}

    for oddsElement in oddsElements:
        try:
            odd = oddsElement.find_element(By.TAG_NAME, "span")           
            oddType = oddsElement.get_attribute("data-atid").split("||")[-1]
            odds[oddType] = odd.get_attribute("textContent")
        except:
            print("Span element not found, skipping this iteration.")
            continue
        
    # Append match data to the list
    matchData.append({
        "title": titleText,
        "date":  date.get_attribute("textContent"),
        "odds": odds
    })

# Create a dictionary with match data
data = {"matches": matchData}

# Write data to a JSON file
with open("chance-matches.json", "w") as jsonFile:
    json.dump(data, jsonFile, indent=4)

browser.quit()
