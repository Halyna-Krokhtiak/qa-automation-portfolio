from playwright.sync_api import Page

from pages.base_page import BasePage


class ProductsPage(BasePage):
    PATH = "/products"

    def __init__(self, page: Page):
        super().__init__(page)
        # Search form at the top of the page
        self.search_input = page.locator("#search_product")
        self.search_button = page.locator("#submit_search")
        # Heading that appears after a search
        self.searched_title = page.get_by_text("Searched Products")
        # Names of all product cards on the page (one locator, many elements)
        self.product_names = page.locator(".productinfo p")

    def search(self, query: str):
        self.search_input.fill(query)
        self.search_button.click()
