from playwright.sync_api import sync_playwright


def parse_ozon(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        page.goto(url)

        input("Пройди капчу и нажми Enter в терминале...")

        print("TITLE:")
        print(page.title())

        input("Нажми Enter для закрытия браузера...")

        browser.close()
