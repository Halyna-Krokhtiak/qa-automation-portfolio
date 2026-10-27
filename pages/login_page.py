from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = "/login"

    def __init__(self, page: Page):
        # Викликаємо __init__ з BasePage, щоб зберегти self.page
        super().__init__(page)
        # locators: page elements for "Login to your account"
        self.email_input = page.locator('[data-qa="login-email"]')
        self.password_input = page.locator('[data-qa="login-password"]')
        self.login_button = page.locator('[data-qa="login-button"]')
        self.error_message = page.get_by_text(
            "Your email or password is incorrect!"
        )

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()

    def get_password_validation_message(self) -> str:
        return self.password_input.evaluate("el => el.validationMessage")
