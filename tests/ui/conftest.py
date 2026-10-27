import uuid

import pytest
import requests
from playwright.sync_api import Page
API_URL = "https://automationexercise.com/api"


@pytest.fixture(autouse=True)
def accept_cookies(page: Page):
    # "Consent" button in cookies banner (not for all countries)
    consent_button = page.locator(".fc-cta-consent")

    def click_consent():
        consent_button.click()

    #  Playwright will close the banner when it apppears in any page of the site
    page.add_locator_handler(consent_button, click_consent)

@pytest.fixture  # create a new user
def registered_user():
    payload = {
        "name": "Test",
        "email":
        f"test_{uuid.uuid4().hex[:8]}@example.com",
        "password": "Password123",
        "title": "Mrs",
        "birth_date": 11,
        "birth_month": 11,
        "birth_year": 2000,
        "firstname": "User",
        "lastname": "Testing",
        "country": "Canada",
        "city": "Toronto",
        "zipcode": "M5A 4E5",
        "address1": "6 AITKEN PL TORONTO",
        "mobile_number": 1111111111,
        "company": "tessst",
        "address2": "6 AITKEN PL TORONTO",
        "state": "ontario"
    }
    response = requests.post(f"{API_URL}/createAccount", data=payload)
    assert response.json()["responseCode"] == 201
    yield payload
    requests.delete(
        f"{API_URL}/deleteAccount",
        data={"email": payload["email"], "password": payload["password"]},
    )
