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
