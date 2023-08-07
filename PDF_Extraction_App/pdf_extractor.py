
import os
import requests
import PyPDF2
from io import BytesIO
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
from law_scraper_pdf import PDFScraper  # Assumes the previous script is named 'law_scraper_pdf.py'

def extract_title_from_pdf(pdf_path):
    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                text = element.get_text().strip()
                if text:
                    first_char = next(element.iter_contents(), None)
                    if first_char:
                        font_size = first_char.size
                        font_name = first_char.fontname
                        if font_size > 10.5 and "Bold" in font_name:
                            return text
    return None

def download_and_extract_pdf_text(url, output_dir):
    response = requests.get(url)
    with BytesIO(response.content) as open_pdf_file:
        # Save the PDF temporarily
        temp_pdf_path = os.path.join(output_dir, "temp.pdf")
        with open(temp_pdf_path, "wb") as temp_pdf:
            temp_pdf.write(open_pdf_file.read())
        
        # Extract the title
        title = extract_title_from_pdf(temp_pdf_path)
        if title:
            filename = os.path.join(output_dir, f"{title}.txt")
        else:
            filename = os.path.join(output_dir, "document.txt")

        # Now, extract text using PyPDF2
        reader = PyPDF2.PdfFileReader(open_pdf_file)
        text = ""
        for page_num in range(reader.numPages):
            text += reader.getPage(page_num).extractText()
        
        with open(filename, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)
        
        # Delete the temporary PDF
        os.remove(temp_pdf_path)

if __name__ == "__main__":
    # Initialize PDFScraper
    scraper = PDFScraper('https://oasrs.org/o-que-faz/apoio-tecnico/24/')
    pdf_links = scraper.scrape()
    scraper.close()

    # Create directory for scraped content
    output_dir = 'scraped_pdf_law'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Download, extract text, and save each PDF
    for index, (_, link) in enumerate(pdf_links):
        print(f"Processing PDF {index + 1}/{len(pdf_links)}...")
        download_and_extract_pdf_text(link, output_dir)

    print("All PDFs processed!")
