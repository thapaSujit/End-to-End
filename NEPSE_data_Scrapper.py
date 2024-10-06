import asyncio
import os
import csv
import logging
from dotenv import load_dotenv
from playwright.async_api import async_playwright

# Load environment variables from .env file
load_dotenv()

# Get environment variables
NEPSE_URL = os.getenv("NEPSE_URL")
DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", "/home/sujit/Desktop/Project Mega-Critical/End-to-End/data")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to download the CSV from "Today's Price"
async def download_csv(page, download_path):
    try:
        # Click on the "Nepse Data" tab
        await page.wait_for_selector('text=Nepse Data', timeout=10000)
        await page.click('text=Nepse Data')
        logger.info("Clicked on Nepse Data tab")

        # Wait for a second before performing the next action (optional)
        await page.wait_for_timeout(1000)

        # Click on the "Today's Price" option under the "Nepse Data" tab
        await page.wait_for_selector('text=Today\'s Price', timeout=10000)
        await page.click('text=Today\'s Price')
        logger.info("Clicked on Today's Price option")

        # Wait for 2 seconds to ensure the page loads
        await page.wait_for_timeout(2000)

        # Click on the "Download as CSV" button and handle the download
        async with page.expect_download() as download_info:
            await page.click('text=Download as CSV')
            logger.info("Clicked on Download as CSV")

        download = await download_info.value
        # Save the download to the specified path
        download_filename = f"{download_path}/{download.suggested_filename}"
        await download.save_as(download_filename)
        logger.info(f"File downloaded to: {download_filename}")
    except Exception as e:
        logger.error(f"Failed to download CSV: {str(e)}")

# Function to access the list of "Listed Securities" from the network response
async def extract_securities_from_network(page):
    async def handle_response(response):
        try:
            if "company/list" in response.url and response.status == 200:
                # Parse the JSON response body
                json_data = await response.json()

                # Specify CSV file path
                csv_file = f'{DOWNLOAD_PATH}/listed_securities.csv'

                # Write JSON to CSV
                with open(csv_file, mode='w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=json_data[0].keys())
                    writer.writeheader()  # Write the CSV headers
                    writer.writerows(json_data)  # Write the JSON data rows

                logger.info(f"CSV file '{csv_file}' has been created successfully.")
        except Exception as e:
            logger.error(f"Error capturing network response: {str(e)}")

    # Set up a listener for network responses
    page.on("response", handle_response)

    try:
        # Navigate to the "Company" tab
        await page.click('text=Company')
        logger.info("Clicked on Company tab")

        # Wait a second before proceeding
        await page.wait_for_timeout(1000)

        # Click on "Listed Securities"
        await page.click('text=Listed Securities')
        logger.info("Clicked on Listed Securities option")

        # Wait for the network response and give time to capture it
        await page.wait_for_timeout(5000)  # Wait 5 seconds for the network response to be captured
    except Exception as e:
        logger.error(f"Failed to extract listed securities: {str(e)}")

# Main function to call the other functions
async def main():
    # Check if the folder exists, if not, create it
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)
        logger.info(f"Created directory: {DOWNLOAD_PATH}")

    async with async_playwright() as p:
        try:
            # Create a new browser context
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(accept_downloads=True)

            # Create a new page in the context
            page = await context.new_page()

            # Navigate to the NEPSE website using the URL from the .env file
            await page.goto(NEPSE_URL, wait_until='networkidle')
            logger.info(f"Navigated to {NEPSE_URL}")

            # Call the function to download CSV from "Today's Price"
            await download_csv(page, DOWNLOAD_PATH)

            # Call the function to extract listed securities from the network
            await extract_securities_from_network(page)

        except Exception as e:
            logger.error(f"Error in browser operation: {str(e)}")
        finally:
            await browser.close()

# Run the main function
asyncio.run(main())
