from playwright.sync_api import sync_playwright
def parse_ozon(url):
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir="./ozon_profile",
            headless=False,
        )

        page = context.new_page()

        page.goto(url)

        title = page.locator("h1").inner_text()

        price = int(
            page.locator('[data-widget="webPrice"]')
            .inner_text()
            .split("\n")[0]
            .replace("\u2009", "")
            .replace("₽", "")
        )

        return {
            "title": title,
            "price": price,
        }
