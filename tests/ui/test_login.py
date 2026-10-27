from playwright.sync_api import Page, expect

from pages.login_page import LoginPage


def test_login_with_unregistered_email(page: Page):
    # Arrange: open the login page
    login_page = LoginPage(page)
    login_page.open()

    # Act: enter non unregistered email
    login_page.login("not.registered.user@example.com", "Password123")

    # Assert: the error message is displayed
    expect(login_page.error_message).to_be_visible()


def test_login_with_empty_password(page: Page):
    # Arrange: open the login page
    login_page = LoginPage(page)
    login_page.open()

    # Act: enter any email and password field left empty
    login_page.login("test_qwerty8@example.com", "")
    message = login_page.get_password_validation_message()

    # Assert: the tooltip that password is not filled in is displayed
    expect(page).to_have_url(login_page.BASE_URL + login_page.PATH)
    assert message != "", "Browser tooltip for empty password was not shown"


