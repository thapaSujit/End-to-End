from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from src.utils import download_csv, extract_securities_from_network
from dotenv import load_dotenv
import os
from playwright.async_api import async_playwright

# Load environment variables
load_dotenv()
NEPSE_URL = os.getenv("NEPSE_URL")
DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", "./data")

router = APIRouter()

@router.get("/download-price-csv")
async def download_price_csv():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=[
            "--disable-blink-features=AutomationControlled",  # Avoid detection as headless
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage"
        ])
        context = await browser.new_context(accept_downloads=True, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        page = await context.new_page()
        await page.goto(NEPSE_URL, wait_until='networkidle', timeout=60000)
        csv_path = await download_csv(page, DOWNLOAD_PATH)
        await browser.close()
    return FileResponse(csv_path, filename=os.path.basename(csv_path))

@router.get("/get-listed-securities")
async def get_listed_securities():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage"
        ])
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        page = await context.new_page()
        await page.goto(NEPSE_URL, wait_until='networkidle', timeout=60000)
        securities_data = await extract_securities_from_network(page, DOWNLOAD_PATH)
        await browser.close()
    return JSONResponse(content=securities_data)
