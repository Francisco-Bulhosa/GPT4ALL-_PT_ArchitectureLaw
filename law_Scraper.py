# This annotated code is used if you require a single page scraper.

# # Create the folder if it doesn't exist
# if not os.path.exists('scraped_law'):
#     os.makedirs('scraped_law')



# import bs4
# import re
# from time import sleep
# from selenium import webdriver
# import lxml
# from bs4 import BeautifulSoup


# driver.get(url)
# sleep(8)
# innerHTML = driver.execute_script("return document.body.innerHTML")


# root=bs4.BeautifulSoup(innerHTML,"lxml")

# # Find all elements with the class 'OSInline' which wraps each article
# articles = root.select('.OSInline')

# print(root)
# # Initialize an empty list to hold the combined articles
# combined_articles = []

# # Loop through each article block
# for article in articles:
#     # Extract the title (Artigo n.º)
#     title = article.select_one('.Fragmento_Titulo')
    
#     # Extract the associated text
#     text = article.select_one('.Fragmento_Texto')
    
#     # If both title and text are found, append them to the list
#     if title and text:
#         combined_articles.append(title.get_text(strip=True))
#         combined_articles.append(text.get_text(strip=True))

# # Convert the list to a single string for saving
# combined_text = '\n'.join(combined_articles)

# # Save the combined text to a .txt file
# with open('targeted_output.txt', 'w', encoding='utf-8') as file:
#     file.write(combined_text)


import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
import lxml

class LawScraper:
    def __init__(self, base_url, save_folder='scraped_law'):
        self.base_url = base_url
        self.save_folder = save_folder
        self.driver = self._setup_driver()
        self._ensure_save_folder_exists()

    def _setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        return webdriver.Chrome(options=options)

    def _ensure_save_folder_exists(self):
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)

    def get_links_and_titles(self):

        self.driver.get(self.base_url)
        sleep(8)
        # Logic to extract links and titles from the main page
        # Assuming the links are inside 'a' tags and titles can be extracted as described
        link_elements = self.driver.find_elements(By.CSS_SELECTOR, ".title a")
        links_and_titles = [(link.get_attribute('href'), link.text) for link in link_elements]
        return links_and_titles

    def extract_content_from_link(self, link):
        self.driver.get(link)
        sleep(8)
        innerHTML = self.driver.execute_script("return document.body.innerHTML")
        root = BeautifulSoup(innerHTML, "lxml")
        
        articles = root.select('.OSInline')
        combined_articles = []

        for article in articles:
            title = article.select_one('.Fragmento_Titulo')
            text = article.select_one('.Fragmento_Texto')
            
            if title and text:
                combined_articles.append(title.get_text(strip=True))
                combined_articles.append(text.get_text(strip=True))

        combined_text = '\n'.join(combined_articles)
        return combined_text


    def save_content_to_file(self, content, title):
        # Convert title to a valid filename (remove invalid characters)
        valid_filename = "".join([c for c in title if c.isalpha() or c.isdigit() or c in (' ', '.', '_')]).rstrip()
        filename = os.path.join(self.save_folder, valid_filename + '.txt')
        
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)

    def scrape(self):
        links_and_titles = self.get_links_and_titles()
        for link, title in links_and_titles:
            content = self.extract_content_from_link(link)
            self.save_content_to_file(content, title)

    def close(self):
        self.driver.quit()


if __name__ == '__main__':
    scraper = LawScraper('https://diariodarepublica.pt/dr/legislacao-consolidada-pesquisa/urbanismo')
    scraper.scrape()
    scraper.close()