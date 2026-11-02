from playwright.sync_api import Page

from pages.base_page import BasePage


class PaymentPage(BasePage):
    PATH = "/payment"

    def __init__(self, page: Page):
        super().__init__(page)
        # Card form
        self.name_on_card_input = page.locator('[data-qa="name-on-card"]')
        self.card_number_input = page.locator('[data-qa="card-number"]')
        self.cvc_input = page.locator('[data-qa="cvc"]')
        self.expiry_month_input = page.locator('[data-qa="expiry-month"]')
        self.expiry_year_input = page.locator('[data-qa="expiry-year"]')
        self.pay_button = page.locator('[data-qa="pay-button"]')
        # Title after a successful payment
        self.order_placed_title = page.get_by_text("Order Placed!")

    def pay(self, card: dict):
        self.name_on_card_input.fill(card["name"])
        self.card_number_input.fill(card["number"])
        self.cvc_input.fill(card["cvc"])
        self.expiry_month_input.fill(card["month"])
        self.expiry_year_input.fill(card["year"])
        self.pay_button.click()

    def get_name_on_card_validation_message(self) -> str:
        return self.name_on_card_input.evaluate("el => el.validationMessage")
