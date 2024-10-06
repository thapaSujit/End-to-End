import asyncio
from playwright.async_api import async_playwright
import time  # Added for manual sleep

async def main():
    async with async_playwright() as p:
        # Launch the browser in non-headless mode for debugging (ensure headless=False to see the browser actions)
        browser = await p.chromium.launch(headless=False, slow_mo=500)  # slow_mo adds a delay (500 ms here)
        page = await browser.new_page()
        
        # Navigate to the website and wait until the network is idle
        await page.goto('https://www.nepalstock.com', wait_until='networkidle')
        
        try:
            # Wait for the "Company" tab to be available (Adjust the selector based on actual element in DOM)
            await page.wait_for_selector('text=Company', timeout=60000)  # Wait for the Company tab
            
            # Sleep for a few seconds to make sure you can observe the browser loading
            time.sleep(2)  # Sleep for 2 seconds before clicking
            
            # Click the "Company" tab to show the dropdown menu
            await page.click('text=Company')
            print("Successfully clicked on the Company tab")
            
            # Sleep for a few seconds to observe the click and dropdown
            time.sleep(2)  # Sleep for 2 seconds after clicking
            
            # Now click on the "Listed Securities" option from the dropdown
            await page.click('text=Listed Securities')
            print("Successfully clicked on Listed Securities")

            # Sleep for a few seconds to observe the page change
            time.sleep(2)

        except Exception as e:
            print(f"Error during scraping: {e}")
        
        # Close the browser
        await browser.close()

# Run the main function
asyncio.run(main())
