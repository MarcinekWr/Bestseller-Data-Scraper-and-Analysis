from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
import numpy as np
import re
from bs4 import BeautifulSoup
import requests
import time
import datetime
import sqlalchemy as sa

##SCRAPER WSYZSTKICH PODSTAWOWYCH KATEGORI Z LINKA https://www.amazon.pl/gp/bestsellers/ref=zg_bs_tab_bs
def SCRAPER(URL):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service,options=options)

    driver.get(URL)
    page_source = driver.page_source
    time.sleep(5)

    driver.quit()

    soup = BeautifulSoup(page_source, 'html.parser')

    return soup

def cathegory():
    soup = SCRAPER("https://www.amazon.pl/gp/bestsellers/ref=zg_bs_tab_bs") ##GŁOWNA STRONA AMAZONA BESTSELLERS

    divs = soup.find_all('div',class_='_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf _p13n-zg-nav-tree-all_style_zg-browse-height-small__nleKL')

    links = []
    for div in divs:
        data = div.find('a')
        name = data.text.strip()
        link = 'https://www.amazon.pl/' + data['href']
        links.append([name, link])

    #MOJE DODATKI
    additional_url =[
        ['Tablety','https://www.amazon.pl/gp/bestsellers/electronics/20788300031/ref=zg_bs_nav_electronics_1'],
        ['Laptotpy','https://www.amazon.pl/gp/bestsellers/electronics/20788292031/ref=zg_bs_nav_electronics_2_20788300031'],
        ['Telefony komórkowe','https://www.amazon.pl/gp/bestsellers/electronics/20788267031/ref=zg_bs_nav_electronics_2_20788252031'],
        ['Podzespoły i części komputerowe','https://www.amazon.pl/gp/bestsellers/electronics/20788298031/ref=zg_bs_nav_electronics_2_20788256031']
    ]

    links = links + additional_url

    return links
