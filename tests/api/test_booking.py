import requests  # library is sending the requests instead of browser
from config import USERNAME, PASSWORD, LOGIN_PATH

BASE_URL = "https://restful-booker.herokuapp.com"  #  API address


def test_get_booking_ids_returns_200():
    # Arrange: preconditions
    url = f"{BASE_URL}/booking"

    # Act: receive data from booking
    response = requests.get(url)

    # Assert: checking the correct status code 200
    assert response.status_code == 200


def test_get_data_from_ping_and_status_201():
    # Arrange: preconditions
    url = f"{BASE_URL}/ping"

    # Act: test case step to receive data from ping
    response = requests.get(url)

    # Assert: checking the correct status code 201
    assert response.status_code == 201


def test_get_booking_ids_returns_not_empty_list():
    # Arrange: preconditions
    url = f"{BASE_URL}/booking"

    # Act: get data from the list
    response = requests.get(url)
    body = response.json()
    first_booking = body[0]

    # Assert: first element is shown from the list
    assert len(body) > 0
    assert "bookingid" in first_booking


def test_login_success_with_valid_creds():
    # Arrange: user login with valid creds
    url = f"{BASE_URL}{LOGIN_PATH}"
    payload = {"username": USERNAME, "password": PASSWORD}

    # Act: sending user creds
    response = requests.post(url, json=payload)
    body = response.json()

    # Assert: token is present and status code 200
    assert response.status_code == 200
    assert "token" in body
