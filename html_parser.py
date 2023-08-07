from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os

# Create the folder if it doesn't exist
if not os.path.exists('scraped_law'):
    os.makedirs('scraped_law')

# URL to scrape
url = 'https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-lei/1951-120610500'

import bs4
import re
from time import sleep
from selenium import webdriver
import lxml
from bs4 import BeautifulSoup

driver = webdriver.PhantomJS()

driver.get(url)
sleep(8)
innerHTML = driver.execute_script("return document.body.innerHTML")

root=bs4.BeautifulSoup(innerHTML,"lxml")

soup = BeautifulSoup(str(root), 'html.parser')

print(root)



https://diariodarepublica.pt/dr/legislacao-consolidada-pesquisa/urbanism



text_file = open("sample.txt", "w")
n = text_file.write(str(soup))
text_file.close()




















# Open the browser and navigate to the page
driver = webdriver.Chrome()
driver.get(url)

# Wait for the first "Artigo n.º" element to be present
wait = WebDriverWait(driver, 8) # 8 seconds timeout
wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "Fragmento_Titulo")]/span')))

# Locate the elements containing "Artigo n.º" and law text
artigos_elements = driver.find_elements_by_xpath('//div[contains(@class, "Fragmento_Titulo")]/span')
text_elements = driver.find_elements_by_xpath('//div[contains(@class, "Fragmento_Texto")]/div/div/div')

# Define the path where the CSV file will be saved
path_to_save = 'scraped_law/law_document.csv'

# Check if the lengths match
if len(artigos_elements) != len(text_elements):
    print("Mismatch in number of articles and texts.")
else:
    # Open a CSV file for writing
    with open(path_to_save, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Artigo", "Text"])  # Write the header
        # Iterate through the elements and write to CSV
        for artigo, text in zip(artigos_elements, text_elements):
            writer.writerow([artigo.text, text.text])
    print(f"Scraping completed and content saved to {path_to_save}.")

# Close the browser
driver.close()



