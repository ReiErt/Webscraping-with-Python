# Webscraping-with-Python

This repository is for a university project "data science with Python": 

# Task

In this project, you need to create a user-friendly software that stores and extracts information about the top 50 popular Hollywood actor and actresses http://www.imdb.com/list/ls053501318/.
Your IMDB software should provide following functionality:
1. List of all available actors and actresses
2. About the actor/actresses
3. All time movie names and years
4. Awards to actor/actresses in different years
5. Movie genre of actor/actresses
6. Average rating of their movies (overall and each year)
7. Top 5 movies, their respective years and genre

Please remember, your software needs to be user-friendly and well-formatted.

# The nature of HTML Tags on front end:

IMDB is constantly changing the layout of its HTML page, including its HTML tags. Therefore, the webscraping_mine file will likely not be able to scrape.

# How to run:

1. call py setup.py to scrape data  # static DB file is created. This script takes 30 minutes to run. Information on why in demonstration.pdf 
2. call py terminal_program.py      # opens a run-time program in terminal

# Dependencies

1. python 3.12.0
2. sqlite3
3. BeautifulSoup4 4.4.1
4. SQL
5. requests from python
6. time from python
7. bs4 from beautifulsoup
