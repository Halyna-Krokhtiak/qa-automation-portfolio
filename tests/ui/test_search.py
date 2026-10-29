import pytest
from playwright.sync_api import Page, expect

from pages.products_page import ProductsPage


@pytest.mark.parametrize("query", ["Blue Top", "Men Tshirt", "Stylish Dress"])
def test_search_shows_searched_product(page: Page, query: str):
    # Arrange: open the products page
    products_page = ProductsPage(page)
    products_page.open()

    # Act: search by product name
    products_page.search(query)

    # Assert: product with this name is in the results
    expect(products_page.product_names).to_contain_text([query])


def test_search_shows_searched_products_title(page: Page):
    # Arrange: open the products page
    products_page = ProductsPage(page)
    products_page.open()

    # Act: search by product name
    products_page.search("Blue Top")

    # Assert: search product title is displayed
    expect(products_page.searched_title).to_be_visible()
