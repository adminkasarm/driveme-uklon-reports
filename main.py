
import os
from playwright.sync_api import sync_playwright

UKLON_URL = "https://fleets.uklon.com.ua/auth/login"

def main():
    login = os.environ["UKLON_LOGIN"]
    password = os.environ["UKLON_PASSWORD"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(UKLON_URL, wait_until="domcontentloaded")

        page.locator('input[name="phone"]').fill(login)
        page.get_by_role("button", name="Continue").click()

        page.wait_for_url("**/auth/password**")

        page.locator('input[type="password"]').fill(password)
        page.get_by_role("button", name="Sign in").click()

        page.wait_for_timeout(7000)

        print("Адрес после входа:", page.url)
        print("Заголовок:", page.title())
        print("Текст страницы:")
        print(page.locator("body").inner_text()[:4000])

        browser.close()

if __name__ == "__main__":
    main()
