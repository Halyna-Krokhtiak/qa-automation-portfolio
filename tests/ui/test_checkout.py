from playwright.sync_api import Page, expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.payment_page import PaymentPage
from pages.product_details_page import ProductDetailsPage

# Test card: demo site accepts any data
TEST_CARD = {
    "name": "Test User",
    "number": "4111111111111111",
    "cvc": "123",
    "month": "12",
    "year": "2030",
}


def test_place_order(page: Page, logged_in_user):
    # Arrange: logged in user has Blue Top in the cart
    product_page = ProductDetailsPage(page)
    product_page.open_product(1)
    product_page.add_to_cart(1)
    product_page.view_cart_link.click()

    # Act: go through checkout and pay
    cart_page = CartPage(page)
    cart_page.proceed_to_checkout_button.click()
    checkout_page = CheckoutPage(page)
    checkout_page.place_order_link.click()
    payment_page = PaymentPage(page)
    payment_page.pay(TEST_CARD)

    # Assert: the order is confirmed
    expect(payment_page.order_placed_title).to_be_visible()


def test_checkout_shows_user_delivery_address(page: Page, logged_in_user):
    # Arrange: logged in user has Blue Top in the cart
    product_page = ProductDetailsPage(page)
    product_page.open_product(1)
    product_page.add_to_cart(1)
    product_page.view_cart_link.click()

    # Act: go to checkout from cart page
    cart_page = CartPage(page)
    cart_page.proceed_to_checkout_button.click()

    # Assert: the delivery address contains Address1 and City
    checkout_page = CheckoutPage(page)
    expect(checkout_page.delivery_address).to_contain_text(
        logged_in_user["address1"]
    )
    expect(checkout_page.delivery_address).to_contain_text(
        logged_in_user["city"]
    )


def test_guest_checkout_asks_to_login(page: Page):
    # Arrange: guest user has Blue Top in the cart
    product_page = ProductDetailsPage(page)
    product_page.open_product(1)
    product_page.add_to_cart(1)
    product_page.view_cart_link.click()

    # Act: go to checkout from cart page
    cart_page = CartPage(page)
    cart_page.proceed_to_checkout_button.click()

    # Assert: the checkout modal is displayed
    expect(cart_page.product_checkout_modal).to_be_visible()


def test_payment_with_empty_card_is_not_placed(page: Page, logged_in_user):
    # Arrange: logged in user has Blue Top in the cart
    product_page = ProductDetailsPage(page)
    product_page.open_product(1)
    product_page.add_to_cart(1)
    product_page.view_cart_link.click()

    # Act: go through checkout and click pay with empty card
    cart_page = CartPage(page)
    cart_page.proceed_to_checkout_button.click()
    checkout_page = CheckoutPage(page)
    checkout_page.place_order_link.click()
    payment_page = PaymentPage(page)
    payment_page.pay_button.click()

    # Assert: the tooltip that name on card is not filled in is displayed
    expect(page).to_have_url(payment_page.BASE_URL + payment_page.PATH)
    message = payment_page.get_name_on_card_validation_message()
    assert message != "", "Browser tooltip for empty Name on Card is not shown"
