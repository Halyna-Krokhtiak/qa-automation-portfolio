from playwright.sync_api import Page

from pages.base_page import BasePage


class CartPage(BasePage):
    PATH = "/view_cart"

    def __init__(self, page: Page):
        super().__init__(page)
        # Columns of the cart table: one element per product row
        self.product_names = page.locator(".cart_description h4 a")
        self.product_prices = page.locator(".cart_price p")
        self.product_quantities = page.locator(".cart_quantity button")
        self.product_totals = page.locator(".cart_total_price")
