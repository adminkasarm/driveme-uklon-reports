
import os
from playwright.sync_api import sync_playwright

UKLON_URL = "https://fleets.uklon.com.ua/workspace/reports#drivers-reports"

def main():
    login = os.environ.get("UKLON_LOGIN")
    password = os.environ.get("UKLON_PASSWORD")

    if not login or not password:
        raise RuntimeError("Не заданы UKLON_LOGIN и UKLON_PASSWORD")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(UKLON_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)

        print("Заголовок страницы:", page.title())
        print("Текущий адрес:", page.url)
        print("Текст страницы:")
        print(page.locator("body").inner_text()[:5000])

        browser.close()

if __name__ == "__main__":
    main()
