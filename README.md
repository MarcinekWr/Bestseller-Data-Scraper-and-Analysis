# Amazon Bestseller Data Scraper

I've decided experimentally to open my own online store. To reach a wide audience and increase my store's effectiveness, I plan to align with current popular trends and offer the best-selling products at competitive prices. To achieve this, I aim to create a Python script that will daily scrape the top bestsellers from various categories, store this data, and generate a simple report. This report will help me identify the most popular products with the highest sales potential for the given period.

## Plan of this project: 
![Bez tytułu](https://github.com/user-attachments/assets/0902169d-8be4-4201-8c42-2ac023b00573)

## What i gained from this project?

Firstly, I have learned web scraping techniques using popular Python libraries like BeautifulSoup and Selenium. I now understand how to navigate and extract data from HTML documents, and how to handle websites with dynamically rendered content using tools like Selenium. I have also gained experience in data cleaning and preparation by using Pandas and NumPy. I have learned how to connect Python with databases such as PostgreSQL. Through libraries such as SQLAlchemy. I have mastered database management and SQL queries within Python. This includes creating and managing database schemas, inserting, updating, and querying data using SQL commands. Lastly, I have developed proficiency in Power BI, enabling me to create dynamic visualizations and reports. I can effectively filter data and use DAX to create new, valuable columns. This skill set allows me to present data insights clearly and interactively, making data more accessible and understandable. 

## Code
In the code, I made sure to add comments so that everything is clear.
## Future steps

* Currently, I'm waiting to scrape one month of data to do a more complex analysis.
* The next idea is to add a price tracker feature. Users can input a target price, and since prices are quite dynamic and can change seasonally, the system will inform them via email when the price drops below or exceeds their desired price.
* To make this more user-friendly, I can create a web interface using Flask where users can select the products they want to track and generate reports. Additionally, this interface could allow users to set their desired price thresholds for notifications and view the latest price trends and analysis.


## Raport in Power BI


## Quick 

After successfully installing libraries, we run a data_scraper.py code but we need to make sure that we change variable path = '' to a location where files should be saved and file the database connection parameters

Database parameters

![database](https://github.com/user-attachments/assets/eef22a15-3752-4f5f-a590-c35b02ea6649)  

Path

![3](https://github.com/user-attachments/assets/7a992a37-f36f-4350-8885-eda573c18e37)

When we run a script the command window if everything went successfully should look like this

![run](https://github.com/user-attachments/assets/e08b216b-b8d8-440b-bc75-b91a084086c9)


