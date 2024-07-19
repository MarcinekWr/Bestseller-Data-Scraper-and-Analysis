import sys
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
from tqdm import tqdm


def SCRAPER_2(URL):
    # Configure webpage, without graphic interface, it will work in the background
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    # Initialize Chrome browser
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Open URL
    driver.get(URL)
    # driver.set_window_size(1500, 800)
    time.sleep(5)

    # Clicking the accept button for the cookie
    cookie_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, 'sp-cc-accept'))
    )
    cookie_button.click()

    # This simulates the scrolling process because the webpage does not load the whole HTML code at once.
    # We need to simulate scrolling to get the entire source code.

    # Scroll down to 80% of the page height
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.80);")
    time.sleep(5) # Wait for the content to load

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.80);")
    time.sleep(5)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.80);")
    time.sleep(5)

    # Get the source
    page_source = driver.page_source
    time.sleep(5)

    # CLose webpage
    driver.quit()

    # Processing source using BeautyfulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    return soup


def save_webpage(URL, path):
    # Getting the HTML code from a URL
    soup = SCRAPER_2(URL)

    # Finding all divs with this specified class
    divs = soup.find_all('div', class_='a-column a-span12 a-text-center _cDEzb_grid-column_2hIsc')
    # Finding h1 element with this specified class
    whole_title = soup.find('h1', class_='a-size-large a-spacing-medium a-text-bold')
    # Get the text content, strip it and replace worlds if not found set whole_title to none
    whole_title = whole_title.get_text(strip=True).replace('Bestsellery w ', '') if whole_title else 'None'

    # Empty list to store the scraped data
    titles = []
    prices = []
    ratings = []
    img = []
    links = []
    day = []
    avg_ratio = []
    kategory = []

    # Iterate through each div in the list of divs
    for div in divs:

        # Extracting the title from the alt attribute of the image
        title = div.find('img', class_='a-dynamic-image p13n-sc-dynamic-image p13n-product-image')
        title = title['alt'] if title else np.nan

        # Extracting price from the span tag
        span_outer = div.find('span', class_='a-size-base a-color-price')
        if span_outer:
            span_inner = span_outer.find('span')
            price = span_inner.text.strip()
        else:
            price = np.nan

        # Extract the rating if available
        icon_row_div = div.find('div', class_='a-icon-row')
        if icon_row_div:
            rating_span = icon_row_div.find('span', class_='a-size-small')
            if rating_span:
                rating = rating_span.text.strip()
            else:
                rating = np.nan
        else:
            rating = np.nan

        # Extract the average rating
        avg_rating = div.find('span', class_='a-icon-alt')
        if avg_rating:
            avg_rating = avg_rating.get_text(strip=True)
            avg_rating = re.sub(r'[^\d\.]', '', avg_rating)
        else:
            avg_rating = np.nan

        # Extract the image link
        img_tag = div.find('img', class_='a-dynamic-image p13n-sc-dynamic-image p13n-product-image')
        link = img_tag['src'] if img_tag else 'Brak linku'

        # Extract the product link
        link_phone = div.find('a', class_='a-link-normal aok-block')
        new_link = link_phone['href'] if link_phone else 'Brak linku'
        new_link = 'https://www.amazon.pl' + new_link

        # Get today's date
        today = datetime.date.today()

        # Append the extracted data to the respective lists
        titles.append(title)
        prices.append(price)
        ratings.append(rating)
        img.append(link)
        links.append(new_link)
        day.append(today)
        avg_ratio.append(avg_rating)
        kategory.append(whole_title)

    # Create a DataFrame from the collected data
    data = pd.DataFrame({
        'title': titles,
        'price': prices,
        'ratings': ratings,
        'mean_rating': avg_ratio,
        'date': day,
        'category': kategory,
        'img': img,
        'link': links,

    })

    data['ratings'] = data['ratings'].apply(lambda x: x.strip() if isinstance(x, str) else x)
    today = str(datetime.date.today())

    # Define the path for the Excel file
    whole_title = whole_title.replace(' ', '_')
    excel_path = os.path.join(today, whole_title + '_' + today + '.xlsx')
    excel_path = os.path.join(path, excel_path)

    # Save the DataFrame to an Excel file
    data.to_excel(excel_path, index=False)



def clearing_data(path):
    df = pd.read_excel(path)

    # Additiona cleanig of the data
    df['price'] = df['price'].astype('str')
    df['price'] = df['price'].str.replace('zł', '').str.replace('\u00A0', '').str.replace(',', '.')
    df['price'] = df['price'].astype('float')
    df['ratings'] = df['ratings'].astype('str')
    df['ratings'] = df['ratings'].str.replace('\u00A0', '')
    df['ratings'] = df['ratings'].astype('float')

    return df


# Path where the excel files gonna be saved
path = r'C:\Users\suzum\PycharmProjects\pythonProject15\Web_scraping\Amazon_scraping\Scraping_webpage'
today = str(datetime.date.today())
today_import = os.path.join(path, today)
print(fr"Data scraping amazon bestsellers {today}")
# Call the function to get the category URLs
urls = cathegory()

print("Scraping data and saving each category to the excel file.")

# Check if today's directory already exists
if not os.path.exists(today_import):
    os.mkdir(today_import)
else:
    print("Error! Today scraping was already done " + today + " file already exists")
    sys.exit(0) # Exit the script if the directory already exists

# Iterate over each URL and save the webpage data
for url in tqdm(urls):
    save_webpage(url[1],path)

print("Done saving scraped data to excel files.\n")

print("Connecting to database...", flush=True)

# Database connection parameters
dbname = 'postgres'
user = 'postgres'
password = ''
host = 'localhost'

# Create a SQLAlchemy engine for connecting to the PostgreSQL database
engine = sa.create_engine(f'postgresql://{user}:{password}@{host}/{dbname}')

try:
    conn = engine.connect()
    print("Successfully connected to database.\n")
    conn.close()
except Exception as e:
    print(f'Error: {e}\n')

# List to store paths of Excel files
paths = []

# Walk through the directory and collect paths of Excel files
for dirpath, dirnames, filenames in os.walk(today_import):
    for filename in filenames:
        if filename.endswith('.xlsx'):
            path_excel = os.path.join(dirpath, filename)
            paths.append(path_excel)

print("Data cleaning and saving to database.")
# Iterate over each Excel file path
for i in tqdm(paths):
    # Clean the data using the clearing_data function
    df = clearing_data(i)

    # Define the table name
    table_name = 'bestsellers'

    # Save the DataFrame to the SQL table in the database
    df.to_sql(table_name, engine, schema='project', if_exists='append', index=False)

print("Data cleaning complete and files are stored in database.")
