from playwright.sync_api import sync_playwright
import re


def parse_citilink(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(5000)

        title = page.locator("h1").first.inner_text()

        body = page.locator("body").inner_text()

        prices = re.findall(r"\d[\d ]*₽", body)

        price = int(
            prices[-1]
            .replace("₽", "")
            .replace(" ", "")
        )

        browser.close()

        return {
            "title": title,
            "price": price,
        }