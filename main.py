
import os
from playwright.sync_api import sync_playwright

UKLON_URL = "https://fleets.uklon.com.ua/auth/login"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(UKLON_URL, wait_until="domcontentloaded")
        page.locator('input[name="phone"]').fill(os.environ["UKLON_LOGIN"])
        page.get_by_role("button", name="Continue").click()
        page.wait_for_url("**/auth/password**")
        page.locator('input[type="password"]').fill(os.environ["UKLON_PASSWORD"])
        page.get_by_role("button", name="Sign in").click()
        page.wait_for_url("**/workspace/**", timeout=30000)

        page.goto(
            "https://fleets.uklon.com.ua/workspace/reports#drivers-reports",
            wait_until="domcontentloaded"
        )
        page.wait_for_timeout(4000)

        page.get_by_text("DriveMe Івано-Франківськ", exact=True).click()
        page.wait_for_timeout(1500)

        print("СПИСОК ПАРКОВ:")
        print(page.locator("body").inner_text()[:5000])

        print("\nКНОПКИ:")
        for button in page.locator("button").all():
            text = button.inner_text().strip()
            if text:
                print(repr(text))

        browser.close()

if __name__ == "__main__":
    main()
