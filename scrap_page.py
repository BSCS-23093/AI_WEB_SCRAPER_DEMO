import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

def scrape_webpage(url):
    print("Scraping webpage content")
    chrome_driver_path = "./chromedriver.exe"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(url)
        print("WebPage loaded...")
        html = driver.page_source
        time.sleep(10)
        return html
    finally:
        driver.quit()
        print("Driver closed...")

def extract_body(html):
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find('body')
    if body:
        return str(body)
    return "None"

def cleanze_body(body):
    soup = BeautifulSoup(body, 'html.parser')
    # for script in soup(["script", "style"]):
    #     script.extract()
    cleaned = soup.get_text(separator='\n')
    cleaned = "\n".join([line.strip() for line in cleaned.split("\n") if line.strip()])
    return cleaned

def split_dom_content(dom_content,max_length=6000):
    return [dom_content[i:i+max_length] for i in range(0, len(dom_content), max_length)]