from bs4 import BeautifulSoup
import time, re, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Suppress Selenium and ChromeDriver logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import logging
logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(logging.WARNING)


url = "https://yepsavings.com/ca-ab-calgary-nw-beacon-hill-25"
search_query = input("Enter the item name to search for: ").strip().lower()

#Headless Chrome and supress silly ssl warnings
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--enable-unsafe-swiftshader")

driver = webdriver.Chrome(options=options)
driver.get(url)

# Scroll to load more content until no new images load
SCROLL_PAUSE_TIME = 2
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Wait explicitly for images to be present
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, "img"))
)
time.sleep(2)  

# Process the loaded page
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')
images = soup.find_all("img", alt=True)

found = False
for img in images:
    alt_text = img["alt"]
    if search_query in alt_text.lower():
        match = re.search(r'ITM\s*(\d+)', alt_text, re.I)
        if match:
            item_number = match.group(1)
            print(f"Found listing for '{alt_text}' with Item Number: {item_number}")
        else:
            print(f"Listing for '{alt_text}' found, but item number was not detected.")
        found = True

if not found:
    print("No listing matching that item name was found.")

driver.quit()
