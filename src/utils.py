import os
import csv
import logging
from fastapi import HTTPException

# Initialize logging
logger = logging.getLogger(__name__)

async def download_csv(page, download_path):
    try:
        await page.wait_for_selector('text=Nepse Data', timeout=30000)
        await page.click('text=Nepse Data')
        logger.info("Clicked on Nepse Data tab")

        await page.wait_for_selector('text=Today\'s Price', timeout=30000)
        await page.click('text=Today\'s Price')
        logger.info("Clicked on Today's Price option")

        # Wait for 2 seconds to ensure the page loads
        await page.wait_for_timeout(3000)

        async with page.expect_download(timeout=60000) as download_info:  # Wait up to 60 seconds
            await page.click('text=Download as CSV')
            logger.info("Clicked on Download as CSV")

        download = await download_info.value
        download_filename = os.path.join(download_path, download.suggested_filename)
        await download.save_as(download_filename)
        logger.info(f"File downloaded to: {download_filename}")

        return download_filename
    except Exception as e:
        logger.error(f"Failed to download CSV: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to download CSV")

async def extract_securities_from_network(page, download_path):
    securities_data = []
    async def handle_response(response):
        if "company/list" in response.url and response.status == 200:
            json_data = await response.json()
            securities_data.extend(json_data)
            csv_file = os.path.join(download_path, "listed_securities.csv")
            with open(csv_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=json_data[0].keys())
                writer.writeheader()
                writer.writerows(json_data)
            logger.info(f"CSV file '{csv_file}' has been created successfully.")
    page.on("response", handle_response)
    try:
        await page.click('text=Company')
        logger.info("Clicked on Company tab")
        await page.wait_for_timeout(2000)
        await page.click('text=Listed Securities')
        logger.info("Clicked on Listed Securities option")
        await page.wait_for_timeout(5000)
    except Exception as e:
        logger.error(f"Failed to extract listed securities: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to extract listed securities")

    return securities_data
