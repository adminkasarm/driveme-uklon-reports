
import os
from playwright.sync_api import sync_playwright

UKLON_URL = "https://fleets.uklon.com.ua/auth/login"

def main():
    login = os.environ.get("UKLON_LOGIN")
    password = os.environ.get("UKLON_PASSWORD")

    if not login or not password:
        raise RuntimeError("Не заданы UKLON_LOGIN и UKLON_PASSWORD")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(UKLON_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        print("Поля до Continue:")
        for field in page.locator("input").all():
            print({
                "type": field.get_attribute("type"),
                "placeholder": field.get_attribute("placeholder"),
                "name": field.get_attribute("name")
            })

        print("Кнопки:")
        print(page.locator("button").all_text_contents())

        browser.close()

if __name__ == "__main__":
    main()
