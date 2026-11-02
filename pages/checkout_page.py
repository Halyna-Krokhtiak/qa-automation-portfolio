from playwright.sync_api import Page

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    PATH = "/checkout"

    def __init__(self, page: Page):
        super().__init__(page)
        # "Your delivery address" block
        self.delivery_address = page.locator("#address_delivery")
        self.place_order_link = page.get_by_role("link", name="Place Order")
