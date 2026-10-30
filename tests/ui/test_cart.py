import pytest
from playwright.sync_api import Page, expect

from pages.cart_page import CartPage
from pages.product_details_page import ProductDetailsPage


def test_add_product_with_quantity(page: Page):
    # Arrange: open the Blue Top product page
    product_page = ProductDetailsPage(page)
    product_page.open_product(1)

    # Act: add 4 items and go to the cart
    product_page.add_to_cart(4)
    product_page.view_cart_link.click()

    # Assert: the cart has Blue Top with quantity 4
    cart_page = CartPage(page)
    expect(cart_page.product_names).to_have_text("Blue Top")
    expect(cart_page.product_quantities).to_have_text("4")

@pytest.mark.parametrize(
    "quantity, total",
    [
        (1, "Rs. 500"),
        (3, "Rs. 1500")
    ],
)

def test_cart_total_depends_on_quantity(page: Page, quantity: int, total: str):
    # Arrange: open the Blue Top product page
    product_page = ProductDetailsPage(page)
    product_page.open_product(1)

    # Act: add items and go to the cart
    product_page.add_to_cart(quantity)
    product_page.view_cart_link.click()

    # Assert: the cart has Blue Top with correct quantity and total price
    cart_page = CartPage(page)
    expect(cart_page.product_names).to_have_text("Blue Top")
    expect(cart_page.product_quantities).to_have_text(str(quantity))
    expect(cart_page.product_totals).to_have_text(total)
    expect(cart_page.product_prices).to_have_text("Rs. 500")
