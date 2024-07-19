from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time


def SCRAPER(URL):
    # configuration webpage without graphical interface
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    # Initialize chrome browser
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Open URL
    driver.get(URL)

    time.sleep(5)

    # Get the page source
    page_source = driver.page_source

    # Close browser
    driver.quit()

    # Processing source using BeautyfulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    return soup


def cathegory():
    # Get the main Amazon Bestsellers page using the SCRAPER function
    soup = SCRAPER("https://www.amazon.pl/gp/bestsellers/ref=zg_bs_tab_bs")

    # Find all divs containing category links
    divs = soup.find_all('div',
                         class_='_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf _p13n-zg-nav-tree-all_style_zg-browse-height-small__nleKL')

    links = []

    # Loop through each div to extract the category name and link
    for div in divs:
        data = div.find('a')
        name = data.text.strip()  # category name
        link = 'https://www.amazon.pl/' + data['href']  # link
        links.append([name, link])

    # My few additional links
    additional_url = [
        ['Tablety', 'https://www.amazon.pl/gp/bestsellers/electronics/20788300031/ref=zg_bs_nav_electronics_1'],
        ['Laptotpy',
         'https://www.amazon.pl/gp/bestsellers/electronics/20788292031/ref=zg_bs_nav_electronics_2_20788300031'],
        ['Telefony komórkowe',
         'https://www.amazon.pl/gp/bestsellers/electronics/20788267031/ref=zg_bs_nav_electronics_2_20788252031'],
        ['Podzespoły i części komputerowe',
         'https://www.amazon.pl/gp/bestsellers/electronics/20788298031/ref=zg_bs_nav_electronics_2_20788256031']
    ]

    # Append the additional URLs to the links list
    links = links + additional_url

    # Return the complete list of category names and links
    return links
