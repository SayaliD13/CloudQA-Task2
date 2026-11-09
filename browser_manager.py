from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright
from config import BROWSER_TIMEOUT_MS, NAVIGATION_TIMEOUT_MS


class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None

    def start(self, headless=False):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.page = self.browser.new_page()
        self.page.set_default_timeout(BROWSER_TIMEOUT_MS)
        self.page.set_default_navigation_timeout(NAVIGATION_TIMEOUT_MS)
        return self.page

    def save_failure_screenshot(self):
        if self.page is None:
            return ""

        folder = Path("screenshots")
        folder.mkdir(exist_ok=True)

        file_name = "failure_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
        file_path = folder / file_name
        self.page.screenshot(path=str(file_path), full_page=True)
        return str(file_path)

    def close(self):
        if self.browser is not None:
            try:
                self.browser.close()
            except Exception:
                pass

        if self.playwright is not None:
            try:
                self.playwright.stop()
            except Exception:
                pass
