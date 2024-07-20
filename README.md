# Amazon Bestseller Data Scraper

I've decided experimentally to open my own online store. To reach a wide audience and increase my store's effectiveness, I plan to align with current popular trends and offer the best-selling products at competitive prices. To achieve this, I aim to create a Python script that will daily scrape the top bestsellers from various categories, store this data, and generate a simple report. This report will help me identify the most popular products with the highest sales potential for the given period.

## Plan of this project: 
![Bez tytułu](https://github.com/user-attachments/assets/0902169d-8be4-4201-8c42-2ac023b00573)

## What i gained from this project?

Firstly, I have learned web scraping techniques using popular Python libraries like BeautifulSoup and Selenium. I now understand how to navigate and extract data from HTML documents, and how to handle websites with dynamically rendered content using tools like Selenium. I have also gained experience in data cleaning and preparation by using Pandas and NumPy. I have learned how to connect Python with databases such as PostgreSQL. Through libraries such as SQLAlchemy. I have mastered database management and SQL queries within Python. This includes creating and managing database schemas, inserting, updating, and querying data using SQL commands. Lastly, I have developed proficiency in Power BI, enabling me to create dynamic visualizations and reports. I can effectively filter data and use DAX to create new, valuable columns. This skill set allows me to present data insights clearly and interactively, making data more accessible and understandable. 

## Code
In the code, I made sure to add comments so that everything is clear.

## Quick overview 

After successfully installing the libraries, we need to run the data_scraper.py code. However, make sure to change the variable path = '' to the location where the files should be saved, and fill in the database connection parameters. Note that it only works on the Polish Amazon website because the cleaning and filtering is specified to this language. However, with a few changes, it can also work for different regions websites.

Database parameters

![database](https://github.com/user-attachments/assets/eef22a15-3752-4f5f-a590-c35b02ea6649)  

Path

![3](https://github.com/user-attachments/assets/7a992a37-f36f-4350-8885-eda573c18e37)

When we run the script, the command window should look like this. I used the tqdm function, which shows the progress and estimated time to complete the scraping process.

![run](https://github.com/user-attachments/assets/e08b216b-b8d8-440b-bc75-b91a084086c9)

When the code finishes, we should have new daily scraped data in our database. Now we can take a look at the automatically generated report with Power BI.

## Raport in Power BI

I created the main page where we can see the popularity of each category, measured by the ratings of the category's products. As a second measure, I used the "measure of earnings," which is calculated as ratings multiplied by price. Since we cannot see how many products are sold on Amazon. We can filter this data by each day or a range of days to see which category is the bestseller.

We can dynamically click on each column of the chart to see more detailed information.
![image](https://github.com/user-attachments/assets/0e09bc3c-4287-44b6-b4f0-2e21aebe73ed)

On the second page, we can choose the product category we are interested in, such as Video Games, which is one of the most popular categories. We can then view 50 products with more detailed information. For example, the Nintendo Switch console.

![image](https://github.com/user-attachments/assets/b6ca50e4-6377-41d6-a06f-9cf568ff3fbc)


## Future steps

* Currently, I'm waiting to scrape one month of data to do a more complex analysis.
* The next idea is to add a price tracker feature. Users can input a target price, and since prices are quite dynamic and can change seasonally, the system will inform them via email when the price drops below or exceeds their desired price.
* To make this more user-friendly, I can create a web interface using Flask where users can select the products they want to track and generate reports. Additionally, this interface could allow users to set their desired price thresholds for notifications and view the latest price trends and analysis.



