# NEPSE Data Scraper

This NEPSE Data Scraper automates the process of extracting financial data from the Nepal Stock Exchange (NEPSE) website. It performs two key tasks: downloading the latest stock prices (Today's Price) in CSV format and capturing a list of listed securities from the website's network response, also saving it as a CSV file.

The script utilizes Playwright for browser automation and Python's built-in CSV module for handling data exports. The project is designed to be highly configurable, leveraging environment variables to define the NEPSE URL and the local directory where the CSV files are stored. Error handling, logging, and dynamic directory creation are implemented to ensure robustness during execution