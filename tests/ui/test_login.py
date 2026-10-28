from playwright.sync_api import Page, expect

from pages.login_page import LoginPage


def test_login_with_unregistered_email(page: Page):
    # Arrange: open the login page
    login_page = LoginPage(page)
    login_page.open()

    # Act: enter unregistered email
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


def test_login_with_valid_credentials(page: Page, registered_user):
    # Arrange: open the login page
    login_page = LoginPage(page)
    login_page.open()

    # Act: log in with the user created via API
    login_page.login(registered_user["email"], registered_user["password"])

    # Assert: header shows the user's name
    expect(login_page.logged_in_as).to_contain_text(registered_user["name"])


def test_login_with_wrong_password(page: Page, registered_user):
    # Arrange: open the login page
    login_page = LoginPage(page)
    login_page.open()

    # Act: log in with the user created via API with wrong password
    login_page.login(registered_user["email"], "WrongPassword123")

    # Assert: error message is displayed
    expect(login_page.error_message).to_be_visible()


def test_logout_redirects_to_login_page(page: Page, registered_user):
    # Arrange: login with registered user
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(registered_user["email"], registered_user["password"])

    # Act: click logout button
    login_page.logout_link.click()

    # Assert: user is logged out and the login page is shown
    expect(page).to_have_url(login_page.BASE_URL + login_page.PATH)
