from playwright.sync_api import Page


class BasePage:
    # site address
    BASE_URL = "https://automationexercise.com"
    # page path
    PATH = "/"

    def __init__(self, page: Page):
        # page for fixture pytest
        self.page = page

    def open(self):
        # open BASE_URL + PATH, for example .../login
        self.page.goto(self.BASE_URL + self.PATH)
