
 
# impor bs4
# import re
# from time import sleep
# from selenium import webdriver
# import lxml
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from time import sleep
# from selenium.common.exceptions import TimeoutException


# url = 'https://oasrs.org/o-que-faz/apoio-tecnico/24/'

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--ignore-certificate-errors')
# driver = webdriver.Chrome(options=options)

# driver.get(url)

# try:
#     # Wait for the buttons to be present
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h2.accordion__toggle"))
#     )

#     # Find all the buttons and click on each one
#     buttons = driver.find_elements(By.CSS_SELECTOR, "h2.accordion__toggle")
#     for button in buttons:
#         try:
#             button.click()
#             sleep(1)  # Wait for potential animations or content loading
#         except:
#             print("Couldn't click on one of the buttons. Skipping and continuing.")

#     # Wait a bit after clicking all buttons to let all content load
#     sleep(5)

#     # Extract PDF links
#     pdf_link_elements = driver.find_elements(By.CSS_SELECTOR, "a[href$='.pdf']")
#     pdf_links = [link.get_attribute('href') for link in pdf_link_elements]

#     # Create an indexed list of PDF links
#     indexed_links = [(index, link) for index, link in enumerate(pdf_links, 1)]

#     print(indexed_links)



# except TimeoutException:
#     print("Could not find the buttons in time. Either increase the wait time or check the page structure.")

# driver.quit()


#This scraper works for a specific case to retrieve pdf files that require loading upon user interaction, but it can be tweaked for other websites.

import os
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class PDFScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.driver = self._init_webdriver()

    def _init_webdriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors')
        return webdriver.Chrome(options=options)

    def get_pdf_links(self):
        self.driver.get(self.base_url)
        
        try:
            # Wait for the buttons to be present
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h2.accordion__toggle"))
            )
            
            # Click on each button
            buttons = self.driver.find_elements(By.CSS_SELECTOR, "h2.accordion__toggle")
            for button in buttons:
                try:
                    button.click()
                    sleep(1)  # Wait for potential animations or content loading
                except:
                    print("Couldn't click on one of the buttons. Skipping and continuing.")

            # Wait after clicking all buttons to allow content to load
            sleep(5)
            
            # Extract PDF links
            pdf_link_elements = self.driver.find_elements(By.CSS_SELECTOR, "a[href$='.pdf']")
            pdf_links = [link.get_attribute('href') for link in pdf_link_elements]
            
            return pdf_links
        
        except TimeoutException:
            print("Could not find the buttons in time. Either increase the wait time or check the page structure.")
            return []

    def scrape(self):
        pdf_links = self.get_pdf_links()
        indexed_links = [(index, link) for index, link in enumerate(pdf_links, 1)]
        return indexed_links

    def close(self):
        self.driver.quit()

# Usage
# if __name__ == "__main__":
#     scraper = PDFScraper('https://oasrs.org/o-que-faz/apoio-tecnico/24/')
#     indexed_links = scraper.scrape()
#     print(indexed_links)
#     scraper.close()

