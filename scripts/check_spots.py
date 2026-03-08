import asyncio
import re
import sys
from playwright.async_api import async_playwright

URL = "https://shop.rs.berkeley.edu/Program/GetProgramDetails?courseId=037a8c42-070b-42ff-b72b-d18c5100bb44"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(URL, wait_until="networkidle", timeout=60000)

        # Find the spots-tag element: <p class="card-text">12 Spots Left</p>
        el = page.locator(".spots-tag p").first
        text = await el.inner_text()
        await browser.close()

    match = re.search(r"(\d+)\s+spots?\s+left", text, re.IGNORECASE)
    if not match:
        print(f"ERROR: Could not parse spots from: {text!r}", file=sys.stderr)
        sys.exit(1)

    print(match.group(1))

asyncio.run(main())
