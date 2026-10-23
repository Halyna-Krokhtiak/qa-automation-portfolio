import requests  # library is sending the requests instead of browser
from config import USERNAME, PASSWORD, LOGIN_PATH

BASE_URL = "https://restful-booker.herokuapp.com"  # API address


def test_get_booking_ids_returns_200():
    # Arrange: preconditions
    url = f"{BASE_URL}/booking"

    # Act: receive data from booking
    response = requests.get(url)

    # Assert: checking the correct status code 200
    assert response.status_code == 200


def test_get_data_from_ping_returns_201():
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


def test_login_with_valid_creds_returns_token_with_status_200():
    # Arrange: user login with valid creds
    url = f"{BASE_URL}{LOGIN_PATH}"
    payload = {"username": USERNAME, "password": PASSWORD}

    # Act: sending user creds
    response = requests.post(url, json=payload)
    body = response.json()

    # Assert: token is present and status code 200
    assert response.status_code == 200
    assert "token" in body


def test_create_booking_returns_bookingid():
    # Arrange: new booking data
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

    # Act sending new booking data
    response = requests.post(url, json=payload, headers=headers)
    body = response.json()

    # Assert new booking id is created
    assert response.status_code == 200
    assert "bookingid" in body
    assert body["booking"]["firstname"] == "Test"
    assert isinstance(body["bookingid"], int)


def test_get_booking_by_id_returns_created_booking():
    # Arrange: new booking data
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
    booking_id = response.json()["bookingid"]

    # Act sending new booking id
    url = f"{BASE_URL}/booking/{booking_id}"
    response = requests.get(url, headers=headers)
    body = response.json()

    # Assert new booking shows firstname
    assert response.status_code == 200
    assert body["firstname"] == "Test"


def test_update_name_for_created_booking():
    # Arrange: new booking data
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
    booking_id = response.json()["bookingid"]
    auth_payload = {"username": USERNAME, "password": PASSWORD}
    auth_response = requests.post(f"{BASE_URL}{LOGIN_PATH}", json=auth_payload)
    token = auth_response.json()["token"]
    headers = {"Accept": "application/json", "Cookie": f"token={token}"}
    payload["firstname"] = "Testing"

    # Act sending booking id with changed firstname
    url = f"{BASE_URL}/booking/{booking_id}"
    response = requests.put(url, json=payload, headers=headers)
    body = response.json()

    # Assert firstname is updated
    assert response.status_code == 200
    assert body["firstname"] == "Testing"


def test_delete_created_booking():
    # Arrange: new booking data
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
    booking_id = response.json()["bookingid"]
    auth_payload = {"username": USERNAME, "password": PASSWORD}
    auth_response = requests.post(f"{BASE_URL}{LOGIN_PATH}", json=auth_payload)
    token = auth_response.json()["token"]
    headers = {"Accept": "application/json", "Cookie": f"token={token}"}

    # Act deleting new booking id
    url = f"{BASE_URL}/booking/{booking_id}"
    response = requests.delete(url, headers=headers)

    # Assert new booking is deleted
    assert response.status_code == 201
    get_response = requests.get(url, headers=headers)
    assert get_response.status_code == 404
