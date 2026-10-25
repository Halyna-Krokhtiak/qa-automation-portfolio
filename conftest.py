import pytest
import requests
from config import BASE_URL, USERNAME, PASSWORD, LOGIN_PATH


@pytest.fixture  # precondition
def booking_id():
    # Precondition: a fresh booking exists
    url = f"{BASE_URL}/booking"
    payload = {
        "firstname": "Test",
        "lastname": "User",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-11-01", "checkout": "2026-11-05"},
        "additionalneeds": "Breakfast",
    }
    headers = {"Accept": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()["bookingid"]


@pytest.fixture  # precondition
def token():
    auth_payload = {"username": USERNAME, "password": PASSWORD}
    auth_response = requests.post(f"{BASE_URL}{LOGIN_PATH}", json=auth_payload)
    return auth_response.json()["token"]


@pytest.fixture  # precondition
def auth_headers(token):
    headers = {"Accept": "application/json", "Cookie": f"token={token}"}
    return headers

