from playwright.sync_api import Page

from pages.base_page import BasePage


class ProductDetailsPage(BasePage):
    # product id is added to the end: /product_details/1
    PATH = "/product_details/"

    def __init__(self, page: Page):
        super().__init__(page)
        # Quantity field next to the price
        self.quantity_input = page.locator("#quantity")
        self.add_to_cart_button = page.get_by_role(
            "button", name="Add to cart"
        )
        # Link in the "Added!" pop-up
        self.view_cart_link = page.get_by_role("link", name="View Cart")

    def open_product(self, product_id: int):
        # open BASE_URL + PATH + id, for example .../product_details/1
        self.page.goto(self.BASE_URL + self.PATH + str(product_id))

    def add_to_cart(self, quantity: int):
        self.quantity_input.fill(str(quantity))
        self.add_to_cart_button.click()
