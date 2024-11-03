from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from src.utils import download_csv, extract_securities_from_network
from dotenv import load_dotenv
import os
import asyncio
from playwright.async_api import async_playwright

# Load environment variables
load_dotenv()
NEPSE_URL = os.getenv("NEPSE_URL")
DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", "./data")

router = APIRouter()

@router.get("/download-price-csv")
async def download_price_csv():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=["--disable-http2"])
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()
        await page.goto(NEPSE_URL, wait_until='networkidle')
        csv_path = await download_csv(page, DOWNLOAD_PATH)
        await browser.close()
    return FileResponse(csv_path, filename=os.path.basename(csv_path))

@router.get("/get-listed-securities")
async def get_listed_securities():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=["--disable-http2"])
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(NEPSE_URL, wait_until='networkidle')
        securities_data = await extract_securities_from_network(page, DOWNLOAD_PATH)
        await browser.close()
    return JSONResponse(content=securities_data)
