
import os
from playwright.sync_api import sync_playwright

UKLON_URL = "https://fleets.uklon.com.ua/auth/login"

def main():
    login = os.environ["UKLON_LOGIN"]
    password = os.environ["UKLON_PASSWORD"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(accept_downloads=True)

        page.goto(UKLON_URL, wait_until="domcontentloaded")
        page.locator('input[name="phone"]').fill(login)
        page.get_by_role("button", name="Continue").click()
        page.wait_for_url("**/auth/password**")

        page.locator('input[type="password"]').fill(password)
        page.get_by_role("button", name="Sign in").click()
        page.wait_for_url("**/workspace/**", timeout=30000)

        page.goto(
            "https://fleets.uklon.com.ua/workspace/reports#drivers-reports",
            wait_until="domcontentloaded"
        )
        page.wait_for_timeout(5000)

        print("Адрес:", page.url)
        print("Текст раздела отчётов:")
        print(page.locator("body").inner_text()[:6000])

        print("\nКнопки:")
        for button in page.locator("button").all():
            text = button.inner_text().strip()
            if text:
                print(repr(text))

        print("\nПоля:")
        for field in page.locator("input").all():
            print({
                "type": field.get_attribute("type"),
                "placeholder": field.get_attribute("placeholder"),
                "value": field.input_value()
            })

        browser.close()

if __name__ == "__main__":
    main()
