import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

# Suppress TensorFlow logging (if any)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

email = "maxwell.souchereau@edu.sait.ca"
password = "Password Here"

options = Options()
options.add_argument("--headless")

#Suppress Logging messages for cleaner terminal 
options.add_argument("--log-level=3")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

# Navigate to the login page
driver.get("https://catalogit.app/login/credentials")
time.sleep(2)

# Locate email and password fields
wait = WebDriverWait(driver, 20)
email_field = wait.until(EC.presence_of_element_located((By.ID, "emailField")))
password_field = wait.until(EC.presence_of_element_located((By.ID, "passwordField")))

# Enter credentials and submit
email_field.send_keys(email)
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)
time.sleep(3)

# List of URLs to scrape titles from
urls = [
    "https://catalogit.app/collections/d8ad2d30-d37f-11ef-942e-a9ab53bb22fc/entries/8460b230-d387-11ef-970e-0dcfb0428747",
    "https://catalogit.app/collections/d8ad2d30-d37f-11ef-942e-a9ab53bb22fc/entries/4d18cef0-d384-11ef-970e-0dcfb0428747",
    "https://catalogit.app/collections/d8ad2d30-d37f-11ef-942e-a9ab53bb22fc/entries/8eac5160-d38a-11ef-970e-0dcfb0428747"
]

for url in urls:
    driver.get(url)
    time.sleep(2)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find title and print it
    title_elements = soup.find_all("div", class_="title")
    titles = [el.get_text(strip=True) for el in title_elements]
    print(f"Titles: {titles}")

driver.quit()

