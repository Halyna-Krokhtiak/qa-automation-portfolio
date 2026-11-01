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


def test_add_two_different_products(page: Page):
    # Arrange: open Blue Top PDP and add to cart, open Men Tshirt PDP
    product_page = ProductDetailsPage(page)
    product_page.open_product(1)
    product_page.add_to_cart(1)
    product_page.continue_shopping_button.click()
    product_page.open_product(2)

    # Act: add Men Tshirt product to the cart and open cart page
    product_page.add_to_cart(1)
    product_page.view_cart_link.click()

    # Assert: the cart has Blue Top and Men Tshirt products
    cart_page = CartPage(page)
    expect(cart_page.product_names).to_have_text(["Blue Top", "Men Tshirt"])

def test_remove_product_from_cart(page: Page):
    # Arrange: open the Blue Top PDP and add to cart, go to cart page
    product_page = ProductDetailsPage(page)
    product_page.open_product(1)
    product_page.add_to_cart(1)
    product_page.view_cart_link.click()

    # Act: remove product from cart page
    cart_page = CartPage(page)
    cart_page.product_quantity_delete.click()

    # Assert: the cart page is shown with no products
    expect(cart_page.product_names).to_have_count(0)
    expect(cart_page.product_empty_cart).to_be_visible()


def test_add_same_product_twice_increases_quantity(page: Page):
   # Arrange: open the Blue Top PDP and add to cart
    product_page = ProductDetailsPage(page)
    product_page.open_product(1)
    product_page.add_to_cart(1)
    product_page.continue_shopping_button.click()

    # Act: add Blue Top product to the cart once again
    product_page.add_to_cart(1)
    product_page.view_cart_link.click()

    # Assert: the cart has Blue Top product with quantity 2
    cart_page = CartPage(page)
    expect(cart_page.product_names).to_have_text("Blue Top")
    expect(cart_page.product_totals).to_have_text("Rs. 1000")
    expect(cart_page.product_quantities).to_have_text("2")

