
import os
from playwright.sync_api import sync_playwright

UKLON_URL = "https://fleets.uklon.com.ua/auth/login"

def main():
    login = os.environ["UKLON_LOGIN"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(UKLON_URL, wait_until="domcontentloaded")
        page.locator('input[name="phone"]').fill(login)
        page.get_by_role("button", name="Continue").click()

        page.wait_for_timeout(3000)

        print("Адрес после Continue:", page.url)
        print("Поля после Continue:")

        for field in page.locator("input").all():
            print({
                "type": field.get_attribute("type"),
                "placeholder": field.get_attribute("placeholder"),
                "name": field.get_attribute("name")
            })

        print("Текст страницы:")
        print(page.locator("body").inner_text()[:3000])

        browser.close()

if __name__ == "__main__":
    main()
