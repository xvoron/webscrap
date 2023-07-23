# Web Scrap sreality.cz


# Task
1. Scrap first 500 offers from https://www.sreality.cz in categories __flat__ and __sell__.
2. Save the data to PostgreSQL database.
3. Create a simple web page with a table of scrapped data.
4. Wrap the whole project into docker compose.

# Overview

There are three main containers in the project:
1. __scrapper__ - container for scrapping data from sreality.cz. Utilize
   __scrapy__ framework.
2. __db__ - container for PostgreSQL database.
3. __web__ - container for web page with table of scrapped data. Utilize
   __flask__ framework.

# Installation & Usage

Make sure you have installed **docker** and **docker-compose**.

1. Clone the repository.
2. Run `docker-compose up` in the root of the repository.
3. Open http://localhost:8080 in your browser.
4. Enjoy the table with scrapped data :)

