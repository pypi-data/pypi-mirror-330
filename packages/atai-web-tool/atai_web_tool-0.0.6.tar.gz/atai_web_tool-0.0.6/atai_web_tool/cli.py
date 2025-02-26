import argparse
import asyncio
import sys
from playwright.async_api import async_playwright
from readability import Document
from bs4 import BeautifulSoup

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

async def extract_content(url: str, headless: bool, no_sandbox: bool) -> str:
    async with async_playwright() as p:
        args = ["--no-sandbox"] if no_sandbox else []
        browser = await p.chromium.launch(headless=headless, args=args)
        page = await browser.new_page()

        # Block non-essential resources (images, stylesheets, fonts) for faster loading.
        await page.route("**/*", lambda route, request: 
            route.abort() if request.resource_type in ["image", "stylesheet", "font"] else route.continue_()
        )

        # Navigate to the URL and wait until the DOM content is loaded, with a shorter timeout.
        await page.goto(url, wait_until="domcontentloaded", timeout=15000)
        
        # Retrieve the full HTML content of the page.
        raw_html = await page.content()
        
        # Use readability-lxml to extract the main content HTML.
        doc = Document(raw_html)
        main_html = doc.summary()
        
        # Clean the HTML to get plain text.
        soup = BeautifulSoup(main_html, "html.parser")
        main_text = soup.get_text(separator="\n", strip=True)
        
        await browser.close()
        return main_text

def main():
    parser = argparse.ArgumentParser(
        description="Extract the main content from a webpage using Playwright, readability-lxml, and BeautifulSoup."
    )
    parser.add_argument("url", help="The URL of the webpage to extract content from.")
    parser.add_argument(
        "--no-sandbox",
        action="store_true",
        help="Run browser with no sandbox (useful when running as root or in restricted environments)."
    )
    parser.add_argument(
        "--headless",
        type=str2bool,
        nargs='?',
        const=True,
        default=True,
        help="Run browser in headless mode (default: True). Use '--headless false' to disable headless mode."
    )
    args = parser.parse_args()

    try:
        content = asyncio.run(extract_content(args.url, args.headless, args.no_sandbox))
        print(content)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
