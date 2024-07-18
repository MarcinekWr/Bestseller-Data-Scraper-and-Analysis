from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import numpy as np
import re
from bs4 import BeautifulSoup
import time
import datetime
import sqlalchemy as sa
from scraper_category import cathegory, SCRAPER


def SCRAPER_2(URL):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(URL)
    driver.set_window_size(1500, 800)
    time.sleep(5)

    cookie_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, 'sp-cc-accept'))
    )
    cookie_button.click()

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.80);")
    time.sleep(5)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.80);")
    time.sleep(5)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.80);")
    time.sleep(5)

    page_source = driver.page_source
    time.sleep(5)

    driver.quit()

    soup = BeautifulSoup(page_source, 'html.parser')

    return soup

def save_webpage(URL):
    soup = SCRAPER_2(URL)

    divs = soup.find_all('div', class_='a-column a-span12 a-text-center _cDEzb_grid-column_2hIsc')
    whole_title = soup.find('h1', class_='a-size-large a-spacing-medium a-text-bold')
    whole_title = whole_title.get_text(strip=True).replace('Bestsellery w ', '') if whole_title else 'None'
    print(whole_title)

    titles = []
    prices = []
    ratings = []
    img = []
    links = []
    day = []
    avg_ratio = []
    kategory = []

    for div in divs:

        title = div.find('img', class_='a-dynamic-image p13n-sc-dynamic-image p13n-product-image')
        title = title['alt'] if title else 'Brak'

        span_outer = div.find('span', class_='a-size-base a-color-price')
        if span_outer:
            span_inner = span_outer.find('span')
            price = span_inner.text.strip()
        else:
            price = np.nan

        icon_row_div = div.find('div', class_='a-icon-row')
        if icon_row_div:
            rating_span = icon_row_div.find('span', class_='a-size-small')
            if rating_span:
                rating = rating_span.text.strip()
            else:
                rating = np.nan
        else:
            rating = np.nan

        avg_rating = div.find('span', class_='a-icon-alt')
        if avg_rating:
            avg_rating = avg_rating.get_text(strip=True)
            avg_rating = re.sub(r'[^\d\.]', '', avg_rating)
        else:
            avg_rating = np.nan

        img_tag = div.find('img', class_='a-dynamic-image p13n-sc-dynamic-image p13n-product-image')
        link = img_tag['src'] if img_tag else 'Brak linku'

        link_phone = div.find('a', class_='a-link-normal aok-block')
        new_link = link_phone['href'] if link_phone else 'Brak linku'
        new_link = 'https://www.amazon.pl' + new_link

        today = datetime.date.today()

        titles.append(title)
        prices.append(price)
        ratings.append(rating)
        img.append(link)
        links.append(new_link)
        day.append(today)
        avg_ratio.append(avg_rating)
        kategory.append(whole_title)

    data = pd.DataFrame({
        'Tytuł': titles,
        'Cena': prices,
        'Oceny': ratings,
        'srednia': avg_ratio,
        'Dzien': day,
        'Kategoria': kategory,
        'Img': img,
        'Link': links,

    })

    data['Oceny'] = data['Oceny'].apply(lambda x: x.strip() if isinstance(x, str) else x)
    data['srednia'] = data['srednia']
    today = str(datetime.date.today())

    if not os.path.exists(today):
        os.mkdir(today)

    # json_path = os.path.join(today, whole_title + '_' + today + '.json')
    excel_path = os.path.join(today, whole_title + '_' + today + '.xlsx')

    # data.to_json(json_path, orient='records', force_ascii=False, indent=8)
    data.to_excel(excel_path, index=False)

urls = cathegory()

for url in urls:
    save_webpage(url[1])


###IMPORT DANYCH DO BAZY DANYCH
def clearing_data(path):
    df = pd.read_excel(path)

    df['Cena'] = df['Cena'].astype('str')
    df['Cena'] = df['Cena'].str.replace('zł', '').str.replace('\u00A0', '').str.replace(',', '.')
    df['Cena'] = df['Cena'].astype('float')
    df['Oceny'] = df['Oceny'].astype('str')
    df['Oceny'] = df['Oceny'].str.replace('\u00A0', '')
    df['Oceny'] = df['Oceny'].astype('float')

    df = df.rename(columns={
        'Tytuł': 'title',
        'Cena': 'price',
        'Oceny': 'ratings',
        'srednia': 'mean_rating',
        'Dzien': 'date',
        'Kategoria': 'category',
        'Img': 'img',
        'Link': 'link'
    })
    return df


dbname = 'postgres'
user = 'postgres'
password = ''
host = 'localhost'

engine = sa.create_engine(f'postgresql://{user}:{password}@{host}/{dbname}')

try:
    conn = engine.connect()
    print("Connected")
    conn.close()
except Exception as e:
    print(f'Error: {e}')

path = r'C:\Users\suzum\PycharmProjects\pythonProject15\Web_scraping\Amazon_scraping\Scraping_webpage'
today = str(datetime.date.today())
today_import = os.path.join(path, today)
paths = []

for dirpath, dirnames, filenames in os.walk(today_import):
    for filename in filenames:
        if filename.endswith('.xlsx'):
            path_excel = os.path.join(dirpath, filename)
            paths.append(path_excel)

for i in paths:
    df = clearing_data(i)
    table_name = 'bestsellers'
    df.to_sql(table_name, engine, schema='project', if_exists='append', index=False)
